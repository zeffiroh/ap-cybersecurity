import functools
import http.server
import json
import socketserver
import struct
import sys
import tempfile
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from builder import levels as LV
from builder import toolsteps as T

SITE = ROOT / "site"
CASE = "assets/linux/cases/phish/case/"
FAILS = []


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def check(ok, what):
    print(("  ok    " if ok else "  FAIL  ") + what)
    if not ok:
        FAILS.append(what)


HARNESS = """async ([tool, files, state, saved]) => {
  const box = document.createElement('div');
  document.body.replaceChildren(box);
  window.REC = [];
  window.MEM = null;
  AayatTools.get(tool).mount(box, {
    state: state || {}, saved: saved || null,
    files: () => files,
    remember: (v) => { window.MEM = v; },
    recordLabel: 'Add to notebook',
    record: (st, text) => { window.REC.push({st, text}); }
  });
  return true;
}"""


def blank_page(browser, base):
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.route("**/blank", lambda route: route.fulfill(status=200, content_type="text/html", body="<!DOCTYPE html><title>t</title><body></body>"))
    page.goto(base + "/blank")
    for s in ("tools.js", "tool-packets.js", "tool-proxy.js", "tool-events.js"):
        page.add_script_tag(url=f"{base}/assets/theme/{s}")
    page.add_style_tag(url=f"{base}/assets/theme/tools.css")
    return page, errors


def guided(tool, state):
    out = LV.variant([{"t": "md", "s": T.fence(tool, state)}], "guided")[0]["s"]
    return T.steps_in(out)[0][1]


def packets(page, files):
    page.evaluate(HARNESS, ["packets", files, {}, None])
    page.wait_for_selector(".tp-box tr.tp-row")
    rows = page.locator(".tp-box tr.tp-row").count()
    check(rows == 35, f"packet list shows all 35 phish packets ({rows})")
    page.fill('[data-r="f"]', "http.request and ip.addr == 10.20.0.14")
    page.click('[data-r="go"]')
    check(page.locator(".tp-box tr.tp-row").count() == 2, "display filter narrows the list to the 2 HTTP requests")
    page.locator(".tp-box tr.tp-row").first.click()
    tree = page.inner_text('[data-r="tree"]')
    check("Hypertext Transfer Protocol" in tree and "GET /invoices/INV-30412.docm" in tree, "packet details show the HTTP layer")
    hexv = page.inner_text('[data-r="hex"]')
    raw = "".join(l[6:55].replace(" ", "") for l in hexv.splitlines())
    check(hexv.startswith("0000  02 00") and "474554202f696e766f69636573" in raw, "hex pane shows the frame bytes, including GET /invoices")
    page.fill('[data-r="f"]', "htttp")
    page.click('[data-r="go"]')
    check("doesn't work" in page.inner_text('[data-r="msg"]'), "a bad filter is refused with a message")
    page.fill('[data-r="f"]', "dns")
    page.click('[data-r="go"]')
    page.click('[data-v="dns"]')
    check("cdn-update-check.net" in page.inner_text('[data-r="body"]'), "DNS view lists the queried names")
    page.click('[data-v="http"]')
    page.fill('[data-r="f"]', "")
    page.click('[data-r="go"]')
    body = page.inner_text('[data-r="body"]')
    check("/s2.bin" in body and "200 OK" in body, "HTTP view pairs requests with responses")
    page.click('[data-v="conv"]')
    check("198.51.100.140" in page.inner_text('[data-r="body"]'), "Conversations view lists the C2 address")
    page.fill('[data-r="f"]', "smb2")
    page.click('[data-r="go"]')
    page.click('[data-v="list"]')
    page.locator(".tp-box tr.tp-row").first.click()
    page.click("[data-follow]")
    stream = page.inner_text('[data-r="stream"]')
    check("Tree Connect Request" in stream and "kestrel-locked" in stream, "Follow stream shows the SMB conversation")
    page.fill('[data-r="f"]', "http.request")
    page.click('[data-r="go"]')
    page.click('[data-v="list"]')
    page.click('[data-r="save"]')
    rec = page.evaluate("window.REC")
    check(len(rec) == 1 and rec[0]["st"]["f"] == "http.request" and rec[0]["st"]["n"] == 2 and rec[0]["st"]["blank"] == ["f"], f"recording a filter makes a step ({rec and rec[0]['st']})")
    step = guided("packets", rec[0]["st"])
    page.evaluate(HARNESS, ["packets", files, step, None])
    page.wait_for_selector(".tp-box tr.tp-row")
    check(page.input_value('[data-r="f"]') == "", "Guided step hides the recorded filter")
    page.fill('[data-r="f"]', "http")
    page.click('[data-r="go"]')
    check("The recorded filter showed 2" in page.inner_text('[data-r="msg"]'), "a different answer is compared with the recording")
    page.click('[data-r="show"]')
    check(page.input_value('[data-r="f"]') == "http.request", "Show the recorded filter fills it in")
    page.click('[data-r="go"]')
    check("Same count as the recorded filter" in page.inner_text('[data-r="msg"]'), "the recorded answer matches")


