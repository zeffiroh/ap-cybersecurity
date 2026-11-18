import functools
import http.server
import os
import socketserver
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
SHOTS = Path(os.environ.get("BENCH_SHOTS", "")) if os.environ.get("BENCH_SHOTS") else None
FAILS = []

LABS = """(() => {
  let real;
  const fake = (r) => new Proxy(r || {}, { get: (t, k) => k === 'has' ? (() => true) : t[k] });
  Object.defineProperty(window, 'Paywall', { configurable: true, get: () => fake(real), set: (v) => { real = v; } });
})();"""


class Quiet(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, ".js": "text/javascript", ".wasm": "application/wasm"}

    def log_message(self, *a):
        pass


def check(ok, what):
    print(("  ok    " if ok else "  FAIL  ") + what)
    if not ok:
        FAILS.append(what)


def shot(page, name):
    if SHOTS:
        SHOTS.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(SHOTS / (name + ".png")))


def desk(browser, base, case, level=None):
    page = browser.new_page(viewport={"width": 1500, "height": 950})
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.add_init_script(LABS)
    page.goto(f"{base}/workstation.html?case={case}")
    page.wait_for_selector(".ws-signbtn", timeout=30000)
    page.click(".ws-signbtn")
    page.wait_for_function("(c) => window.AayatDesk && AayatDesk.caseId() === c && AayatDesk.caseMeta()", arg=case, timeout=30000)
    page.wait_for_timeout(600)
    pick = page.query_selector(f"[data-lv={level}]" if level else "[data-skip]")
    if pick:
        pick.click()
    page.evaluate("() => document.querySelectorAll('.ws-win [data-w=close]').forEach(b => { if (!/Mission/.test(b.closest('.ws-win').innerText.slice(0, 80))) b.click(); })")
    return page, errors


def term_run(page, win, cmd):
    inp = win.locator("form input").last
    inp.fill(cmd)
    inp.press("Enter")
    page.wait_for_timeout(120)
    return win.locator("pre").last.inner_text()


