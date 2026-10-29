"""What the published site gets: scripts, styles and pages without comments. Vendored libraries keep theirs
(licences); SVG figures keep the build stamp the book step reads. Every page outside assets/ loads the paywall."""
import re

import rcssmin
import rjsmin

from .paths import ASSETS, SHARED, SITE
from .util import rel

VENDOR = (ASSETS / "vendor").resolve()
BLOCK = re.compile(r"(<script\b[^>]*>)(.*?)(</script>)|(<style\b[^>]*>)(.*?)(</style>)|(<textarea\b[^>]*>.*?</textarea>)",
                   re.S | re.I)
HEAD = re.compile(r"<head\b[^>]*>(\s*<meta charset[^>]*>)?", re.I)


def js(text):
    return rjsmin.jsmin(text).strip()


def css(text):
    return rcssmin.cssmin(text).strip()


def html(text):
    out, last = [], 0
    for m in BLOCK.finditer(text):
        out.append(re.sub(r"<!--(?!\[if).*?-->\n?", "", text[last:m.start()], flags=re.S))
        if m.group(1):
            body = m.group(2)
            out.append(m.group(1) + (js(body) if body.strip() else body) + m.group(3))
        elif m.group(4):
            out.append(m.group(4) + css(m.group(5)) + m.group(6))
        else:
            out.append(m.group(7))
        last = m.end()
    out.append(re.sub(r"<!--(?!\[if).*?-->\n?", "", text[last:], flags=re.S))
    return "".join(out)


def gate(path, text):
    """The paywall first thing in <head>, so a locked page never shows. assets/config.js lists the free pages."""
    path = path.resolve()
    m = HEAD.search(text)
    if not m or SITE not in path.parents or ASSETS in path.parents or "paywall.js" in text:
        return text
    d = path.parent
    tags = (f'\n<script src="{rel(d, ASSETS / "config.js")}"></script>'
            f'\n<script src="{rel(d, SHARED / "paywall.js")}"></script>')
    return text[:m.end()] + tags + text[m.end():]


def clean(path, text):
    """Text as it is published at `path`."""
    if VENDOR in path.resolve().parents:
        return text
    suffix = path.suffix.lower()
    if suffix == ".js":
        return js(text) + "\n"
    if suffix == ".css":
        return css(text) + "\n"
    if suffix == ".html":
        return gate(path, html(text))
    return text
