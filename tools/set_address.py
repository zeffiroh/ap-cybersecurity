import argparse
import html
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
SETTING = Path("builder") / "course.py"
LINE = re.compile(r'(?m)^SITE_URL = "([^"]*)"$')
SCAN = ["builder", "tools", "db", "tests", "source", ".github", "publish", "build.py", "teach", "desk.cmd"]
SKIP_DIRS = {"__pycache__", "node_modules", ".git"}
TEXT = {".py", ".js", ".css", ".html", ".md", ".json", ".txt", ".yml", ".yaml", ".sh", ".cmd", ".ps1", ".ipynb", ".svg", ".xml", ""}
GITHUB_IPS = ["185.199.108.153", "185.199.109.153", "185.199.110.153", "185.199.111.153"]


def normalise(address):
    a = address.strip()
    if not re.match(r"^https?://", a):
        a = "https://" + a
    parts = urlsplit(a)
    if not parts.netloc or " " in a or parts.query or parts.fragment:
        raise ValueError(f"{address} isn't a web address. Use one like https://www.example.com/ or example.com/course/")
    path = parts.path if parts.path.endswith("/") else parts.path + "/"
    return f"{parts.scheme}://{parts.netloc.lower()}{path}"


def host_of(url):
    return url.split("://", 1)[-1].rstrip("/")


def current(root):
    m = LINE.search((root / SETTING).read_text(encoding="utf-8"))
    if not m:
        raise ValueError(f"No SITE_URL line in {SETTING}")
    return m.group(1)


def write_setting(root, new):
    path = root / SETTING
    text = path.read_text(encoding="utf-8")
    path.write_bytes(LINE.sub(f'SITE_URL = "{new}"', text, count=1).encode("utf-8"))


def files_to_scan(root):
    for name in SCAN:
        p = root / name
        if p.is_file():
            yield p
        elif p.is_dir():
            for f in p.rglob("*"):
                if f.is_file() and f.suffix.lower() in TEXT and not SKIP_DIRS & set(f.relative_to(root).parts):
                    yield f


def leftovers(root, url):
    needle = host_of(url).encode("utf-8")
    out = []
    for f in files_to_scan(root):
        if f.resolve() == (root / SETTING).resolve():
            continue
        try:
            if needle in f.read_bytes():
                out.append(f.relative_to(root).as_posix())
        except OSError:
            pass
    return sorted(out)


def fix_videos(root, old, new):
    changed, cards = [], []
    for base in (root / ".cache" / "demos", root / ".cache" / "lectures"):
        if not base.is_dir():
            continue
        for folder in sorted(p for p in base.iterdir() if p.is_dir()):
            yt = folder / "youtube.txt"
            if yt.is_file():
                text = yt.read_text(encoding="utf-8")
                if old in text:
                    yt.write_text(text.replace(old, new), encoding="utf-8")
                    changed.append(folder.name)
            if (folder / "card-end.png").is_file():
                cards.append(folder.name)
    return changed, cards


def stub(target):
    t = html.escape(target, quote=True)
    js = target.replace("\\", "\\\\").replace('"', '\\"')
    return (f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>This page has moved</title>\n'
            f'<meta name="robots" content="noindex"><link rel="canonical" href="{t}">\n'
            f'<meta http-equiv="refresh" content="0; url={t}">\n'
            f'<script>location.replace("{js}" + location.search + location.hash)</script>\n'
            f'</head><body><p>This page has moved to <a href="{t}">{t}</a>.</p></body></html>\n')


def redirect_site(site, out, old, new):
    old_path = urlsplit(old).path
    made = 0
    for page in sorted(site.rglob("*.html")):
        rel = page.relative_to(site).as_posix()
        target = new + (rel[: -len("index.html")] if rel.endswith("index.html") else rel)
        dest = out / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(stub(target), encoding="utf-8", newline="\n")
        made += 1
    base = old_path.replace("\\", "\\\\").replace('"', '\\"')
    js = new.replace('"', '\\"')
    (out / "404.html").write_text(
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><title>This page has moved</title>\n'
        '<meta name="robots" content="noindex">\n'
        f'<script>var p = location.pathname, b = "{base}"; if (p.indexOf(b) === 0) p = p.slice(b.length); else p = p.replace(/^\\//, "");\n'
        f'location.replace("{js}" + p + location.search + location.hash)</script>\n'
        f'</head><body><p>This site has moved to <a href="{html.escape(new)}">{html.escape(new)}</a>.</p></body></html>\n',
        encoding="utf-8", newline="\n")
    (out / ".nojekyll").write_text("", encoding="utf-8")
    return made + 1


