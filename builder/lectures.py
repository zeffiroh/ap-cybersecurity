"""The 30 lecture decks from their Markdown sources.

source/lectures/NN_<name>.md   ->  lectures/NN_<name>.html          (browser deck, speaker notes popup on N)
                               ->  teacher/lectures/NN_<name>.pptx  (same slides, on the templates/lecture.pptx
                                                                     theme; `smartart=<Layout>` blocks become SmartArt)
source/lectures/images/        ->  lectures/images/ (copied by the static step)
```mermaid code blocks          ->  lectures/diagrams/<hash>.png (drawn by Mermaid in the browser at build time)
all front matter               ->  lectures/index.html              (deck menu)
templates/deck.html, templates/deck_index.html are the page shells.

Notes syntax: YAML front matter per deck (`deck:`) and per slide, slides separated by `%%%`,
blocks written as `:::type key=value ... :::` (`::::columns` / `::col::` / `::::` for columns).

Long slides are split into "(2/3)"-style parts. With Playwright + Chromium installed, every split is
measured in a real browser against lectures/site.css, so a part never overflows the slide; otherwise a
fitted height estimate is used.
"""
import hashlib
import html
import io
import json
import re
import sys
import zipfile
from pathlib import Path

import yaml
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

from . import lecture_pptx
from . import nav as N
from .paths import LECTURES as SITE, LECTURES_SRC as NOTES, TEACHER, TEMPLATES
from .util import emit as _emit, emit_bytes, keep
from . import util

PPT = TEACHER / "lectures"
ESTIMATE = False          # set by build.py --estimate: skip the browser, use the height estimate
NO_PPTX = False           # set by build.py --no-pptx
ONLY = []                 # deck numbers ("04") to rebuild; empty = all


# ============================================================================
# 1. INLINE MARKDOWN  (bold / italic / code / links)
# ============================================================================

def esc(text):
    """HTML-escape plain text (used for attributes and code blocks)."""
    return html.escape(text if text is not None else "", quote=True)


def inline_md(text):
    """Convert a small subset of inline Markdown to HTML.
    Supports **bold**, *italic*, `code`, [text](url). Escapes raw HTML first."""
    if text is None:
        return ""
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    t = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    return t


def paragraph_html(raw_text, force_paragraphs=False):
    """Turn a raw multi-line block of text into HTML.
    Blank lines separate paragraphs. If there's only one paragraph and
    force_paragraphs is False, no <p> wrapper is added (keeps short callouts
    looking inline, matching the original hand-built deck)."""
    raw_text = raw_text.strip("\n")
    paras = [p.strip() for p in re.split(r"\n\s*\n", raw_text) if p.strip()]
    converted = [inline_md(" ".join(p.split("\n"))) for p in paras]
    if not converted:
        return ""
    if len(converted) == 1 and not force_paragraphs:
        return converted[0]
    return "".join(f"<p>{p}</p>" for p in converted)


# ============================================================================
# 2. FENCE TOKENIZER  (the ":::type key=val" ... ":::" block DSL)
# ============================================================================

FENCE_OPEN_RE = re.compile(r"^(:{3,})([A-Za-z][\w-]*)\s*(.*)$")
ATTR_RE = re.compile(r'([A-Za-z_][\w-]*)\s*=\s*(".*?"|\'.*?\'|\S+)')
COLSEP_RE = re.compile(r"^::col::\s*$")


def parse_attrs(attr_str):
    """Parse `key="val with spaces" key2=val2 key3=true` into a dict.
    Bareword true/false become Python booleans."""
    out = {}
    for m in ATTR_RE.finditer(attr_str or ""):
        key, val = m.group(1), m.group(2)
        if val and val[0] in "\"'" and val[-1] == val[0]:
            val = val[1:-1]
        if val.lower() == "true":
            val = True
        elif val.lower() == "false":
            val = False
        out[key] = val
    return out