def events(page, files):
    page.evaluate(HARNESS, ["events", files, {}, None])
    page.wait_for_selector(".te-box tr.te-row")
    logs = page.inner_text('[data-r="logs"]')
    check("Security" in logs and "System" in logs and "Application" in logs, "event viewer lists the three logs")
    page.fill('[data-r="ids"]', "4720-4732")
    page.click('[data-r="go"]')
    n = page.locator(".te-box tr.te-row").count()
    check(n == 2, f"ID range finds the new account and the group change ({n})")
    page.locator(".te-box tr.te-row").first.click()
    check("support_svc" in page.inner_text('[data-r="dbody"]'), "General tab shows the message")
    page.click('[data-t="xml"]')
    check("<EventID>4732</EventID>" in page.inner_text('[data-r="dbody"]'), "XML tab shows the event")
    page.click('[data-log="eventlogs/System.jsonl"]')
    page.fill('[data-r="ids"]', "")
    page.fill('[data-r="q"]', "Endpoint Protection")
    page.click('[data-r="go"]')
    check(page.locator(".te-box tr.te-row").count() >= 3, "text search finds the protection service changes")
    page.click('[data-log="eventlogs/Security.jsonl"]')
    page.fill('[data-r="q"]', "")
    page.fill('[data-r="ids"]', "4688")
    page.fill('[data-r="q"]', "svchost-upd")
    page.click('[data-r="go"]')
    n = page.locator(".te-box tr.te-row").count()
    page.click('[data-r="save"]')
    rec = page.evaluate("window.REC")
    check(len(rec) == 1 and rec[0]["st"]["ids"] == "4688" and rec[0]["st"]["n"] == n, f"recording an event filter makes a step ({n} events)")
    page.fill('[data-r="ids"]', "4699")
    page.click('[data-r="go"]')
    check("not an event ID" not in page.inner_text('[data-r="msg"]'), "an ID with no events is not an error")
    page.fill('[data-r="ids"]', "46x")
    page.click('[data-r="go"]')
    check("isn't an event ID" in page.inner_text('[data-r="msg"]'), "a bad ID list is refused")
    step = guided("events", rec[0]["st"])
    page.evaluate(HARNESS, ["events", files, step, None])
    page.wait_for_selector(".te-box tr.te-row")
    check(page.input_value('[data-r="ids"]') == "" and page.input_value('[data-r="q"]') == "", "Guided step hides the recorded filter")
    page.click('[data-r="show"]')
    page.click('[data-r="go"]')
    check("Same count as the recorded filter" in page.inner_text('[data-r="msg"]'), "the recorded event filter matches")