def clinic(browser, base):
    page, errors = desk(browser, base, "sem-x03-secure-a-small-office", "walk")
    page.wait_for_selector('[data-ask="rogue"] input', timeout=20000)
    page.fill('[data-ask="rogue"] input', "10.40.0.99")
    page.press('[data-ask="rogue"] input', "Enter")
    page.wait_for_timeout(300)
    page.evaluate("() => AayatDesk.run('bench')")
    page.wait_for_selector(".hb-dev[data-dev=sw1]", timeout=20000)
    page.wait_for_timeout(300)
    n = page.locator(".hb-dev").count()
    wires = page.locator(".hb-wires path").count()
    check(n == 12, f"the clinic bench shows every device and the internet ({n})")
    check(wires >= 14, f"cables are drawn between sockets, ports and devices ({wires})")
    check(page.locator(".hb-tasks li").count() == 6 and page.locator(".hb-tasks li.ok").count() == 1, "the work order lists 6 jobs, only 'the clinic still works' done at the start")
    shot(page, "bench-clinic")

    page.click('.hb-sock[data-port="sw1:9"]')
    page.wait_for_selector('.hb-panel [data-a="unplug"]')
    check("waiting room" in page.inner_text(".hb-panel") and "TL-WR840N" in page.inner_text(".hb-panel"), "wall socket W1 shows its room and the rogue device")
    page.click('.hb-panel [data-a="unplug"]')
    page.wait_for_timeout(300)
    check(page.locator(".hb-tasks li.ok").count() == 2, "pulling W1's cable ticks 'take the device off the network'")
    check("No network at all: TL-WR840N" in page.inner_text(".hb-impact"), "'Compared with the start' says what broke")

    page.click('.hb-dev[data-dev=sw1]')
    page.click('.hb-panel [data-a="con"]')
    con = page.locator(".ws-win", has_text="sw1 console").last
    con.wait_for()
    for c in ["enable", "configure terminal", "interface range fa0/7, fa0/11", "shutdown", "end"]:
        term_run(page, con, c)
    out = term_run(page, con, "show interfaces status")
    check("Fa0/7     consult room 3     disabled" in out, "the switch console shuts ports with real commands")
    check(page.locator(".hb-tasks li.ok").count() == 3, "shutting fa0/7 and fa0/11 ticks the empty-rooms job")
    shot(page, "bench-console")
    con.locator("[data-w=close]").click()

    page.click('.hb-dev[data-dev=gw]')
    page.fill('.hb-panel [data-k="rules"]', "zone clinic 10.40.0.0/24\nzone guest 10.40.1.0/24\nzone internet any\nallow any clinic -> any\nallow udp guest -> 10.40.0.1:53\nallow tcp guest -> internet:80,443\ndeny any guest -> clinic\ndefault deny\n")
    page.click('.hb-panel [data-a="rules"]')
    page.wait_for_timeout(300)
    check(page.locator(".hb-tasks li.ok").count() == 4, "new router rules keep guests away from nas01")

    page.click('.hb-dev[data-dev="recep-pc"]')
    page.click('.hb-panel [data-a="usb"]')
    page.wait_for_timeout(200)
    page.click('.hb-dev[data-dev="recep-pc"]')
    page.click('.hb-panel [data-a="desk"]')
    page.wait_for_selector(".wm-icons [data-app=cmd]")
    page.dblclick(".wm-icons [data-app=cmd]")
    cmd = page.locator(".wm-win", has_text="Command Prompt").last
    cmd.wait_for()
    out = term_run(page, cmd, "ping nas01")
    check("Reply from 10.40.0.10: bytes=32" in out, "recep-pc's own Command Prompt pings nas01 through the bench wiring")
    out = term_run(page, cmd, "tracert 198.51.100.1")
    check("gw.saffron.lan [10.40.0.1]" in out and "Trace complete." in out, "tracert goes through the clinic router")
    shot(page, "machine-bench")

    page.locator(".ws-win", has_text="RECEP-PC").last.locator("[data-w=close]").first.click()
    page.check('.hb-door [data-door]')
    page.wait_for_timeout(300)
    check(page.locator(".hb-tasks li.ok").count() == 6, "after USB and the rack lock, the whole work order is done")
    run = page.evaluate("() => JSON.parse(localStorage.getItem('ws-sim-run-sem-x03-secure-a-small-office') || '{}')")
    done = sorted((run.get("done") or {}).keys())
    check(all(k in done for k in ["rogue", "cut", "usb"]), f"the simulation counts the bench work as objectives ({done})")

    page.evaluate("() => AayatDesk.run('rack')")
    page.wait_for_selector("[data-view=patch]")
    page.click("[data-view=patch]")
    page.wait_for_selector(".pp-col")
    check(page.locator(".pp-col").count() == 12, "the Server room's patch panel shows the switch's 12 ports")
    check(page.locator('.pp-col[data-port="sw1:9"] .pp-cable.out').count() == 1 and page.locator('.pp-col.s-disabled').count() == 3, "the patch panel shows W1 unplugged and three shut ports")
    check(page.is_checked(".rk-bar [data-r=door]"), "the Server room's rack door shares the bench's lock")
    shot(page, "patch-panel")

    page.evaluate("() => AayatDesk.run('bench', { bench: 'practice:router-on-a-stick' })")
    page.wait_for_function("() => [...document.querySelectorAll('.hb-bar select')].some(s => s.value === 'practice:router-on-a-stick') && document.querySelector('.hb-dev[data-dev=r1]')", timeout=20000)
    hb = page.locator(".hb").last
    check(hb.locator(".hb-tasks li").count() == 5 and hb.locator(".hb-tasks li.ok").count() == 0, "a practice bench opens with its own work order")
    shot(page, "bench-practice")
    check(not errors, f"no page errors on the bench ({errors[:3]})")
    page.close()