def tokenize_fences(text):
    """Split `text` into top-level fenced blocks. A fence opens with
    `:::name attrs` (3+ colons) and closes with a bare line of the SAME
    number of colons. Fences of the same colon-length nested inside one
    another (e.g. a `card` inside a `columns`, both written with four
    colons) are matched by depth, like balanced brackets — the first
    same-length bare-colon line does NOT necessarily close the block;
    only the one that brings that length's depth back to zero does."""
    lines = text.split("\n")
    blocks = []
    i = 0
    n = len(lines)
    while i < n:
        m = FENCE_OPEN_RE.match(lines[i].strip())
        if not m:
            i += 1
            continue
        colons, btype, attr_str = m.groups()
        close = colons
        depth = 1
        inner = []
        i += 1
        closed = False
        while i < n:
            stripped = lines[i].strip()
            if stripped == close:
                depth -= 1
                if depth == 0:
                    closed = True
                    i += 1
                    break
                inner.append(lines[i])
                i += 1
                continue
            mm = FENCE_OPEN_RE.match(stripped)
            if mm and mm.group(1) == colons:
                depth += 1
            inner.append(lines[i])
            i += 1
        if not closed:
            raise ValueError(
                f"Unclosed '{colons}{btype}' block (expected a line with exactly "
                f"'{close}' to close it). If this block contains other "
                f"::: blocks inside it, remember 'columns' and 'card' need "
                f"FOUR colons (::::), not three."
            )
        blocks.append({
            "type": btype.lower(),
            "attrs": parse_attrs(attr_str),
            "raw": "\n".join(inner),
        })
    return blocks


# ============================================================================
# 3. BLOCK MATERIALIZATION  (raw fence -> schema-shaped block dict)
# ============================================================================

def materialize_list(raw, attrs):
    items = []
    for line in raw.split("\n"):
        s = line.strip()
        if s.startswith(("- ", "* ")):
            items.append(s[2:].strip())
        elif s in ("-", "*"):
            items.append("")
    block = {
        "type": "list",
        "items": items,
        "style": attrs.get("style", "plain"),
        "ordered": bool(attrs.get("ordered", False)),
    }
    if attrs.get("heading"):
        block["heading"] = attrs["heading"]
    return block


def materialize_table(raw, attrs):
    rows = [r.strip() for r in raw.split("\n") if r.strip()]
    rows = [r for r in rows if not re.match(r"^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?$", r)]

    def split_row(r):
        r = r.strip()
        if r.startswith("|"):
            r = r[1:]
        if r.endswith("|"):
            r = r[:-1]
        return [c.strip() for c in r.split("|")]

    if not rows:
        return {"type": "table", "headers": [], "rows": []}
    headers = split_row(rows[0])
    data_rows = [split_row(r) for r in rows[1:]]
    return {"type": "table", "headers": headers, "rows": data_rows}


def materialize_flow(raw, attrs):
    steps = [s.strip() for s in raw.split("\n") if s.strip()]
    return {"type": "flow", "steps": steps}


def materialize_steps(raw, attrs):
    items = []
    for line in raw.split("\n"):
        s = line.strip()
        if s.startswith(("- ", "* ")):
            items.append(s[2:].strip())
        elif s:
            items.append(s)
    return {"type": "steps", "items": items}


def materialize_code(raw, attrs):
    code_text = raw
    if code_text.startswith("\n"):
        code_text = code_text[1:]
    block = {
        "type": "code",
        "code": code_text.rstrip("\n"),
        "language": attrs.get("language", "text"),
    }
    if attrs.get("caption"):
        block["caption"] = attrs["caption"]
    return block


def materialize_media(btype, attrs):
    block = {"type": btype}
    block.update(attrs)
    return block


def materialize_columns(raw, attrs):
    chunks = COLSEP_RE.split(raw, flags=0) if False else re.split(r"(?m)^::col::\s*$", raw)
    chunks = [c for c in chunks if c.strip() != ""]
    columns = [materialize_blocks(tokenize_fences(c)) for c in chunks]
    block = {"type": "columns", "columns": columns}
    if attrs.get("ratio"):
        block["ratio"] = attrs["ratio"]
    return block


def materialize_card(raw, attrs):
    inner = materialize_blocks(tokenize_fences(raw))
    block = {"type": "card", "blocks": inner}
    if attrs.get("heading"):
        block["heading"] = attrs["heading"]
    return block


def materialize_one(fence):
    t = fence["type"]
    raw, attrs = fence["raw"], fence["attrs"]

    if t == "callout":
        return {"type": "callout", "html": paragraph_html(raw), "style": attrs.get("style", "soft")}
    if t == "pullquote":
        return {"type": "pullquote", "html": paragraph_html(raw)}
    if t == "text":
        b = {"type": "text", "html": paragraph_html(raw, force_paragraphs=True)}
        if attrs.get("class"):
            b["class"] = attrs["class"]
        return b
    if t == "notes":
        return {"type": "notes", "html": paragraph_html(raw, force_paragraphs=True)}
    if t == "list":
        return materialize_list(raw, attrs)
    if t == "table":
        return materialize_table(raw, attrs)
    if t == "flow":
        return materialize_flow(raw, attrs)
    if t == "steps":
        return materialize_steps(raw, attrs)
    if t == "code":
        return materialize_code(raw, attrs)
    if t in ("image", "iframe", "geogebra", "desmos"):
        return materialize_media(t, attrs)
    if t == "columns":
        return materialize_columns(raw, attrs)
    if t == "card":
        return materialize_card(raw, attrs)

    raise ValueError(f"Unknown block type ':::{t}'")


