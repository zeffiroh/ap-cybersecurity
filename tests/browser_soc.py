import functools
import http.server
import json
import socketserver
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from builder import levels as LV
from builder import toolsteps as T

SITE = ROOT / "site"
CASES = SITE / "assets" / "linux" / "cases"
FAILS = []


class Quiet(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, ".js": "text/javascript", ".wasm": "application/wasm"}

    def log_message(self, *a):
        pass


def check(ok, what):
    print(("  ok    " if ok else "  FAIL  ") + what)
    if not ok:
        FAILS.append(what)


def case_files(case):
    man = json.loads((CASES / case / "manifest.json").read_text(encoding="utf-8"))
    out = {}
    for f in man["files"]:
        if f.startswith("case/"):
            p = CASES / case / f
            try:
                t = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if "\x00" not in t:
                out[f[5:]] = t
    return out


HARNESS = """async ([tool, files, state]) => {
  const box = document.createElement('div');
  document.body.replaceChildren(box);
  window.REC = [];
  AayatTools.get(tool).mount(box, {
    state: state || {}, saved: null, files: () => files, remember: () => {},
    recordLabel: 'Add to notebook', record: (st, text) => { window.REC.push({st, text}); }
  });
  return true;
}"""


def open_page(browser, base):
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.route("**/blank", lambda route: route.fulfill(status=200, content_type="text/html", body="<!DOCTYPE html><title>t</title><body></body>"))
    page.goto(base + "/blank")
    for s in ["tools.js"] + T.TOOL_FILES:
        page.add_script_tag(url=f"{base}/assets/theme/{s}")
    page.add_style_tag(url=f"{base}/assets/theme/tools.css")
    return page, errors


def mount(page, tool, files, state=None):
    page.evaluate(HARNESS, [tool, files, state or {}])
    page.wait_for_function("() => { const n = document.querySelector('[data-r=note]'); return n && !/Loading/.test(n.textContent); }", timeout=30000)


def msg(page):
    return page.inner_text('[data-r="msg"]')


def saved(page):
    page.click('[data-r="save"]')
    rec = page.evaluate("window.REC")
    return rec[-1] if rec else None


def guided(tool, state):
    out = LV.variant([{"t": "md", "s": T.fence(tool, state)}], "guided")[0]["s"]
    return T.steps_in(out)[0][1]


def yara(page, files):
    mount(page, "yara", files)
    page.click('[data-r="go"]')
    page.wait_for_function("() => /files match|didn't compile|didn't load/.test(document.querySelector('[data-r=msg]').textContent)", timeout=60000)
    m = msg(page)
    check("invoice.eml" in m and "proxy.log" in m, f"the starter YARA rule matches the phishing email and the proxy log ({m[:120]})")
    check(page.locator("tr.ty-hit").count() >= 2, "YARA lists each matched string with its offset")
    page.locator("tr.ty-hit").first.click()
    check(page.locator(".ty-ctx mark").count() == 1, "clicking a hit shows the match in context")
    rec = saved(page)
    check(rec and rec["st"]["n"] >= 2 and "rule" in rec["st"]["blank"], "the recorded YARA step keeps the rule and the count")
    g = guided("yara", rec["st"])
    mount(page, "yara", files, g)
    check(page.input_value('[data-r="rule"]') == "", "in Guided the rule box starts empty")
    page.fill('[data-r="rule"]', 'rule r { strings: $a = "nope" condition: $b }')
    page.click('[data-r="go"]')
    page.wait_for_function("() => /didn't compile/.test(document.querySelector('[data-r=msg]').textContent)", timeout=30000)
    check("unknown pattern" in page.inner_text('[data-r="err"]'), "a broken rule shows the compiler's error")
    page.click('[data-r="show"]')
    page.click('[data-r="go"]')
    page.wait_for_function("() => /Same as the recorded rule/.test(document.querySelector('[data-r=msg]').textContent)", timeout=30000)
    check(True, "the recorded rule gives the same count in Guided")


def sigma(page, files):
    mount(page, "sigma", files)
    page.click('[data-r="go"]')
    m = msg(page)
    check("matched 1 of" in m, f"the starter Sigma rule finds the one scheduled task ({m[:120]})")
    page.locator('[data-k]').first.check()
    check("True positives 1" in page.inner_text('[data-r="score"]'), "ticking the hit as malicious scores a true positive")
    rec = saved(page)
    check(rec and len(rec["st"]["bad"]) == 1, "the recorded Sigma step keeps the labelled event")
    g = guided("sigma", rec["st"])
    mount(page, "sigma", files, g)
    page.fill('[data-r="rule"]', "title: Any logon\nlogsource:\n  product: windows\ndetection:\n  a:\n    EventID: 4624\n  condition: a\n")
    page.click('[data-r="go"]')
    s = page.inner_text('[data-r="score"]')
    check("Missed 1" in s and "True positives 0" in s, f"a wrong rule shows the labelled event as missed ({s})")
    page.fill('[data-r="rule"]', "title: t\ndetection:\n  a:\n    EventID: 1\n  condition: a and b\n")
    page.click('[data-r="go"]')
    check("no search with that name" in msg(page), "a bad condition gives a clear message")
    page.click('[data-r="show"]')
    page.click('[data-r="spl"]')
    page.wait_for_function("() => !document.querySelector('[data-r=out]').hidden || /couldn't/.test(document.querySelector('[data-r=msg]').textContent)", timeout=240000)
    out = page.inner_text('[data-r="out"]')
    check("EventID=4698" in out and "Action" in out and "Users" in out, f"pySigma converts the rule to a search query ({out[:160]})")


