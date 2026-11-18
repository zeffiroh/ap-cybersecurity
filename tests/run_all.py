import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
LOGS = ROOT / ".cache" / "tests"


def found():
    out = []
    for p in sorted(TESTS.glob("test_*.py")):
        out.append((p.stem, [sys.executable, str(p)]))
    js = sorted(TESTS.glob("*.test.js"))
    if js:
        node = shutil.which("node")
        out.append(("node tests", [node, "--test"] + [str(p) for p in js] if node else None))
    for p in sorted(TESTS.glob("browser_*.py")):
        out.append((p.stem, [sys.executable, str(p)]))
    return out


def has_playwright():
    try:
        import playwright.sync_api
        return True
    except ImportError:
        return False


def main():
    ap = argparse.ArgumentParser(description="Run every test in tests/ and print one pass/fail list.")
    ap.add_argument("names", nargs="*", help="only run tests whose name contains one of these words")
    ap.add_argument("--quick", action="store_true", help="skip the browser tests")
    args = ap.parse_args()

    tests = found()
    if args.quick:
        tests = [t for t in tests if not t[0].startswith("browser_")]
    if args.names:
        tests = [t for t in tests if any(n in t[0] for n in args.names)]
    if not tests:
        print("No tests matched.")
        return 1

    LOGS.mkdir(parents=True, exist_ok=True)
    browser_ok = has_playwright()
    results = {}
    started = time.time()

    def finish(name, r, secs):
        text = (r.stdout or "") + (r.stderr or "")
        (LOGS / (name.replace(" ", "_") + ".log")).write_text(text, encoding="utf-8")
        status = "ok" if r.returncode == 0 else "FAIL"
        note = ""
        if r.returncode == 0 and "OK (skipped=" in text:
            note = "some skipped: " + text.split("OK (skipped=")[1].split(")")[0]
        results[name] = (name, status, secs, text if status == "FAIL" else note)
        print(f"  {status:<5} {name}  ({secs:.0f}s){'  ' + note if note else ''}", flush=True)

    def one(name, cmd):
        t0 = time.time()
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        return name, r, time.time() - t0

    browsers = []
    for name, cmd in tests:
        if cmd is None:
            results[name] = (name, "FAIL", 0, "Node.js isn't installed, so the JavaScript tests can't run.")
            print(f"  FAIL  {name}  (Node.js isn't installed)")
        elif name.startswith("browser_") and not browser_ok:
            results[name] = (name, "FAIL", 0, "Playwright isn't installed: pip install playwright ; python -m playwright install chromium")
            print(f"  FAIL  {name}  (Playwright isn't installed)")
        elif name.startswith("browser_"):
            browsers.append((name, cmd))
        else:
            finish(*one(name, cmd))
    if browsers:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=2) as pool:
            for got in pool.map(lambda t: one(*t), browsers):
                finish(*got)
    results = [results[n] for n, _ in tests if n in results]

    fails = [r for r in results if r[1] == "FAIL"]
    for name, _, _, text in fails:
        print(f"\n--- {name} (last lines; full log in .cache/tests/) ---")
        lines = [l for l in text.splitlines() if l.strip()]
        print("\n".join(lines[-25:]))

    print(f"\n{len(results) - len(fails)} of {len(results)} passed in {time.time() - started:.0f}s")
    print(f"{len(fails)} failed: " + ", ".join(r[0] for r in fails) if fails else "All tests passed.")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