_materialize_one = materialize_one


def materialize_one(fence):                              # noqa: F811
    """Adds the `smartart=<Layout>` option (any list/steps/flow block): the PowerPoint shows that block
    as SmartArt using templates/smartart/<Layout>/, the browser deck shows it as written."""
    b = _materialize_one(fence)
    if fence["attrs"].get("smartart"):
        b["smartart"] = fence["attrs"]["smartart"]
    if fence["type"] == "steps" and fence["attrs"].get("heading"):
        b["heading"] = fence["attrs"]["heading"]
    return b


def materialize_blocks(fences):
    return [materialize_one(f) for f in fences]


# ============================================================================
# 4. SLIDE / DECK PARSING
# ============================================================================

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.S)


def split_frontmatter(segment):
    """If `segment` starts with a YAML frontmatter block, return (meta, body).
    Otherwise return ({}, segment)."""
    stripped = segment.lstrip("\n")
    m = FRONTMATTER_RE.match(stripped)
    if not m:
        return {}, segment
    meta = yaml.safe_load(m.group(1)) or {}
    body = stripped[m.end():]
    return meta, body


def parse_slide_segment(segment, index):
    meta, body = split_frontmatter(segment)
    fences = tokenize_fences(body)
    blocks = []
    notes_html_parts = []
    for f in fences:
        if f["type"] == "notes":
            notes_html_parts.append(paragraph_html(f["raw"], force_paragraphs=True))
        else:
            blocks.append(materialize_one(f))

    title = meta.get("title")
    if not title:
        m = re.search(r"(?m)^#\s+(.+)$", body)
        title = m.group(1).strip() if m else f"Untitled Slide {index+1}"

    slide = {
        "title": title,
        "unit": meta.get("unit", ""),
        "code": str(meta.get("code", "")).upper()[:4] or _auto_code(meta.get("unit", ""), index),
        "blocks": blocks,
    }
    if meta.get("cover"):
        slide["cover"] = True
    if notes_html_parts:
        slide["notes"] = "".join(notes_html_parts)
    return slide


def _auto_code(unit, index):
    letters = re.sub(r"[^A-Za-z]", "", unit or "")
    return (letters[:3].upper() or f"S{index+1:02d}")


def parse_file(path):
    raw = Path(path).read_text(encoding="utf-8")

    deck_meta = {}
    if raw.lstrip().startswith("---"):
        m = FRONTMATTER_RE.match(raw.lstrip("\n"))
        if m:
            fm = yaml.safe_load(m.group(1)) or {}
            if "deck" in fm:
                deck_meta = fm["deck"] or {}
                raw = raw.lstrip("\n")[m.end():]

    segments = re.split(r"(?m)^%%%\s*$", raw)
    segments = [s for s in segments if s.strip()]

    slides = [parse_slide_segment(seg, i) for i, seg in enumerate(segments)]
    return {"deck": deck_meta, "slides": slides}


# ============================================================================
# 6. BLOCK -> HTML RENDERING
# ============================================================================

def aspect_padding(aspect):
    try:
        w, h = aspect.split(":")
        return float(h) / float(w) * 100
    except Exception:
        return 56.25  # 16:9 fallback


