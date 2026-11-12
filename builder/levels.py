import html
import json
import re

import markdown as MD

from . import toolsteps as T
from .paths import ASSETS, SITE, SRC
from .util import emit

GUIDES = SITE / "media" / "guides"
CHALLENGES = SRC / "ctf" / "challenges.json"
FLAG_SHAPE = re.compile(r"(?i)\b(flag|ctf|aayat|aap)\{[^}\s]+\}")
HIDDEN = "[flag hidden: run the lab to find it]"
HINT = re.compile(r"(?m)^>\s*Hint:.*(?:\n>.*)*\n?")
TOOL = re.compile(r"^\s*(?:sudo\s+)?([A-Za-z0-9_.+-]+)")
STYLE = """body{margin:0;background:#f6f6f2;color:#17171f;font:17px/1.6 Georgia,'Times New Roman',serif}
main{max-width:800px;margin:0 auto;padding:40px 24px 80px}
h1{font-size:34px;line-height:1.15;margin:8px 0 12px}h2{margin-top:44px;padding-top:18px;border-top:2px solid #17171f;font-size:23px}
.kick{font:700 12px/1 Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:#555}
.meta{font:14px Arial,sans-serif;color:#555}
.go{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0}.go a{font:700 14px Arial,sans-serif;padding:10px 14px;border:2px solid #17171f;color:#17171f;text-decoration:none;background:#fff}
.go a.main{background:#17171f;color:#fff}
pre{background:#101018;color:#e8e8e8;padding:12px 14px;overflow:auto;font:13.5px/1.5 Consolas,Menlo,monospace}
pre.want{background:#fff;color:#222;border:1px solid #bbb;max-height:320px}
code{font:.9em Consolas,Menlo,monospace}.lab{font:700 12px Arial,sans-serif;color:#555;margin:14px 0 4px}
blockquote{border-left:4px solid #17171f;margin:14px 0;padding:2px 14px;background:#fff}
@media print{.go{display:none}pre{white-space:pre-wrap}pre.want{max-height:none}body{background:#fff}}"""


def known_flags():
    if not CHALLENGES.exists():
        return []
    data = json.loads(CHALLENGES.read_text(encoding="utf-8"))["challenges"]
    return sorted({c["flag"] for c in data if isinstance(c.get("flag"), str) and len(c["flag"]) >= 6}, key=len, reverse=True)


def shield(cells, flags=None):
    flags = known_flags() if flags is None else flags
    out = []
    for c in cells:
        n = dict(c)

        def hide(text):
            for f in flags:
                text = re.sub(re.escape(f), HIDDEN, text, flags=re.I)
            return FLAG_SHAPE.sub(HIDDEN, text)
        if n.get("e"):
            n["e"] = hide(n["e"])
        if n.get("t") == "md" and n.get("s"):
            n["s"] = T.scrubbed(n["s"], hide)
        out.append(n)
    return out


def _blank(cell, hints):
    body = cell["s"]
    first = next((l for l in body.splitlines() if l.strip() and not l.lstrip().startswith(("cd ", "#", "import os", "os.chdir"))), "")
    m = TOOL.match(first)
    note = "Your turn. Write the code for this step, then press Run."
    if hints and m:
        note += f"\n# Hint: the recording started with {m.group(1)}."
    return "# " + note + "\n"


def variant(cells, level):
    out = []
    for c in cells:
        n = dict(c)
        if level == "guided":
            if c["t"] == "md":
                n["s"] = T.blanked(c["s"])
            else:
                n["s"] = _blank(c, True)
                n["a"] = c.get("a") or c["s"]
        elif level == "solo":
            if c["t"] == "md":
                n["s"] = T.blanked(HINT.sub("", c["s"]).strip())
            else:
                n["s"] = _blank(c, False)
                n["a"] = c.get("a") or c["s"]
                n.pop("e", None)
        out.append(n)
    return out


