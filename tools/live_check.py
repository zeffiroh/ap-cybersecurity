import argparse
import hashlib
import html
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from builder import audit
from builder.course import SITE_URL

PLACEHOLDER = "dQw4w9WgXcQ"
KEY_PAGES = [
    "", "careers.html", "store.html", "labs.html", "seminars.html", "workstation.html", "playground.html",
    "certificate.html", "community.html", "videos.html", "ctf.html", "sqli.html", "shop.html", "linux.html",
    "notebook.html", "glossary.html", "support.html", "buy/", "media/guides/", "teacher/", "unit-1/",
]
ATTR = re.compile(r"""\s(?:href|src)\s*=\s*(["'])(.*?)\1""", re.I | re.S)
AGENT = "aayat-live-check/1"


def fetch(url, head=False, tries=3):
    for i in range(tries):
        req = urllib.request.Request(url, method="HEAD" if head else "GET", headers={"User-Agent": AGENT, "Cache-Control": "no-cache"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, b"" if head else r.read()
        except urllib.error.HTTPError as e:
            if e.code < 500 or i == tries - 1:
                return e.code, b""
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if i == tries - 1:
                return str(getattr(e, "reason", e)), b""
        time.sleep(2 * (i + 1))


def local_file(path):
    p = ROOT / "site" / path
    return p / "index.html" if path == "" or path.endswith("/") else p


def links(base, body):
    text = re.sub(r"<script\b.*?</script>", "", body.decode("utf-8", "replace"), flags=re.S | re.I)
    out = set()
    for _, raw in ATTR.findall(text):
        raw = html.unescape(raw).strip()
        if not raw or raw.startswith(("#", "mailto:", "javascript:", "data:", "tel:")) or "{" in raw or "$" in raw:
            continue
        url = urljoin(base, raw).split("#")[0]
        if url.startswith(SITE_URL):
            out.add(url)
    return out


def wait_for_deploy(sha, minutes):
    end = time.time() + minutes * 60
    print(f"Waiting for GitHub Pages to deploy {sha[:8]}...")
    while time.time() < end:
        r = subprocess.run(["gh", "run", "list", "--workflow", "pages.yml", "--commit", sha, "--json", "status,conclusion", "-L", "1"],
                           capture_output=True, text=True, cwd=ROOT)
        runs = json.loads(r.stdout or "[]") if r.returncode == 0 else []
        if runs and runs[0]["status"] == "completed":
            if runs[0]["conclusion"] != "success":
                print(f"  The Pages deploy ended with: {runs[0]['conclusion']}. Run: gh run view --log-failed")
                return False
            time.sleep(20)
            return True
        time.sleep(15)
    print(f"  Still not deployed after {minutes} minutes; checking what is live now.")
    return True


def check_pages():
    problems, stale, found = [], [], set()
    with ThreadPoolExecutor(8) as pool:
        results = list(pool.map(lambda p: (p, fetch(SITE_URL + p)), KEY_PAGES))
    for path, (status, body) in results:
        if status != 200:
            problems.append(f"{SITE_URL + path} -> {status}")
            continue
        lf = local_file(path)
        if lf.exists() and hashlib.sha1(lf.read_bytes()).digest() != hashlib.sha1(body).digest():
            stale.append(path or "index.html")
        found |= links(SITE_URL + path, body)
    found -= {SITE_URL + p for p in KEY_PAGES}
    with ThreadPoolExecutor(16) as pool:
        for url, (status, _) in zip(sorted(found), pool.map(lambda u: fetch(u, head=True), sorted(found))):
            if status != 200:
                problems.append(f"{url} -> {status}")
    return problems, stale, len(found) + len(KEY_PAGES)


def check_videos():
    try:
        import psycopg
        sys.path.insert(0, str(ROOT / "db"))
        from sql import url
    except Exception:
        return None, ["Videos not checked: needs  pip install \"psycopg[binary]==3.2.3\"  and NEON_DATABASE_URL in .env"]
    try:
        with psycopg.connect(url(), connect_timeout=20) as db:
            sem = db.execute("select title, youtube, published from seminars order by sort, id").fetchall()
            vids = db.execute("select title from videos where youtube like %s", (f"%{PLACEHOLDER}%",)).fetchall()
    except psycopg.Error as e:
        msg = str(e).strip().splitlines()[-1]
        return -1, [f"DATABASE DOWN: {msg}", "  Sign-in, unlocks, tickets and payment sync do not work while this lasts."]
    lines = []
    ph = [t for t, y, _ in sem if PLACEHOLDER in y]
    missing = [t for t, y, p in sem if p and not y.strip()]
    if ph:
        lines.append(f"{len(ph)} seminar(s) still have the placeholder video (COMMANDS: Clear placeholder videos):")
        lines += [f"  {t}" for t in ph]
    if vids:
        lines.append(f"{len(vids)} lesson video(s) still have the placeholder:")
        lines += [f"  {t}" for (t,) in vids]
    if missing:
        lines.append(f"{len(missing)} published seminar(s) have no video link:")
        lines += [f"  {t}" for t in missing]
    published = sum(1 for _, _, p in sem if p)
    return (len(ph) + len(vids) + len(missing)), [f"seminars: {published} of {len(sem)} published"] + lines


def main():
    ap = argparse.ArgumentParser(description="Check the live site after a publish.")
    ap.add_argument("--wait", metavar="SHA", help="wait for the GitHub Pages deploy of this commit first")
    ap.add_argument("--minutes", type=int, default=10)
    ap.add_argument("--no-db", action="store_true", help="skip the video checks")
    a = ap.parse_args()

    deployed = wait_for_deploy(a.wait, a.minutes) if a.wait else True
    print(f"Live check of {SITE_URL}")
    problems, stale, n = check_pages()
    print(f"pages and files checked: {n}")
    print(f"broken: {len(problems)}")
    for p in problems[:40]:
        print(f"  {p}")
    if stale:
        print(f"not the same as this computer's site\\ (still deploying, or not pushed): {', '.join(stale)}")
    level, lines = audit.size_report()
    for line in lines:
        print(line)
    video_problems = 0
    if not a.no_db:
        video_problems, vlines = check_videos()
        for line in vlines:
            print(line)
    ok = deployed and not problems and level != "stop" and video_problems != -1
    print("Live check: clean." if ok and not stale and not video_problems else
          "Live check: the site is up, see the notes above." if ok else
          "Live check: PROBLEMS, see above.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