def render_block(b):
    t = b["type"]
    extra_class = f' {b["class"]}' if b.get("class") else ""

    if t == "callout":
        cls = {"soft": "card-soft", "line": "card-line", "pull": "pull"}.get(b.get("style", "soft"), "card-soft")
        return f'<div class="{cls}{extra_class}">{b["html"]}</div>'

    if t == "pullquote":
        return f'<div class="pull{extra_class}">{b["html"]}</div>'

    if t == "text":
        return f'<div class="text-block{extra_class}">{b["html"]}</div>'

    if t == "list":
        heading = f'<h4>{esc(b["heading"])}</h4>' if b.get("heading") else ""
        if b.get("style") == "chips":
            chips = "".join(f'<span class="chip">{inline_md(i)}</span>' for i in b["items"])
            inner = chips
            cls_attr = (' class="' + b["class"] + '"') if b.get("class") else ""
            return f'<div class="card-line{extra_class}">{heading}{inner}</div>' if heading else f'<div{cls_attr}>{inner}</div>'
        tag = "ol" if b.get("ordered") else "ul"
        cls = "list-plain" if b.get("style", "plain") == "plain" else "list-tight"
        items = "".join(f"<li>{inline_md(i)}</li>" for i in b["items"])
        body = f'<{tag} class="{cls}{extra_class}">{items}</{tag}>'
        return f'<div class="card-line">{heading}{body}</div>' if heading else body

    if t == "table":
        head = "".join(f"<th>{esc(h)}</th>" for h in b["headers"])
        rows = "".join(
            "<tr>" + "".join(f"<td>{inline_md(c)}</td>" for c in row) + "</tr>"
            for row in b["rows"]
        )
        return f'<table class="tbl{extra_class}"><tr>{head}</tr>{rows}</table>'

    if t == "flow":
        parts = []
        for i, s in enumerate(b["steps"]):
            if i:
                parts.append('<span class="arrow">&rarr;</span>')
            parts.append(f'<span class="step">{esc(s)}</span>')
        return f'<div class="flow{extra_class}">{"".join(parts)}</div>'

    if t == "steps":
        rows = "".join(
            f'<div class="step-row"><div class="step-circle">{i}</div>'
            f'<div class="step-text">{inline_md(s)}</div></div>'
            for i, s in enumerate(b["items"], start=1)
        )
        return f'<div class="steps{extra_class}">{rows}</div>'

    if t == "card":
        heading = f'<h4>{esc(b["heading"])}</h4>' if b.get("heading") else ""
        inner = "".join(render_block(nb) for nb in b["blocks"])
        return f'<div class="card-line{extra_class}">{heading}{inner}</div>'

    if t == "columns":
        n = len(b["columns"])
        cells = "".join(f"<div>{''.join(render_block(nb) for nb in col)}</div>" for col in b["columns"])
        if n in (2, 3, 5):
            return f'<div class="grid-{n}{extra_class}">{cells}</div>'
        return (f'<div class="{extra_class.strip()}" '
                f'style="display:grid;grid-template-columns:repeat({n},1fr);gap:18px;height:100%;">{cells}</div>')

    if t == "image":
        widthcls = "half" if b.get("width") == "half" else ""
        cap = f'<div class="media-caption">{inline_md(b["caption"])}</div>' if b.get("caption") else ""
        alt = esc(b.get("alt", ""))
        return (f'<figure class="media-figure {widthcls}{extra_class}">'
                f'<img src="{esc(b["src"])}" alt="{alt}" loading="lazy">{cap}</figure>')

    if t == "iframe":
        pad = aspect_padding(b.get("aspect", "16:9"))
        cap = f'<div class="media-caption">{inline_md(b["caption"])}</div>' if b.get("caption") else ""
        title = esc(b.get("title", "embedded content"))
        return (f'<div class="embed-wrap{extra_class}"><div class="aspect-box" style="padding-bottom:{pad}%;">'
                f'<iframe src="{esc(b["src"])}" title="{title}" allowfullscreen loading="lazy"></iframe></div></div>{cap}')

    if t == "geogebra":
        src = b.get("src") or f'https://www.geogebra.org/material/iframe/id/{b.get("material_id","")}'
        pad = aspect_padding(b.get("aspect", "4:3"))
        cap = f'<div class="media-caption">{inline_md(b["caption"])}</div>' if b.get("caption") else ""
        return (f'<div class="embed-wrap{extra_class}"><div class="aspect-box" style="padding-bottom:{pad}%;">'
                f'<iframe src="{esc(src)}" title="GeoGebra applet" allowfullscreen loading="lazy"></iframe></div></div>{cap}')

    if t == "desmos":
        src = b.get("src") or f'https://www.desmos.com/calculator/{b.get("graph_id","")}?embed'
        pad = aspect_padding(b.get("aspect", "4:3"))
        cap = f'<div class="media-caption">{inline_md(b["caption"])}</div>' if b.get("caption") else ""
        return (f'<div class="embed-wrap{extra_class}"><div class="aspect-box" style="padding-bottom:{pad}%;">'
                f'<iframe src="{esc(src)}" title="Desmos calculator" allowfullscreen loading="lazy"></iframe></div></div>{cap}')

    if t == "code":
        cap = f"<span>{esc(b['caption'])}</span>" if b.get("caption") else ""
        return (f'<div class="code-block{extra_class}"><div class="code-head">'
                f'<span>{esc(b.get("language","text"))}</span>{cap}</div>'
                f'<pre><code>{esc(b["code"])}</code></pre></div>')

    return ""


