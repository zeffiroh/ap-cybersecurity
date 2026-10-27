"""What the published site gets: scripts, styles and pages without comments. Vendored libraries keep theirs
(licences); SVG figures keep the build stamp the book step reads."""
import re

import rcssmin
import rjsmin

from .paths import ASSETS

VENDOR = (ASSETS / "vendor").resolve()
BLOCK = re.compile(r"(<script\b[^>]*>)(.*?)(</script>)|(<style\b[^>]*>)(.*?)(</style>)|(<textarea\b[^>]*>.*?</textarea>)",
                   re.S | re.I)


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
        return html(text)
    return text