def proxy(page):
    page.evaluate(HARNESS, ["proxy", {}, {}, None])
    page.wait_for_selector('[data-px="toggle"]', timeout=60000)
    page.fill('[data-r="bp"]', "/api/products?q=key")
    page.click('[data-px="browse"]')
    check("answered 200" in page.inner_text('[data-r="msg"]'), "the proxy's browser reaches the simulated shop")
    page.click('[data-px="toggle"]')
    page.select_option('[data-r="bm"]', "POST")
    page.fill('[data-r="bp"]', "/api/login")
    page.fill('[data-r="bb"]', '{"email":"demo@nimbu.shop","password":"wrong"}')
    page.click('[data-px="browse"]')
    check(page.locator('[data-r="held"]').count() == 1, "with Intercept on, the request is held")
    held = page.input_value('[data-r="held"]').replace('"password":"wrong"', '"password":"demo123"')
    page.fill('[data-r="held"]', held)
    page.click('[data-px="forward"]')
    check("answered 200" in page.inner_text('[data-r="msg"]'), "an edited, forwarded request logs in")
    page.click('[data-px="toggle"]')
    page.click('[data-pv="history"]')
    rows = page.locator(".tx-box tr.tx-row").count()
    check(rows == 2, f"HTTP history shows both requests ({rows})")
    page.locator(".tx-box tr.tx-row").first.click()
    check("HTTP/1.1 200 OK" in page.inner_text('[data-r="hres"]'), "history shows the raw response")
    page.click('[data-px="torep2"]')
    rep = page.input_value('[data-r="rep"]')
    check(rep.startswith("POST /api/login HTTP/1.1"), "Send to Repeater copies the request")
    page.fill('[data-r="rep"]', "POST /api/login HTTP/1.1\nHost: nimbu.shop\nContent-Type: application/json\n\n{\"email\":\"admin@nimbu.shop' --\",\"password\":\"x\"}")
    page.click('[data-px="send"]')
    out = page.inner_text('[data-r="rout"]')
    check("HTTP/1.1 200 OK" in out and '"role": "admin"' in out, "Repeater sends the SQL injection login and gets admin")
    page.fill('[data-r="rep"]', "GET /api/orders/1 HTTP/1.1\nHost: nimbu.shop\nAuthorization: Bearer {{token}}\n\n")
    page.click('[data-px="send"]')
    check('"user_id": 1' in page.inner_text('[data-r="rout"]'), "{{token}} reuses the last login token")
    page.click('[data-px="save"]')
    rec = page.evaluate("window.REC")
    st = rec[0]["st"] if rec else {}
    check(st.get("m") == "GET" and st.get("p") == "/api/orders/1" and "{{token}}" in st.get("h", "") and st.get("s") == 200, f"recording a Repeater request makes a step ({st})")
    login = {"m": "POST", "p": "/api/login", "h": "Content-Type: application/json", "b": "{\"email\":\"admin@nimbu.shop' --\",\"password\":\"x\"}", "s": 200, "blank": ["p", "b"]}
    step = guided("proxy", login)
    page.evaluate(HARNESS, ["proxy", {}, step, None])
    page.wait_for_selector('[data-r="rep"]', timeout=60000)
    rep = page.input_value('[data-r="rep"]')
    check(rep.startswith("POST ___ HTTP/1.1") and "admin@" not in rep, "Guided step hides the path and body")
    page.click('[data-px="send"]')
    check("Fill in the ___ blanks" in page.inner_text('[data-r="msg"]'), "blanks must be filled first")
    page.click('[data-px="show"]')
    page.click('[data-px="send"]')
    check("Same status as the recorded request" in page.inner_text('[data-r="msg"]'), "the recorded request gets the same status")