def render_slide_content_html(slide):
    inner_blocks = "".join(render_block(b) for b in slide["blocks"])
    if slide.get("cover"):
        return f'<div class="cover"><div class="kicker">{esc(slide.get("unit",""))}</div><h1>{slide["title"]}</h1>{inner_blocks}</div>'
    return (
        f'<div class="slide-eyebrow">{esc(slide.get("unit",""))}</div>'
        f'<h1 class="slide-title">{slide["title"]}</h1>'
        f'<div class="title-rule"></div>'
        f'<div class="slide-body">{inner_blocks}</div>'
    )




# ============================================================================
# 7. CODE HIGHLIGHTING AND IMAGE PATHS
# ============================================================================

def highlight_code(code, language):
    try:
        lexer = get_lexer_by_name(language)
    except ClassNotFound:
        return esc(code)
    return highlight(code, lexer, HtmlFormatter(nowrap=True)).rstrip("\n")


SHOW_UNFINISHED = False   # set by build.py --show-unfinished-images
_usable = {}
hidden_images = set()


def image_usable(src):
    """False for a missing file or one of the red-banner "COURSE VISUAL PLACEHOLDER" stand-ins,
    so the decks never show a broken image or a placeholder's prompt text. Saving a real image
    under the same name in source/lectures/images brings the slide back on the next build."""
    if SHOW_UNFINISHED or not src.startswith("images/"):
        return True
    if src not in _usable:
        path = NOTES / src
        ok = path.exists()
        if ok:
            from PIL import Image
            im = Image.open(path).convert("RGB")
            w, h = im.size
            band = [im.getpixel((int(w * x), int(h * 0.06))) for x in (0.2, 0.4, 0.6)]
            ok = not all(abs(r - 0xB3) < 25 and g < 40 and b < 60 for r, g, b in band)
        _usable[src] = ok
    if not _usable[src]:
        hidden_images.add(src)
    return _usable[src]


def drop_unfinished(blocks):
    out = []
    for b in blocks:
        if b["type"] == "image" and not image_usable(b.get("src", "")):
            continue
        if b["type"] == "columns":
            cols = [c for c in (drop_unfinished(c) for c in b["columns"]) if c]
            if len(cols) == 1:
                out.extend(cols[0])
                continue
            b = dict(b, columns=cols)
        if b["type"] == "card":
            b = dict(b, blocks=drop_unfinished(b["blocks"]))
        out.append(b)
    return out


def prepare(blocks):
    """Pre-render code (images stay at images/..., copied next to the decks)."""
    for b in blocks:
        if b["type"] == "code":
            b["code_html"] = highlight_code(b["code"], b.get("language", "text"))
        for col in b.get("columns", []):
            prepare(col)
        prepare(b.get("blocks", []))
    return blocks


_render_block = render_block


def render_block(b):                                     # noqa: F811  (wraps the archived renderer)
    if b["type"] == "code":
        cap = f"<span>{esc(b['caption'])}</span>" if b.get("caption") else ""
        extra = f' {b["class"]}' if b.get("class") else ""
        return (f'<div class="code-block{extra}"><div class="code-head"><span>{esc(b.get("language", "text"))}</span>{cap}</div>'
                f'<pre><code class="highlight">{b["code_html"]}</code></pre></div>')
    if b["type"] == "columns":
        n = len(b["columns"])
        extra = f' {b["class"]}' if b.get("class") else ""
        cells = "".join(f"<div>{''.join(render_block(nb) for nb in col)}</div>" for col in b["columns"])
        if n in (2, 3, 5):
            return f'<div class="grid-{n}{extra}">{cells}</div>'
        return (f'<div class="{extra.strip()}" style="display:grid;grid-template-columns:repeat({n},1fr);gap:18px;height:100%;">{cells}</div>')
    if b["type"] == "card":
        heading = f'<h4>{esc(b["heading"])}</h4>' if b.get("heading") else ""
        extra = f' {b["class"]}' if b.get("class") else ""
        return f'<div class="card-line{extra}">{heading}{"".join(render_block(nb) for nb in b["blocks"])}</div>'
    return _render_block(b)


def slide_html(slide, num):
    blocks = "".join(render_block(b) for b in slide["blocks"])
    if slide.get("cover"):
        return f'<div class="cover"><div class="kicker">{esc(slide.get("unit", ""))}</div><h1>{slide["title"]}</h1>{blocks}</div>'
    return (f'<div class="chapter-tab"><div class="num">{num:02d}</div><div class="code">{esc(slide.get("code", ""))}</div></div>'
            f'<div class="slide-eyebrow">{esc(slide.get("unit", ""))}</div>'
            f'<h1 class="slide-title">{slide["title"]}</h1><div class="title-rule"></div>'
            f'<div class="slide-body">{blocks}</div>')