def sql(page, files):
    mount(page, "sql", files)
    check("security" in page.inner_text('[data-r="schema"]'), "SQL over logs makes a table per log")
    page.fill('[data-r="q"]', "SELECT EventID, count(*) AS n FROM security GROUP BY EventID ORDER BY n DESC")
    page.click('[data-r="go"]')
    m = msg(page)
    check("11 rows" in m, f"a GROUP BY over the Security log works ({m})")
    check("4624" in page.inner_text('[data-r="out"]'), "the results table shows the event IDs")
    page.fill('[data-r="q"]', "DELETE FROM security")
    page.click('[data-r="go"]')
    check("Only SELECT" in msg(page), "changing the evidence is refused")
    page.fill('[data-r="q"]', "SELECT count(*) FROM events")
    page.click('[data-r="go"]')
    check("1 row" in msg(page), "the events view joins every log")


def alerts(page, files):
    mount(page, "alerts", files)
    rows = page.locator("tr.ta-row").count()
    check(rows == 10, f"the alert queue lists the 10 phish alerts ({rows})")
    first = page.locator("tr.ta-row").first.inner_text()
    check("critical" in first, "the queue is ordered by severity")
    page.locator("tr.ta-row").first.click()
    page.select_option('[data-r="disp"]', "escalate")
    page.fill('[data-r="gen"]', "Ransomware on fs01. Cable pulled at 09:52.")
    page.click('[data-r="done"]')
    check("9 alerts are still not triaged" in msg(page) and "1 escalated" in msg(page), f"finishing shows what is left ({msg(page)})")
    rec = saved(page)
    check(rec and rec["st"]["n"] == 1, "the recorded queue step keeps the dispositions")
    g = guided("alerts", rec["st"])
    mount(page, "alerts", files, g)
    page.click('[data-r="done"]')
    check("0 of 1 match" in msg(page), "in Guided, students are told how many dispositions match")


def hunt(page, files):
    mount(page, "hunt", files)
    page.fill('[data-r="hyp"]', "The loader kept a way back in with a scheduled task.")
    page.fill('[data-r="q"]', "UpdCheck")
    page.click('[data-r="run"]')
    check("matching line" in msg(page), "the hunt search runs across the files")
    page.click('[data-r="add"]')
    page.select_option('[data-r="verdict"]', "confirmed")
    page.click('[data-r="done"]')
    check("1 logged search" in msg(page), f"finishing a hunt needs a hypothesis, a search and a result ({msg(page)})")


def ioc(page, files):
    mount(page, "ioc", files)
    page.click('[data-r="go"]')
    m = msg(page)
    check("match known-bad intel" in m, f"indicators are extracted and checked against intel ({m})")
    text = page.inner_text('[data-r="list"]')
    check("kestrel-logistlcs.com" in text and "malicious" in text, "the lookalike domain is flagged malicious")
    heat = page.inner_text('[data-r="heat"]')
    check("T1566.001" in heat and "Initial Access" in heat, "intel techniques appear on the ATT&CK heatmap")
    page.fill('[data-r="tech"]', "T1486")
    page.click('[data-r="map"]')
    check("Data Encrypted for Impact" in page.inner_text('[data-r="heat"]'), "a technique mapped by hand is added with its name")


def email(page, files):
    mount(page, "email", files)
    n = page.locator('[data-r="q"] button').count()
    check(n == 5, f"the email queue lists all 5 emails ({n})")
    card = page.inner_text('[data-r="card"]')
    check("Risk:" in card, "an email opens with its risk and reasons")
    page.locator('[data-r="q"] button', has_text="Action required").click()
    check("really goes to kestrel-sso.login-check.example" in page.inner_text('[data-r="card"]'), "a disguised link is caught")
    page.locator('[data-r="q"] button', has_text="Urgent and confidential").click()
    c = page.inner_text('[data-r="card"]')
    check("DMARC passed" in c and "free mail address" in c, "CEO fraud that passes DMARC is still flagged")
    page.select_option('[data-r="v"]', "bec")
    page.click('[data-r="done"]')
    check("1 to block or stop" in msg(page), "finishing the email queue counts what to block")


def main():
    from playwright.sync_api import sync_playwright
    sys.stdout.reconfigure(encoding="utf-8")
    handler = functools.partial(Quiet, directory=str(SITE))
    with socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler) as server:
        base = f"http://127.0.0.1:{server.server_address[1]}"
        threading.Thread(target=server.serve_forever, daemon=True).start()
        phish = case_files("phish")
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page, errors = open_page(browser, base)
            for name, fn in (("YARA", yara), ("Sigma", sigma), ("SQL over logs", sql), ("Alert queue", alerts), ("Threat hunt", hunt),
                             ("Indicators", ioc), ("Email triage", email)):
                print(name)
                try:
                    fn(page, phish)
                except Exception as e:
                    check(False, f"{name} ran without an exception ({e.__class__.__name__}: {str(e)[:200]})")
            check(not errors, f"no page errors ({errors[:3]})")
            browser.close()
        server.shutdown()
    print(f"\n{len(FAILS)} failed" if FAILS else "\nall passed")
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
