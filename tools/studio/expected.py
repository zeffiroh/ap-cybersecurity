import functools
import http.server
import json
import socketserver
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
CASES = ROOT / "source" / "static" / "assets" / "linux" / "cases"
TEACHER = ROOT / "source" / "teacher-cases"
RUN = """async ([id, cells]) => {
  const out = [];
  await AayatVM.installCase(id);
  for (const c of cells) {
    const r = await AayatVM.shell(c.r ? 'aayat-replay --id ' + c.r : c.s, {hide: true});
    out.push({s: c.s, out: r.out, code: r.code});
  }
  return out;
}"""


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def targets(only):
    index = json.loads((SITE / "assets" / "linux" / "cases" / "index.json").read_text(encoding="utf-8"))
    return [m["id"] for m in index if not only or m["id"] == only]


def save_path(cid):
    if (CASES / cid).is_dir():
        return CASES / cid / "expected.json"
    if cid.startswith("tc-"):
        return TEACHER / "expected" / f"{cid[3:]}.json"
    if cid.startswith("sem-") and "--" not in cid and (ROOT / "source" / "seminars" / cid[4:]).is_dir():
        return ROOT / "source" / "seminars" / cid[4:] / "expected.json"
    return None


def run_case(page, cid):
    man = json.loads((SITE / "assets" / "linux" / "cases" / cid / "manifest.json").read_text(encoding="utf-8"))
    cells = [c for c in man["template"] if c["t"] == "sh"]
    results = page.evaluate(RUN, [cid, cells])
    failed = [r for r in results if r["code"] not in (0, 1)]
    empty = [r for r in results if not r["out"].strip()]
    print(f"{cid}: {len(results)} Linux cells ran, {len(failed)} failed, {len(empty)} printed nothing")
    for r in failed:
        print(f"  exit {r['code']}: {r['s'].splitlines()[0][:90]}")
    path = save_path(cid)
    if path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({r["s"]: r["out"] for r in results}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    return len(failed)


def run(only=None):
    from playwright.sync_api import sync_playwright
    handler = functools.partial(Quiet, directory=str(SITE))
    with socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler) as server:
        port = server.server_address[1]
        threading.Thread(target=server.serve_forever, daemon=True).start()
        bad = 0
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for cid in targets(only):
                page = browser.new_page()
                page.route("**/*", lambda route: route.fulfill(status=200, content_type="text/html", body="<!DOCTYPE html><title>lab</title>") if route.request.url.endswith("/blank") else route.continue_())
                page.goto(f"http://127.0.0.1:{port}/blank")
                page.add_script_tag(content="window.AAYAT_EVIDENCE = 0;")
                page.add_script_tag(url=f"http://127.0.0.1:{port}/assets/theme/linux-vm.js")
                page.set_default_timeout(180000)
                bad += run_case(page, cid)
                page.close()
            browser.close()
        server.shutdown()
    return 1 if bad else 0