# ============================================================================
# 8. PAGINATION
# ============================================================================
# Fallback height estimate (fraction of one slide body), fitted to the hand-checked splits of the
# original decks: (base, per 100 characters, per item/row/line).
ESTIMATE_W = {
    "text": (0.05, 0.045, 0.02), "callout": (0.12, 0.045, 0.0), "pullquote": (0.07, 0.18, 0.0),
    "list": (0.08, 0.04, 0.055), "table": (0.12, 0.03, 0.06), "code": (0.10, 0.0, 0.035),
    "flow": (0.33, 0.0, 0.04), "steps": (0.08, 0.04, 0.06), "image": (1.0, 0.0, 0.0),
}


def plain(h):
    return re.sub(r"<[^>]+>", "", h or "")


def est_height(b, scale=1.0):
    t = b["type"]
    if t == "columns":
        n = len(b["columns"])
        return 0.03 + max(sum(est_height(x, scale * n) for x in col) for col in b["columns"])
    if t == "card":
        return 0.06 + sum(est_height(x, scale) for x in b["blocks"])
    base, per_chars, per_item = ESTIMATE_W.get(t, (0.2, 0.04, 0.0))
    if t in ("text", "callout", "pullquote"):
        chars, items = len(plain(b.get("html"))), b.get("html", "").count("<p>")
    elif t in ("list", "steps"):
        chars, items = sum(len(plain(i)) for i in b["items"]), len(b["items"])
    elif t == "table":
        chars, items = sum(len(c) for r in b["rows"] for c in r), len(b["rows"]) + 1
    elif t == "code":
        chars, items = 0, b["code"].count("\n") + 1
    elif t == "flow":
        chars, items = 0, len(b["steps"])
    else:
        chars, items = 0, 0
    return base + per_chars * scale * chars / 100 + per_item * items


def split_estimate(slide):
    parts, cur, h = [], [], 0.0
    for b in slide["blocks"]:
        hb = est_height(b)
        if cur and h + hb > 1.0:
            parts.append(cur)
            cur, h = [], 0.0
        cur.append(b)
        h += hb
    return parts + [cur] if cur else parts or [[]]


MEASURE_JS = """async ([pieces]) => {
  const panel = document.getElementById('panel-slide');
  const out = [];
  for (const p of pieces) {
    // p = {head, blocks:[html...]}; greedily fill parts while the slide body does not overflow
    const parts = []; let cur = [];
    const fits = async (arr) => {
      panel.innerHTML = p.head + '<div class="slide-body">' + arr.join('') + '</div>';
      const imgs = [...panel.querySelectorAll('img')];
      await Promise.all(imgs.map(im => im.complete ? 0 : new Promise(r => { im.onload = im.onerror = r; })));
      const body = panel.querySelector('.slide-body');
      return body.scrollHeight <= body.clientHeight + 1;
    };
    for (let i = 0; i < p.blocks.length; i++) {
      if (cur.length && !(await fits(cur.concat([p.blocks[i]])))) { parts.push(cur.length); cur = []; }
      cur.push(p.blocks[i]);
    }
    if (cur.length || !parts.length) parts.push(cur.length);
    out.push(parts);
  }
  return out;
}"""


class Measurer:
    """Splits slides by rendering them in headless Chromium with the decks' own CSS."""

    def __init__(self):
        from playwright.sync_api import sync_playwright
        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch()
        self.page = self._browser.new_page(viewport={"width": 1280, "height": 800})

    def mermaid_png(self, code):
        """Draw a Mermaid diagram (black and white, Times) and return it as a PNG."""
        page = self._browser.new_page(device_scale_factor=2, viewport={"width": 1400, "height": 1000})
        try:
            page.set_content('<html><body style="margin:0;background:#fff"><div id="d" style="display:inline-block;padding:12px"></div></body></html>')
            page.add_script_tag(path=str(TEMPLATES / "mermaid.min.js"))
            plain = "\n".join(ln for ln in code.splitlines()      # the site is black and white: drop colour directives
                              if not re.match(r"\s*(style|classDef|linkStyle|class)\s", ln))
            page.evaluate(MERMAID_JS, plain)
            return page.locator("#d").screenshot(omit_background=False)
        finally:
            page.close()

    def split(self, slides):
        """slides -> list of part sizes (block counts) for each slide, measured in one deck page."""
        shell = (TEMPLATES / "deck.html").read_text(encoding="utf-8")
        probe = SITE / "_measure.html"
        probe.write_text(shell.replace("__SLIDES__", "[]").replace("__META__", "{}")
                         .replace("__TITLE__", "").replace("__KICKER__", "").replace("__COUNT__", "0")
                         .replace('<script src="site.js"></script>', ""), encoding="utf-8")
        try:
            self.page.goto(probe.as_uri())
            pieces = [{"head": (f'<div class="chapter-tab"><div class="num">88</div><div class="code">{esc(s.get("code", ""))}</div></div>'
                                f'<div class="slide-eyebrow">{esc(s.get("unit", ""))}</div>'
                                f'<h1 class="slide-title">{s["title"]} (8/8)</h1><div class="title-rule"></div>'),
                       "blocks": [render_block(b) for b in s["blocks"]]} for s in slides]
            return self.page.evaluate(MEASURE_JS, [pieces])
        finally:
            probe.unlink()

    def layout(self, page_htmls):
        """Final pages -> where each top-level block sits in the slide body (browser px), for the PowerPoint."""
        shell = (TEMPLATES / "deck.html").read_text(encoding="utf-8")
        probe = SITE / "_measure.html"
        probe.write_text(shell.replace("__SLIDES__", "[]").replace("__META__", "{}")
                         .replace("__TITLE__", "").replace("__KICKER__", "").replace("__COUNT__", "0")
                         .replace('<script src="site.js"></script>', ""), encoding="utf-8")
        try:
            self.page.goto(probe.as_uri())
            return self.page.evaluate(LAYOUT_JS, [page_htmls])
        finally:
            probe.unlink()

    def close(self):
        self._browser.close()
        self._pw.stop()


