"""Checks over the built site: links to local files that do not exist, and byte-identical copies.

Links built at runtime by JavaScript are not seen; the crawl in a browser covers those.
"""
import hashlib
import html
import re
from collections import defaultdict
from urllib.parse import unquote, urlsplit

from .paths import ROOT, SITE, SRC

ATTR = re.compile(r"""\s(?:href|src)\s*=\s*(["'])(.*?)\1""", re.I | re.S)
EXPECTED_COPIES = ("smartart",)          # PowerPoint template parts that must repeat per layout


def files(base):
    for p in base.rglob("*"):
        if p.is_file() and "__pycache__" not in p.parts and "vendor" not in p.parts:
            yield p


def duplicates():
    by_size = defaultdict(list)
    for base in (SRC, ROOT / "builder"):
        for p in files(base):
            if p.stat().st_size >= 1024:
                by_size[p.stat().st_size].append(p)
    groups = defaultdict(list)
    for ps in by_size.values():
        if len(ps) > 1:
            for p in ps:
                groups[hashlib.sha1(p.read_bytes()).hexdigest()].append(p)
    return [sorted(ps) for ps in groups.values()
            if len(ps) > 1 and not all(any(x in p.parts for x in EXPECTED_COPIES) for p in ps)]


def broken_links():
    bad = []
    for page in files(SITE):
        if page.suffix.lower() != ".html":
            continue
        text = page.read_text(encoding="utf-8", errors="replace")
        text = re.sub(r"<script\b.*?</script>", "", text, flags=re.S | re.I)   # runtime-built URLs
        for _, url in ATTR.findall(text):
            url = html.unescape(url).strip()
            parts = urlsplit(url)
            if (not url or parts.scheme or url.startswith(("#", "//", "mailto:", "javascript:", "data:"))
                    or "{" in url or "$" in url):
                continue
            target = (page.parent / unquote(parts.path)).resolve() if parts.path else page
            if parts.path.endswith("/"):
                target = target / "index.html"
            if not target.exists() or SITE.resolve() not in target.parents:
                bad.append((page.relative_to(ROOT).as_posix(), url))
    return bad


def run(verbose=False):
    dups = duplicates()
    print(f"duplicate source files: {len(dups)} group(s)")
    for ps in dups[:None if verbose else 15]:
        print(f"  {ps[0].stat().st_size / 1e3:8.0f} KB x{len(ps)}: " + " | ".join(p.relative_to(ROOT).as_posix() for p in ps))
    bad = broken_links()
    print(f"broken local links: {len(bad)} in {len({p for p, _ in bad})} page(s)")
    for p, u in bad[:None if verbose else 25]:
        print(f"  {p} -> {u}")
    return not bad