def ransom(browser, base):
    page, errors = desk(browser, base, "sem-x04-ransomware-night-shift")
    page.evaluate("() => AayatDesk.run('rdp')")
    page.wait_for_selector(".rd-host[data-h=fs02]", timeout=20000)
    page.click(".rd-host[data-h=fs02]")
    page.wait_for_selector(".wm-icons")
    page.dblclick(".wm-icons [data-app=services]")
    svc = page.locator(".wm-win", has_text="Display name").last
    svc.wait_for()
    check("WinUpdSvc" in svc.inner_text(), "Services lists the service the attacker installed (from event 7045)")
    page.dblclick(".wm-icons [data-app=cmd]")
    cmd = page.locator(".wm-win", has_text="Command Prompt").last
    cmd.wait_for()
    out = term_run(page, cmd, "sc stop WinUpdSvc")
    check("STOP_PENDING" in out, "sc stop works on the evidence machine")
    ev = page.evaluate("() => JSON.parse(localStorage.getItem('ws-rd-act-sem-x04-ransomware-night-shift') || '{}')")
    check((ev.get("fs02") or {}).get("svc", {}).get("WinUpdSvc") == "stop", "stopping a service is remembered for the debrief")
    page.click(".rd-host, .wm-start") if page.query_selector(".rd-host") else None
    page.evaluate("() => document.querySelectorAll('.ws-win [data-w=close]').forEach(b => b.click())")
    page.evaluate("() => AayatDesk.run('rdp')")
    page.wait_for_selector(".rd-host[data-h=eng-ws14]")
    page.click(".rd-host[data-h=eng-ws14]")
    page.wait_for_selector(".wm-win .wm-tabs")
    tm = page.locator(".wm-win", has_text="Processes").last
    check(tm.locator("tr").count() > 5, f"Task Manager opens with the captured process tree ({tm.locator('tr').count()} rows)")
    tm.locator("[data-t=users]").click()
    check("s.kale" in tm.inner_text().lower(), "the Users tab lists sign-ins from the Security log")
    page.dblclick(".wm-icons [data-app=eventvwr]")
    evw = page.locator(".wm-win", has_text="Open in the Event viewer program").last
    evw.wait_for()
    evw.locator("tr[data-i]").first.click()
    check(len(evw.locator(".wm-msg").inner_text()) > 20, "Event Viewer shows an event's message inside the remote desktop")
    page.dblclick(".wm-icons [data-app=ps]")
    ps = page.locator(".wm-win", has_text="Windows PowerShell").last
    ps.wait_for()
    out = term_run(page, ps, "Get-Process")
    check("ProcessName" in out and "explorer" in out, "PowerShell's Get-Process prints a table")
    page.dblclick(".wm-icons [data-app=explorer]")
    ex = page.locator(".wm-win", has_text="This PC").last
    ex.wait_for()
    ex.locator(".wm-addr input").fill("C:\\Users")
    ex.locator(".wm-addr input").press("Enter")
    page.wait_for_timeout(150)
    check("s.kale" in ex.locator(".wm-list").inner_text(), "File Explorer builds C:\\Users from the evidence")
    shot(page, "machine-evidence")
    check(not errors, f"no page errors on the remote desktop ({errors[:3]})")
    page.close()


def linux(browser, base):
    page, errors = desk(browser, base, "miner")
    page.evaluate("() => AayatDesk.run('rdp')")
    page.wait_for_selector(".rd-host[data-l=build01]", timeout=20000)
    check("Linux" in page.inner_text(".rd-host[data-l=build01]"), "the Remote desktop lists the Linux build server")
    page.click(".rd-host[data-l=build01]")
    page.wait_for_selector(".wm-lin .wm-icons [data-app=term]")
    mon = page.locator(".wm-win", has_text="System Monitor").last
    mon.wait_for()
    check("kswapd0" in mon.inner_text(), "System Monitor opens with the captured ps output, miner included")
    mon.locator("[data-t=net]").click()
    check("3333" in mon.inner_text(), "the Connections tab shows the miner's pool connection from ss.txt")
    page.dblclick(".wm-icons [data-app=term]")
    term = page.locator(".wm-win", has_text="analyst@build01").last
    term.wait_for()
    out = term_run(page, term, "cat /etc/cron.d/sysupdate")
    check("curl" in out, "cat reads the saved cron file at its real path")
    out = term_run(page, term, "systemctl status sysupdate")
    check("System update helper" in out and "active (running)" in out, "systemctl status reads the unit file from the case")
    term_run(page, term, "sudo systemctl disable --now sysupdate")
    out = term_run(page, term, "crontab -r -u root")
    act = page.evaluate("() => JSON.parse(localStorage.getItem('ws-lx-act-miner') || '{}')")
    b = act.get("build01") or {}
    check(b.get("units", {}).get("sysupdate.service") == "both", f"disable --now stops and disables the unit ({b.get('units')})")
    check(len(b.get("cron", {})) >= 1, "crontab -r removes root's cron line and remembers it")
    page.dblclick(".wm-icons [data-app=units]")
    sv = page.locator(".wm-win", has_text="systemd services").last
    sv.wait_for()
    check("inactive (dead)" in sv.inner_text() and "Removed" in sv.inner_text(), "the Services window shows the stopped unit and the removed cron job")
    page.dblclick(".wm-icons [data-app=files]")
    fl = page.locator(".wm-win", has_text="Places").last
    fl.wait_for()
    fl.locator(".wm-addr input").fill("/var/tmp/.cache")
    fl.locator(".wm-addr input").press("Enter")
    page.wait_for_timeout(150)
    check("kswapd0" in fl.locator(".wm-list").inner_text(), "Files builds /var/tmp/.cache from the evidence")
    fl.locator("tr[data-file]", has_text="kswapd0").click()
    check("strings" in fl.locator(".wm-props").inner_text(), "a binary with no copy points to its saved strings")
    shot(page, "machine-linux")
    check(not errors, f"no page errors on the Linux desktop ({errors[:3]})")
    page.close()

    page, errors = desk(browser, base, "phish")
    page.evaluate("() => AayatDesk.run('rdp')")
    page.wait_for_selector(".rd-host[data-h=hr-pc07]", timeout=20000)
    page.click(".rd-host[data-h=hr-pc07]")
    page.wait_for_selector(".wm-icons [data-app=explorer]")
    page.dblclick(".wm-icons [data-app=explorer]")
    ex = page.locator(".wm-win", has_text="This PC").last
    ex.wait_for()
    ex.locator(".wm-addr input").fill("C:\\Users\\Public")
    ex.locator(".wm-addr input").press("Enter")
    page.wait_for_timeout(150)
    ex.locator("tr[data-file]", has_text="upd.ps1").click()
    ex.locator('[data-a="note"]').click()
    np = page.locator(".wm-win", has_text="Notepad").last
    np.wait_for()
    check("DownloadFile" in np.inner_text() and "4104" in np.inner_text(), "Notepad shows upd.ps1 rebuilt from the script-block log")
    page.dblclick(".wm-icons [data-app=cmd]")
    cmd = page.locator(".wm-win", has_text="Command Prompt").last
    cmd.wait_for()
    out = term_run(page, cmd, "type C:\\Users\\Public\\svchost-upd.exe")
    check("binary data" in out and "strings" in out, "type on a program says it's binary and points to the saved strings")
    check(not errors, f"no page errors on the phishing remote desktop ({errors[:3]})")
    page.close()

    page, errors = desk(browser, base, "trial")
    page.evaluate("() => AayatDesk.run('bench')")
    page.wait_for_selector(".hb-dev[data-dev=portal01]", timeout=20000)
    page.wait_for_timeout(300)
    check(page.locator(".hb-tasks li").count() == 3, "the trial bench has its own work order")
    page.click(".hb-dev[data-dev=portal01]")
    page.click('.hb-panel [data-a="desk"]')
    page.wait_for_selector(".wm-lin .wm-icons [data-app=term]")
    page.dblclick(".wm-icons [data-app=term]")
    term = page.locator(".wm-win", has_text="@portal01").last
    term.wait_for()
    out = term_run(page, term, "ping -c 2 198.51.100.1")
    check("2 packets transmitted, 2 received" in out, "a Linux machine on the bench pings through the wiring from its own desktop")
    shot(page, "bench-linux")
    check(not errors, f"no page errors on the trial bench ({errors[:3]})")
    page.close()


