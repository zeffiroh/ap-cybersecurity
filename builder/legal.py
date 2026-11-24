import re

import markdown

from . import nav as N
from .paths import ROOT
from .util import emit, esc

NOTE = re.compile(r"(?m)^\s*>")
GAP = re.compile(r"\[([^\]\n]*)\](?!\()")
THIRD_PARTY = ROOT / "THIRD_PARTY.txt"


def problems(text):
    out = [f"[{g}] still needs filling in" for g in GAP.findall(text)]
    if NOTE.search(text):
        out.append("a > note line is still in it")
    return out


def render(text):
    return markdown.markdown(text, extensions=["tables"])


def store_note():
    p = N.LEGAL_SRC / "store.md"
    return f'<p class="sx-note">{N.inline_md(p.read_text(encoding="utf-8"))}</p>\n' if p.exists() and N.legal_live() else ""


def run():
    bad = []
    for key, _, path in N.LEGAL:
        if key == "third-party":
            if THIRD_PARTY.exists():
                body = ('<h1>Third-party notices</h1>\n<p class="aa-sub">Open-source programs, libraries, fonts and data used on this site, '
                        'and their licences.</p>\n<pre class="lg-pre">' + esc(THIRD_PARTY.read_text(encoding="utf-8")) + "</pre>")
                emit(path, N.shell(path, "", body))
            continue
        src = N.LEGAL_SRC / f"{key}.md"
        if not src.exists():
            continue
        text = src.read_text(encoding="utf-8")
        found = problems(text)
        if found:
            bad.append(f"source/legal/{key}.md: " + "; ".join(found))
            continue
        emit(path, N.shell(path, "", f'<div class="lg">\n{render(text)}\n</div>'))
    for name in ("footer.md", "store.md"):
        p = N.LEGAL_SRC / name
        if p.exists() and problems(p.read_text(encoding="utf-8")):
            bad.append(f"source/legal/{name}: " + "; ".join(problems(p.read_text(encoding="utf-8"))))
    if bad:
        raise SystemExit("These legal pages aren't finished, so they can't go live:\n  " + "\n  ".join(bad))