def merge_expected(cells, expected):
    if not expected:
        return cells
    out = []
    for c in cells:
        n = dict(c)
        hit = expected.get(c["s"]) if c["t"] != "md" else None
        if hit is not None and "e" not in n:
            n["e"] = hit
        out.append(n)
    return out


def _guide_md(text):
    text = T.printable(text)
    text = re.sub(r"(?m)^[ \t]*\?>[ \t]*(.+?)[ \t]*::.*$", r"**Question:** \1", text)
    text = re.sub(r"(?m)^(\s*)- \[[ xX]\] ", "\\1- &#9744; ", text)
    return MD.markdown(text, extensions=["fenced_code", "tables", "sane_lists"])


def guide_html(man, cells):
    cid = man["id"]
    e = html.escape
    start = f"../../../notebook.html?ref=rb-{cid}"
    links = [f'<a class="main" href="{start}&amp;runbook={cid}">Walkthrough</a>',
             f'<a href="{start}--guided&amp;runbook={cid}--guided">Practice</a>',
             f'<a href="{start}--solo&amp;runbook={cid}--solo">Solo</a>']
    if man.get("replay"):
        links.append(f'<a href="../../../replay.html?case={cid}">Watch the recording</a>')
    meta = " &middot; ".join(x for x in [e(str(man.get("level", ""))), f"about {man['minutes']} min" if man.get("minutes") else ""] if x)
    body = [f'<p class="kick">{e(man.get("kicker") or "Lab")} · written tutorial</p>', f"<h1>{e(man['title'])}</h1>", f'<p class="meta">{meta}</p>',
            f"<p>{e(man.get('summary', ''))}</p>", '<div class="go">' + "".join(links) + "</div>"]
    for i, c in enumerate(cells):
        if c["t"] == "md":
            text = c["s"]
            if i == 0:
                text = re.sub(r"(?m)\A#\s+.*$", "", text).replace(man.get("summary") or "\0", "").strip()
            if text:
                body.append(_guide_md(text))
        else:
            if c.get("r"):
                body.append('<p class="lab">Recorded on a real system. The browser Linux shows this result without re-running the tool.</p>')
            body.append("<pre><code>" + e(c["s"]) + "</code></pre>")
            if c.get("e"):
                body.append('<p class="lab">Expected output</p><pre class="want">' + e(c["e"][:6000]) + "</pre>")
    return ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f"<title>{e(man['title'])} written tutorial &middot; Aayat-AP-Prep</title>\n<style>{STYLE}</style>\n</head>\n<body><main>" + "\n".join(body) + "</main></body>\n</html>\n")


def publish(man, cases_dir=None):
    cid = man["id"]
    man["template"] = shield(man["template"])
    cases_dir = cases_dir or ASSETS / "linux" / "cases"
    base = {k: v for k, v in man.items() if k != "template"}
    emit(GUIDES / cid / "index.html", guide_html(man, man["template"]))
    levels = {"worked": cid, "guided": f"{cid}--guided", "solo": f"{cid}--solo"}
    for level, vid in levels.items():
        if level == "worked":
            continue
        emit(cases_dir / vid / "manifest.json", json.dumps(dict(base, id=vid, base=cid, supportLevel=level, levels=levels,
                                                                 guide=f"media/guides/{cid}/index.html", template=variant(man["template"], level)),
                                                            ensure_ascii=False, indent=1) + "\n")
    return levels


def guide_index(entries):
    e = html.escape
    rows = "".join(f'<h2><a href="{e(m["id"])}/index.html">{e(m["title"])}</a></h2><p>{e(m.get("summary", ""))}</p>' for m in entries)
    emit(GUIDES / "index.html", '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
         f"<title>Lab guides &middot; Aayat-AP-Prep</title>\n<style>{STYLE}</style>\n</head>\n<body><main><p class=\"kick\">Aayat-AP-Prep</p><h1>Lab guides</h1>{rows}</main></body>\n</html>\n")