MERMAID_JS = """async (code) => {
  mermaid.initialize({startOnLoad: false, theme: 'neutral', securityLevel: 'strict',
                      themeVariables: {fontFamily: '"Times New Roman", Times, serif', fontSize: '18px'}});
  const {svg} = await mermaid.render('diagram', code);
  document.getElementById('d').innerHTML = svg;
}"""


LAYOUT_JS = """async ([htmls]) => {
  const panel = document.getElementById('panel-slide');
  const out = [];
  for (const h of htmls) {
    panel.innerHTML = h;
    const imgs = [...panel.querySelectorAll('img')];
    await Promise.all(imgs.map(im => im.complete ? 0 : new Promise(r => { im.onload = im.onerror = r; })));
    const body = panel.querySelector('.slide-body');
    if (!body) { out.push(null); continue; }
    const B = body.getBoundingClientRect();
    out.push({body: [B.width, B.height], blocks: [...body.children].map(el => {
      const r = el.getBoundingClientRect();
      return [r.left - B.left, r.top - B.top, r.width, r.height]; })});
  }
  return out;
}"""


def paginate(slides, measurer):
    """Raw slides -> deck pages. Cover slides are never split; split parts get "(k/n)" titles and only
    the first part carries the speaker notes."""
    to_measure = [s for s in slides if not s.get("cover") and len(s["blocks"]) > 1]
    if measurer is not None:
        sizes = dict(zip(map(id, to_measure), measurer.split(to_measure)))
    else:
        sizes = {id(s): [len(p) for p in split_estimate(s)] for s in to_measure}
    pages = []
    for s in slides:
        counts = sizes.get(id(s), [len(s["blocks"])])
        n, start = len(counts), 0
        for k, c in enumerate(counts, 1):
            pg = dict(s, blocks=s["blocks"][start:start + c])
            start += c
            if n > 1:
                pg["part"] = [k, n]
                if k > 1:
                    pg["title"] = f'{s["title"]} ({k}/{n})'
                    pg["notes"] = "<p><i>(continued, see part 1)</i></p>"
            pages.append(pg)
    return pages


# ============================================================================
# 9. DECK PAGES
# ============================================================================

def script_json(obj):
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


DIAGRAMS = SITE / "diagrams"


def mermaid_images(blocks, measurer):
    """Replace ```mermaid code blocks with the drawn diagram (cached by the hash of its code)."""
    out = []
    for b in blocks:
        if b["type"] == "code" and b.get("language") == "mermaid":
            png = DIAGRAMS / f'{hashlib.sha1(b["code"].encode("utf-8")).hexdigest()[:12]}.png'
            keep(png)
            if not png.exists():
                if util.CHECK or measurer is None:
                    util.changed.append(png.relative_to(util.ROOT).as_posix())
                    out.append(b)
                    continue
                emit_bytes(png, measurer.mermaid_png(b["code"]))
            img = {"type": "image", "src": f"diagrams/{png.name}", "alt": b.get("caption", "Diagram")}
            if b.get("caption"):
                img["caption"] = b["caption"]
            out.append(img)
            continue
        for col in b.get("columns", []):
            col[:] = mermaid_images(col, measurer)
        if b.get("blocks"):
            b["blocks"] = mermaid_images(b["blocks"], measurer)
        out.append(b)
    return out