def notebook_console(browser, base):
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base + "/notebook.html?ref=rb-phish&runbook=phish")
    page.wait_for_selector("#pb-dock", state="attached", timeout=60000)
    page.wait_for_function("document.querySelectorAll('#nb-cells .nb-cell').length > 5", timeout=60000)
    names = page.eval_on_selector_all("#pb-dock [data-tab]", "bs => bs.map(b => b.textContent.trim())")
    check(all(n in names for n in ("Log search", "Packet viewer", "Web proxy", "Event viewer")), f"the analyst console has a tab for each tool ({names})")
    for tab, sel in (("tool-packets", "#pb-p-tool-packets tr.tp-row"), ("tool-events", "#pb-p-tool-events tr.te-row"), ("tool-proxy", '#pb-p-tool-proxy [data-px="toggle"]')):
        page.evaluate("t => document.querySelector('#pb-dock [data-tab=\"' + t + '\"]').click()", tab)
        try:
            page.wait_for_selector(sel, timeout=60000)
            check(True, f"console tab {tab} loads the case")
        except Exception as e:
            check(False, f"console tab {tab} loads the case ({e.__class__.__name__})")
    page.evaluate("document.querySelector('#pb-dock [data-tab=\"tool-packets\"]').click()")
    p = "#pb-p-tool-packets "
    page.fill(p + '[data-r="f"]', "dns.qry.name contains cdn")
    page.click(p + '[data-r="go"]')
    page.click(p + '[data-r="save"]')
    page.evaluate("document.querySelector('#pb-dock [data-tab=\"tool-events\"]').click()")
    p = "#pb-p-tool-events "
    page.fill(p + '[data-r="ids"]', "4698")
    page.click(p + '[data-r="go"]')
    page.click(p + '[data-r="save"]')
    try:
        page.wait_for_selector('#nb-cells .tool-step[data-tool="packets"] tr.tp-row', timeout=30000)
        page.wait_for_selector('#nb-cells .tool-step[data-tool="events"] tr.te-row', timeout=30000)
        check(True, "Add to notebook puts runnable Packet viewer and Event viewer steps in the notebook")
    except Exception as e:
        check(False, f"Add to notebook puts runnable steps in the notebook ({e.__class__.__name__})")
    step = '#nb-cells .tool-step[data-tool="events"] '
    if page.locator(step + '[data-r="go"]').count():
        page.click(step + '[data-r="go"]')
        check("Same count as the recorded filter" in page.inner_text(step + '[data-r="msg"]'), "the notebook step runs and matches its recording")
    check(not errors, f"no page errors on the notebook ({errors[:3]})")
    page.close()


def shop_page(browser, base):
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    config = (SITE / "assets" / "config.js").read_text(encoding="utf-8") + "\nif (window.APCYBER_PAYWALL) window.APCYBER_PAYWALL.enabled = false;\n"
    page.route("**/assets/config.js", lambda route: route.fulfill(status=200, content_type="application/javascript", body=config))
    page.goto(base + "/shop.html")
    page.wait_for_selector(".sh-grid", timeout=60000)
    page.click('.sh-tabs [data-tab="proxy"]')
    page.wait_for_selector('[data-px="toggle"]')
    check("In front of nimbu.shop" in page.inner_text(".tx-box .tl-head"), "the shop's Proxy tab sits in front of the page")
    page.click('[data-px="toggle"]')
    page.fill("#sh-url", "/#/login")
    page.click("#sh-goto")
    page.fill('form[data-login] input[name="email"]', "demo@nimbu.shop")
    page.fill('form[data-login] input[name="password"]', "nope")
    page.click('form[data-login] button')
    page.wait_for_selector('[data-r="held"]')
    held = page.input_value('[data-r="held"]')
    check(held.startswith("POST /api/login HTTP/1.1") and "nope" in held, "Intercept catches the page's login request")
    page.fill('[data-r="held"]', held.replace('"email":"demo@nimbu.shop"', '"email":"admin@nimbu.shop\' --"'))
    page.click('[data-px="forward"]')
    page.wait_for_timeout(300)
    check("admin@nimbu.shop" in page.inner_text("#sh-page"), "forwarding the edited request logs the page in as admin")
    check(page.locator("#lk-toast").count() == 1 and "Log in as the admin" in page.inner_text("#lk-toast"), "the shop awards the SQL injection flag")
    page.click('[data-px="toggle"]')
    page.click('[data-pv="history"]')
    check(page.locator(".tx-box tr.tx-row").count() >= 2, "history includes the page's own requests")
    page.click('.sh-tabs [data-tab="net"]')
    check(page.locator(".sh-reqs button").count() >= 2, "the shop's Network tab still works")
    check(not errors, f"no page errors on the shop ({errors[:3]})")
    page.close()


