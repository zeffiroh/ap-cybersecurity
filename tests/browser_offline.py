import functools
import http.server
import socketserver
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
FAILS = []


class Quiet(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, ".js": "text/javascript", ".mjs": "text/javascript",
                      ".wasm": "application/wasm", ".whl": "application/octet-stream"}

    def log_message(self, *a):
        pass


def check(ok, what):
    print(("  ok    " if ok else "  FAIL  ") + what)
    if not ok:
        FAILS.append(what)


def watch(page, base):
    outside = []

    def seen(req):
        u = req.url
        if not u.startswith((base, "data:", "blob:")) and ".neon.tech/" not in u:
            outside.append(u)
    page.on("request", seen)
    return outside


def notebook_python(browser, base):
    page = browser.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    outside = watch(page, base)
    page.goto(base + "/notebook.html?ref=offline-test")
    page.wait_for_selector("#nb-addpy")
    page.click("#nb-addpy")
    page.wait_for_selector(".nb-cell .CodeMirror", timeout=30000)
    check(True, "the code editor loads from the site")
    code = "import pandas as pd, yaml, hashlib\nprint(pd.DataFrame({'a':[1,2,3]}).a.sum(), yaml.safe_load('k: 7')['k'], hashlib.sha256(b'x').hexdigest()[:8])"
    page.evaluate("c => { const e = [...document.querySelectorAll('.nb-cell .CodeMirror')].pop(); e.CodeMirror.setValue(c); }", code)
    page.locator(".nb-cell [data-run]").last.click()
    try:
        page.wait_for_function("[...document.querySelectorAll('.nb-cell .nb-out')].some(o => /6 7 2d711642/.test(o.textContent))", timeout=180000)
        check(True, "Python with pandas and PyYAML runs from the site's own copy")
    except Exception as e:
        out = page.eval_on_selector_all(".nb-cell .nb-out", "os => os.map(o => o.textContent).join(' | ')")
        check(False, f"Python runs from the site's own copy ({e.__class__.__name__}: {out[:300]})")
    check(not outside, f"no requests leave the site ({outside[:4]})")
    check(not errors, f"no page errors ({errors[:3]})")
    page.close()


def linux_page(browser, base):
    page = browser.new_page()
    outside = watch(page, base)
    page.goto(base + "/linux.html")
    page.wait_for_function("!!window.Terminal", timeout=30000)
    check(True, "the Linux lab's terminal library loads from the site")
    check(not outside, f"no requests leave the Linux lab page ({outside[:4]})")
    page.close()


def main():
    from playwright.sync_api import sync_playwright
    sys.stdout.reconfigure(encoding="utf-8")
    handler = functools.partial(Quiet, directory=str(SITE))
    with socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler) as server:
        base = f"http://127.0.0.1:{server.server_address[1]}"
        threading.Thread(target=server.serve_forever, daemon=True).start()
        with sync_playwright() as p:
            browser = p.chromium.launch()
            print("Notebook")
            notebook_python(browser, base)
            print("Linux lab")
            linux_page(browser, base)
            browser.close()
        server.shutdown()
    print(f"\n{len(FAILS)} failed" if FAILS else "\nall passed")
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