def build_deck(md_path, measurer):
    parsed = parse_file(md_path)
    deck = parsed["deck"]
    for s in parsed["slides"]:
        s["blocks"] = prepare(drop_unfinished(mermaid_images(s["blocks"], measurer)))
    pages = paginate(parsed["slides"], measurer)
    slides = [{"slideHtml": slide_html(p, i), "notesBody": p.get("notes", ""), "unit": p.get("unit", ""),
               "slideTitle": plain(p["title"])} for i, p in enumerate(pages, 1)]
    if not NO_PPTX:
        layouts = measurer.layout([s["slideHtml"] for s in slides]) if measurer else [None] * len(pages)
        buf = io.BytesIO()
        lecture_pptx.build(pages, deck, layouts, lambda src: next((p.resolve() for p in (NOTES / src, SITE / src) if p.exists()), None),
                           buf)
        emit_pptx(PPT / f"{md_path.stem}.pptx", buf.getvalue())
    title = deck.get("title") or parsed["slides"][0]["title"]
    page = ((TEMPLATES / "deck.html").read_text(encoding="utf-8")
            .replace("__TITLE__", esc(title)).replace("__KICKER__", esc(deck.get("kicker", "")))
            .replace("__COUNT__", str(len(slides)))
            .replace("__META__", script_json({"stem": md_path.stem, "title": title}))
            .replace("__SLIDES__", script_json(slides)))
    return page, {"stem": md_path.stem, "deck": deck, "count": len(slides), "title": title}


def index_page(decks):
    cards = []
    for d in sorted(decks, key=lambda d: d["stem"]):
        m = d["deck"]
        num = f'{int(m.get("class_number") or d["stem"][:2]):02d}'
        topics = "".join(f'<span class="deck-card-topic">{esc(t)}</span>' for t in (m.get("topics") or [])[:6])
        cards.append(f'<a class="deck-card" href="{d["stem"]}.html">\n  <div class="deck-card-header">\n'
                     f'    <div class="deck-card-num">{num}</div>\n    <div class="deck-card-badge">{d["count"]} slides</div>\n  </div>\n'
                     f'  <div class="deck-card-body">\n    <div class="deck-card-title">{esc(d["title"])}</div>\n'
                     f'    <div class="deck-card-desc">{esc(m.get("description", ""))}</div>\n'
                     f'    <div class="deck-card-topics">{topics}</div>\n  </div>\n</a>\n')
    return (TEMPLATES / "deck_index.html").read_text(encoding="utf-8").replace("__CARDS__", "".join(cards))


def emit(path, text):
    _emit(path, N.apply(path, text))


def pptx_signature(blob):
    """Zip contents minus docProps/core.xml, whose save timestamp changes on every build."""
    z = zipfile.ZipFile(io.BytesIO(blob))
    return {n: z.read(n) for n in z.namelist() if n != "docProps/core.xml"}


def emit_pptx(path, blob):
    emit_bytes(path, blob, same=lambda a, b: pptx_signature(a) == pptx_signature(b))


def deck_info(md_path):
    """Front matter only (for the index entries of decks that are not being rebuilt)."""
    parsed = parse_file(md_path)
    built = SITE / f"{md_path.stem}.html"
    m = re.search(r'id="slide-counter">01 / (\d+)<', built.read_text(encoding="utf-8")) if built.exists() else None
    deck = parsed["deck"]
    return {"stem": md_path.stem, "deck": deck, "count": int(m.group(1)) if m else 0,
            "title": deck.get("title") or parsed["slides"][0]["title"]}


def run():
    measurer = None
    if not ESTIMATE:
        try:
            measurer = Measurer()
        except Exception as e:                                    # no Playwright / Chromium
            print(f"(browser measuring unavailable: {str(e).splitlines()[0][:120]}; using the height estimate)")
    decks = []
    try:
        for md_path in sorted(NOTES.glob("[0-9][0-9]_*.md")):
            if ONLY and md_path.stem[:2] not in ONLY:
                decks.append(deck_info(md_path))
                from .util import keep
                keep(SITE / f"{md_path.stem}.html")
                keep(PPT / f"{md_path.stem}.pptx")
                continue
            page, info = build_deck(md_path, measurer)
            emit(SITE / f"{md_path.stem}.html", page)
            decks.append(info)
            print(f"  {md_path.stem}: {info['count']} slides", flush=True)
    finally:
        if measurer is not None:
            measurer.close()
    emit(SITE / "index.html", index_page(decks))
    if hidden_images:
        print(f"{len(hidden_images)} image(s) left out because the file is missing or still a placeholder "
              f"(--show-unfinished-images to include them)")