def tiny_pcap():
    def frame(src, dst, proto, sp, dp, payload):
        if proto == 6:
            l4 = struct.pack(">HHIIBBHHH", sp, dp, 1, 1, 0x50, 0x18, 65535, 0, 0)
        else:
            l4 = struct.pack(">HHHH", sp, dp, 8 + len(payload), 0)
        ip = struct.pack(">BBHHHBBH4s4s", 0x45, 0, 20 + len(l4) + len(payload), 1, 0, 64, proto, 0, bytes(map(int, src.split("."))), bytes(map(int, dst.split("."))))
        return b"\x02\x00\x00\x00\x00\x01\x02\x00\x00\x00\x00\x02\x08\x00" + ip + l4 + payload
    dns = struct.pack(">HHHHHH", 0x1234, 0x0100, 1, 0, 0, 0) + b"\x04demo\x07example\x00\x00\x01\x00\x01"
    pkts = [frame("192.0.2.10", "192.0.2.53", 17, 50000, 53, dns),
            frame("192.0.2.10", "198.51.100.7", 6, 50001, 80, b"GET /login HTTP/1.1\r\nHost: demo.example\r\nUser-Agent: curl/8.5\r\n\r\n")]
    out = struct.pack("<IHHiIII", 0xa1b2c3d4, 2, 4, 0, 0, 65535, 1)
    for i, p in enumerate(pkts):
        out += struct.pack("<IIII", 1762160000 + i, 0, len(p), len(p)) + p
    return out