def point_pages_at(root, folder):
    wf = root / ".github" / "workflows" / "pages.yml"
    text = wf.read_text(encoding="utf-8")
    new = re.sub(r"(?m)^([ \t]*path:[ \t]*)\S+[ \t]*$", lambda m: m.group(1) + folder, text, count=1)
    wf.write_bytes(new.encode("utf-8"))
    return new != text


def run(cmd, root):
    print("  " + " ".join(cmd[1:]) if cmd[0] == sys.executable else "  " + " ".join(cmd))
    return subprocess.run(cmd, cwd=root).returncode == 0


def outside_steps(old, new, leaving):
    host = urlsplit(new).hostname or ""
    own_domain = not host.endswith(".github.io")
    lines = ["", "Do these by hand (the code can't reach them):"]
    n = 0

    def step(text):
        nonlocal n
        n += 1
        lines.append(f"  {n}. {text}")

    if own_domain and not leaving:
        apex = host.count(".") == 1
        step(f"At the shop where you bought {host}, add the DNS record"
             + (f"s: four A records for {host} -> " + ", ".join(GITHUB_IPS) + f", and a CNAME for www.{host} -> zeffiroh.github.io"
                if apex else f": a CNAME for {host} -> zeffiroh.github.io"))
        step(f"GitHub -> the repository -> Settings -> Pages -> Custom domain: {host}, Save; once it says the DNS check passed, tick Enforce HTTPS. "
             "GitHub then sends every old link to the same page at the new address by itself.")
    if leaving:
        step("Set up the new host to serve the site\\ folder at the new address. The old address (GitHub Pages) now serves the redirect\\ folder, "
             "which sends every old page to the same page at the new address.")
    step(f"Neon console -> Auth -> allowed domains, and Data API -> CORS / allowed origins: add {new.rstrip('/')} "
         "(keep the old one until everyone has moved). Without this, sign-in and grades stop working on the new address.")
    step("Razorpay payment pages: the book page's thank-you message is publication\\razorpay\\thank-you-message.txt (rebuilt just now); "
         "check every page's description and thank-you text for the old address.")
    step("Gumroad, Payhip and Pothi: listing descriptions and thank-you messages (publication\\gumroad\\thank-you-message.txt is rebuilt).")
    step("YouTube: videos already uploaded keep the old address in their description; paste the new one (the old one still forwards).")
    step(f"cyber.txt section 9: find {old} and replace all with {new}.")
    step("Tell students before the switch: work saved only in a browser stays with the old address. Signed-in work moves with the account; "
         "anyone not signed in should save a backup file first.")
    step('Then run:  ./publish "Site address is now ' + new + '"   and read the live check at the end.')
    return lines


def main(argv=None):
    ap = argparse.ArgumentParser(description="Change the site address everywhere. The address lives in one setting: SITE_URL in builder/course.py.")
    ap.add_argument("address", help="the new address, for example https://www.example.com/ or example.com/course/")
    ap.add_argument("--no-build", action="store_true", help="change the setting and the video texts only, don't rebuild")
    ap.add_argument("--leaving-github", action="store_true", help="the site moves off GitHub Pages: also make the redirect site the old address will serve")
    ap.add_argument("--root", default=str(ROOT), help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    try:
        new = normalise(args.address)
        old = current(root)
    except ValueError as e:
        print(e)
        return 1
    if new == old:
        print(f"The site address is already {old}. Nothing changed.")
        return 0
    write_setting(root, new)
    print(f"Site address: {old} -> {new}  (builder/course.py SITE_URL)")
    left = leftovers(root, old)
    if left:
        print("These files still write the old address out in full; change them to read SITE_URL or use {{site}}:")
        for f in left:
            print("  " + f)
    changed, cards = fix_videos(root, old, new)
    if changed:
        print(f"Updated youtube.txt in {len(changed)} video folders.")
    if cards:
        print(f"{len(cards)} silent videos show the old address on their end card. The old address forwards, so remake them only if you want "
              "(Teaching Desk: Make the silent video).")
    ok = True
    if not args.no_build:
        print("Rebuilding the site (about 7 minutes) and the book editions...")
        ok = run([sys.executable, "build.py"], root) and ok
        ok = run([sys.executable, "-m", "builder.editions"], root) and ok
        if not ok:
            print("A rebuild step failed (above). Fix it, then run: python build.py ; python -m builder.editions")
    else:
        print("Skipped the rebuild. Run: python build.py ; python -m builder.editions")
    if args.leaving_github:
        site = root / "site"
        made = redirect_site(site, root / "redirect", old, new) if site.is_dir() else 0
        moved = point_pages_at(root, "redirect")
        print(f"Made redirect\\ with {made} pages for the old address" + (", and pointed GitHub Pages at it (.github/workflows/pages.yml)." if moved else "."))
    print("\n".join(outside_steps(old, new, args.leaving_github)))
    return 0 if ok and not left else 1


if __name__ == "__main__":
    sys.exit(main())
