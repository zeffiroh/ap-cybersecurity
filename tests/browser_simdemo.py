import functools
import http.server
import socketserver
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
from browser_bench import LABS, Quiet, SITE, check, FAILS

SIMS = ["x01-phish-to-containment", "x02-authorised-pen-test", "x03-secure-a-small-office", "x04-ransomware-night-shift", "x05-cloud-bucket-left-open"]


def play(browser, base, name, speed=40):
    page = browser.new_page(viewport={"width": 1500, "height": 950})
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.add_init_script(LABS)
    began = time.time()
    page.goto(f"{base}/workstation.html?case=sem-{name}&sim=walk&demo=1&speed={speed}")
    page.wait_for_function("window.__demo && window.__demo.done", timeout=900000, polling=1000)
    r = page.evaluate("window.__demo")
    took = time.time() - began
    check(not r.get("error"), f"{name}: the demo plays to the end ({r.get('error') or 'ok'}, {took:.0f}s)")
    check(not r.get("open"), f"{name}: every objective is met by the demo's own moves (still open: {r.get('open')})")
    chapters = [x["chapter"] for x in r.get("log", []) if x.get("chapter")]
    check(len(chapters) >= 4 and chapters[-1] == "Debrief", f"{name}: chapters for the video ({', '.join(chapters)})")
    check(page.locator(".sm-over h2").count() == 1, f"{name}: the debrief is on screen at the end")
    check(not errors, f"{name}: no page errors ({errors[:3]})")
    page.close()


def main(names=None):
    from playwright.sync_api import sync_playwright
    handler = functools.partial(Quiet, directory=str(SITE))
    with socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler) as server:
        base = f"http://127.0.0.1:{server.server_address[1]}"
        threading.Thread(target=server.serve_forever, daemon=True).start()
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for name in names or SIMS:
                print(name)
                try:
                    play(browser, base, name)
                except Exception as e:
                    check(False, f"{name} ran without an exception ({e.__class__.__name__}: {str(e)[:300]})")
            browser.close()
        server.shutdown()
    print(f"\n{len(FAILS)} failed" if FAILS else "\nall passed")
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:] or None))