def studio(browser, tmp):
    from tools.studio import server as SV
    work = Path(tmp)
    for p in (SITE / CASE).rglob("*"):
        if p.is_file():
            dest = work / p.relative_to(SITE / CASE)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(p.read_bytes())
    (work / "live.pcap").write_bytes(tiny_pcap())
    fake = type("F", (), {})()
    fake.session = type("S", (), {"work": work})()
    feed = SV.App.case_files(fake)
    got = json.loads(feed)
    check(got.get("live.pcap", "").startswith("#aayat-capture") and "GET /login" in got["live.pcap"], "the studio converts a real .pcap for the packet viewer")
    check(got.get("capture.pcap", "").startswith("#aayat-capture"), "the studio passes a lab capture through unchanged")
    check("eventlogs/Security.jsonl" in got, "the studio feeds event logs to the tools")

    class Studio(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_GET(self):
            path = self.path.split("?", 1)[0]
            if path == "/case-files":
                return self.reply(feed, "application/json")
            for prefix, base in (("/ui/", SV.UI), ("/xterm/", SV.XTERM), ("/site/", SITE)):
                if path.startswith(prefix):
                    f = base / path[len(prefix):]
                    return self.reply(f.read_bytes(), "application/javascript" if f.suffix == ".js" else "text/css" if f.suffix == ".css" else "application/wasm" if f.suffix == ".wasm" else "text/html") if f.is_file() else self.send_error(404)
            if path == "/":
                return self.reply((SV.UI / "index.html").read_bytes(), "text/html")
            self.send_error(404)

        def reply(self, body, kind):
            self.send_response(200)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    with socketserver.ThreadingTCPServer(("127.0.0.1", 0), Studio) as srv:
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{srv.server_address[1]}"
        page = browser.new_page()
        errors, sent = [], []
        page.on("pageerror", lambda e: errors.append(str(e)))

        def ws(route):
            route.on_message(lambda m: sent.append(m) if isinstance(m, str) else None)
        page.route_web_socket("**/ws*", ws)
        page.goto(base + "/?t=test")
        page.wait_for_selector("#toolbtns button")
        names = page.eval_on_selector_all("#toolbtns button", "bs => bs.map(b => b.textContent)")
        check(all(n in names for n in ("Log search", "Packet viewer", "Web proxy", "Event viewer")), f"the studio's Tools list has every tool ({names})")
        page.click("#toolbtns button:has-text('Packet viewer')")
        page.wait_for_selector("#toolbody tr.tp-row")
        check(page.eval_on_selector_all("#toolbody [data-r=file] option", "os => os.map(o => o.value)") == ["capture.pcap", "live.pcap"], "the packet viewer offers both captures in the studio")
        page.select_option("#toolbody [data-r=file]", "live.pcap")
        page.fill("#toolbody [data-r=f]", "http.request")
        page.click("#toolbody [data-r=go]")
        page.click("#toolbody [data-r=save]")
        page.click("#toolbox button.primary")
        page.click("#toolbtns button:has-text('Event viewer')")
        page.wait_for_selector("#toolbody tr.te-row")
        page.fill("#toolbody [data-r=ids]", "4720")
        page.click("#toolbody [data-r=go]")
        page.click("#toolbody [data-r=save]")
        page.click("#toolbox button.primary")
        page.click("#toolbtns button:has-text('Web proxy')")
        page.wait_for_selector("#toolbody [data-pv=repeat]", timeout=60000)
        page.click("#toolbody [data-pv=repeat]")
        page.fill("#toolbody [data-r=rep]", "GET /robots.txt HTTP/1.1\nHost: nimbu.shop\n\n")
        page.click("#toolbody [data-px=send]")
        page.click("#toolbody [data-px=save]")
        page.wait_for_timeout(300)
        msgs = [json.loads(m) for m in sent if '"k": "tool"' in m or '"k":"tool"' in m]
        tools = [m["tool"] for m in msgs]
        check(tools == ["packets", "events", "proxy"], f"each tool records itself into the studio session ({tools})")
        if len(msgs) == 3:
            check(msgs[0]["state"]["file"] == "live.pcap" and msgs[0]["state"]["n"] == 1, "the recorded packet step names the live capture and its count")
            check(msgs[2]["state"]["p"] == "/robots.txt" and msgs[2]["state"]["s"] == 200, "the recorded proxy step keeps the request and status")
            cells = [{"t": "md", "s": T.fence(m["tool"], m["state"])} for m in msgs]
            problems = T.count_problems(cells, {k: v for k, v in got.items()})
            check(not problems, f"the compiled steps find their files ({problems})")
        check(not errors, f"no page errors in the studio ({errors[:3]})")
        page.close()
        srv.shutdown()


def main():
    from playwright.sync_api import sync_playwright
    sys.stdout.reconfigure(encoding="utf-8")
    handler = functools.partial(Quiet, directory=str(SITE))
    with socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler) as server:
        base = f"http://127.0.0.1:{server.server_address[1]}"
        threading.Thread(target=server.serve_forever, daemon=True).start()
        files = {"capture.pcap": (SITE / CASE / "capture.pcap").read_text(encoding="utf-8"), "proxy.log": (SITE / CASE / "proxy.log").read_text(encoding="utf-8")}
        for n in ("Security", "System", "Application"):
            files[f"eventlogs/{n}.jsonl"] = (SITE / CASE / "eventlogs" / f"{n}.jsonl").read_text(encoding="utf-8")
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page, errors = blank_page(browser, base)
            print("Packet viewer")
            packets(page, files)
            print("Event viewer")
            events(page, files)
            print("Web proxy")
            proxy(page)
            check(not errors, f"no page errors in the tools ({errors[:3]})")
            page.close()
            print("Notebook console")
            notebook_console(browser, base)
            print("Hack the shop")
            shop_page(browser, base)
            print("Teaching studio")
            with tempfile.TemporaryDirectory() as tmp:
                studio(browser, tmp)
            browser.close()
        server.shutdown()
    print(f"\n{len(FAILS)} failed" if FAILS else "\nall passed")
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