def ticket_view(page):
    page.evaluate("() => AayatDesk.run('tickets')")
    win = page.locator(".ws-win", has_text="Export CSV").last
    win.wait_for()
    page.wait_for_selector(".tk-list tr[data-id]", timeout=20000)
    row = win.locator(".tk-list tr[data-id]", has=page.locator(".sev.critical")).first
    row.click()
    page.wait_for_selector(".tk-meta")
    return win.locator(".ws-status").inner_text(), win.locator(".tk-meta").inner_text(), row.locator("td").last.inner_text()


def sla(browser, base):
    page, errors = desk(browser, base, "sem-x04-ransomware-night-shift")
    stat, meta, left = ticket_view(page)
    check("this case's SLA" in stat, f"Tickets says the ransomware case uses its own SLA ({stat})")
    check("30m for critical" in meta and "retainer" in meta, "a critical ticket shows the case's 30-minute target and why")
    check(left.startswith(("29m", "30m")), f"the critical ticket's clock counts down from 30 minutes ({left})")
    check(not errors, f"no page errors in Tickets with a case SLA ({errors[:3]})")
    page.close()
    page, errors = desk(browser, base, "phish")
    stat, meta, left = ticket_view(page)
    check("standard SLA" in stat and "15m for critical (standard SLA)" in meta, f"a case without an SLA keeps the standard 15 minutes ({stat})")
    check(not errors, f"no page errors in Tickets with the standard SLA ({errors[:3]})")
    page.close()


def main():
    from playwright.sync_api import sync_playwright
    handler = functools.partial(Quiet, directory=str(SITE))
    with socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler) as server:
        base = f"http://127.0.0.1:{server.server_address[1]}"
        threading.Thread(target=server.serve_forever, daemon=True).start()
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for name, fn in (("Hardware bench and Server room", clinic), ("Remote desktop", ransom), ("Linux desktop and evidence files", linux), ("Ticket SLA per case", sla)):
                print(name)
                try:
                    fn(browser, base)
                except Exception as e:
                    check(False, f"{name} ran without an exception ({e.__class__.__name__}: {str(e)[:300]})")
            browser.close()
        server.shutdown()
    print(f"\n{len(FAILS)} failed" if FAILS else "\nall passed")
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
