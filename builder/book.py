"""The online book (book/index.html) from the LaTeX textbook.

source/textbook/front-matter/*.tex, parts/*/*.tex  ->  book/index.html
source/textbook/book-inserts.json   online-only diagrams and "From the Archives" boxes
each topic's quizbank.xml           first three questions = "Check Your Understanding"
templates/book.html                 page shell: CSS, sidebar, search, practice-question script
TikZ/forest figures in the .tex     ->  book/figures/<label>.svg
                                        (needs latex + dvisvgm from MiKTeX or TeX Live; an SVG is only
                                        rebuilt when its figure source changes)

The downloads table at the end links every per-topic file that exists, so it runs after the downloads step.
"""
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

from . import course as C
from . import nav as N
from . import util
from .materials import topic_quiz
from .paths import BOOK, DOWNLOADS as SITE_DOWNLOADS, TEMPLATES, TEXTBOOK_SRC as TEX
from .util import emit, keep

OUT = BOOK / "index.html"
FIGS = BOOK / "figures"
TEMPLATE = TEMPLATES / "book.html"
INSERTS = TEX / "book-inserts.json"
PRACTICE_PER_TOPIC = 3

unknown = Counter()   # LaTeX commands this converter does not understand (reported, then dropped)
figures = []          # (name, drawing source) for every TikZ/forest figure, in book order
CE = ' contenteditable="true"'


# ------------------------------------------------------------------ TeX reading helpers --
def read_group(s, i, open_="{", close="}"):
    """s[i] (after optional whitespace) is open_; return (contents, index after the matching close)."""
    while i < len(s) and s[i] in " \t\n":
        i += 1
    if i >= len(s) or s[i] != open_:
        return None, i
    depth, j = 0, i
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == open_:
            depth += 1
        elif c == close:
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise ValueError(f"unbalanced {open_} near: {s[i:i + 80]!r}")


def read_opt(s, i):
    """Optional [..] argument: returns (contents or None, index)."""
    k = i
    while k < len(s) and s[k] in " \t":
        k += 1
    if k < len(s) and s[k] == "[":
        return read_group(s, k, "[", "]")
    return None, i


def env_body(s, i, name):
    """i is just after \\begin{name}; return (body, index after the matching \\end{name})."""
    pat = re.compile(r"\\(begin|end)\{" + re.escape(name) + r"\}")
    depth = 1
    for m in pat.finditer(s, i):
        depth += 1 if m.group(1) == "begin" else -1
        if depth == 0:
            return s[i:m.start()], m.end()
    raise ValueError(f"no \\end{{{name}}}")


def split_top(s, sep):
    """Split s on the regex sep, ignoring matches inside braces or \\begin..\\end blocks."""
    parts, depth, last = [], 0, 0
    i = 0
    rx = re.compile(sep)
    while i < len(s):
        c = s[i]
        if c == "\\" and s.startswith("\\begin{", i):
            depth += 1
        elif c == "\\" and s.startswith("\\end{", i):
            depth -= 1
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        if depth == 0:
            m = rx.match(s, i)
            if m:
                parts.append(s[last:i])
                last = i = m.end()
                continue
        i += 2 if c == "\\" and not s.startswith("\\begin{", i) and not s.startswith("\\end{", i) else 1
    parts.append(s[last:])
    return parts


def strip_comments(t):
    # A TeX comment also swallows the line break and the next line's indentation.
    return re.sub(r"(?<!\\)%[^\n]*(\n[ \t]*)?", "", t)


def plain(h):
    """Rendered HTML -> plain text (for alt text and insert matching)."""
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", h))).strip()


def slug(tid):
    return tid.replace(".", "-")


# ------------------------------------------------------------------------ inline TeX -> HTML --
WRAP = {"textbf": "strong", "emph": "em", "textit": "em", "textsuperscript": "sup", "underline": "u"}
SYMBOL = {"S": "§", "pounds": "£", "texteuro": "€", "textregistered": "®", "textdegree": "°",
          "ldots": "…", "dots": "…", "checkmark": "✓", "lbrack": "[", "rbrack": "]",
          "textbackslash": "\\", "times": "×", "quad": " ", "qquad": "  ", "textendash": "–",
          "textemdash": "—", "o": "ø", "O": "Ø", "ss": "ß", "ae": "æ", "LaTeX": "LaTeX", "TeX": "TeX"}
DROP0 = {"small", "scriptsize", "footnotesize", "tiny", "large", "Large", "LARGE", "huge", "Huge",
         "normalsize", "sffamily", "bfseries", "ttfamily", "itshape", "upshape", "normalfont", "rmfamily",
         "centering", "noindent", "medskip", "bigskip", "smallskip", "par", "hfill", "raggedright",
         "raggedleft", "newline", "clearpage", "newpage", "protect", "relax", "today"}
DROP1 = {"label", "index", "vspace", "hspace", "phantom", "color"}
ACCENT = {'"': "\u0308", "'": "\u0301", "`": "\u0300", "^": "\u0302", "~": "\u0303", "c": "\u0327"}


def math(s):
    """TeX math for MathJax. MathJax's \\text{} is literal, so unescape \\_ there."""
    s = re.sub(r"\\(text|textrm|texttt|mathrm)\{([^{}]*)\}", lambda m: f"\\{m.group(1)}{{{m.group(2).replace(chr(92) + '_', '_')}}}", s)
    return html.escape(s)


def inline(s, code=False):
    out, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c == "\\":
            m = re.compile(r"\\([A-Za-z]+)\*?").match(s, i)
            if not m:
                nxt = s[i + 1] if i + 1 < n else ""
                if nxt == "\\":
                    out.append("<br>")
                    i += 2
                    _, i = read_opt(s, i)
                elif nxt in "%$&#_{}":
                    out.append(html.escape(nxt))
                    i += 2
                elif nxt in " \n":
                    out.append(" ")
                    i += 2
                elif nxt == ",":
                    out.append("\u2009")
                    i += 2
                elif nxt in "@/":
                    i += 2
                elif nxt in ACCENT:
                    arg, j = read_group(s, i + 2)
                    if arg is None:
                        arg, j = s[i + 2:i + 3], i + 3
                    out.append(html.escape(arg) + ACCENT[nxt])
                    i = j
                elif nxt == "(":
                    j = s.index("\\)", i)
                    out.append("\\(" + html.escape(s[i + 2:j]) + "\\)")
                    i = j + 2
                else:
                    unknown["\\" + nxt] += 1
                    i += 2
                continue
            name, i = m.group(1), m.end()
            if name in WRAP:
                arg, i = read_group(s, i)
                out.append(f"<{WRAP[name]}>{inline(arg, code)}</{WRAP[name]}>")
            elif name == "texttt":
                arg, i = read_group(s, i)
                out.append(f"<code>{inline(arg, code=True)}</code>")
            elif name == "ref":
                arg, i = read_group(s, i)
                if arg.startswith("ch:"):
                    out.append(f'<a href="#ch-{slug(arg[3:])}">{arg[3:]}</a>')
                else:
                    unknown["\\ref{" + arg.split(":")[0] + ":}"] += 1
            elif name == "srccite":
                key, i = read_group(s, i)
                num, i = read_group(s, i)
                out.append(f'<sup class="src-cite"><a href="#src-{slug(key)}-{num}">[{num}]</a></sup>')
            elif name == "srcitem":
                _, i = read_group(s, i)
                _, i = read_group(s, i)
            elif name == "answerlabel":
                arg, i = read_group(s, i)
                out.append(f' <code class="answer-code">{html.escape(arg)}</code>')
            elif name == "url":
                arg, i = read_group(s, i)
                out.append(f'<a href="{html.escape(arg)}">{html.escape(arg)}</a>')
            elif name == "href":
                url, i = read_group(s, i)
                txt, i = read_group(s, i)
                out.append(f'<a href="{html.escape(url)}">{inline(txt, code)}</a>')
            elif name in SYMBOL:
                out.append(SYMBOL[name])
                if s.startswith("{}", i):
                    i += 2
            elif name in DROP0:
                pass
            elif name in DROP1:
                _, i = read_group(s, i)
            elif name == "addcontentsline":
                for _ in range(3):
                    _, i = read_group(s, i)
            else:
                unknown["\\" + name] += 1
            continue
        if c == "$":
            j = i + 1
            while j < n and not (s[j] == "$" and s[j - 1] != "\\"):
                j += 1
            out.append("\\(" + math(s[i + 1:j]) + "\\)")
            i = j + 1
            continue
        if c == "{":
            arg, i = read_group(s, i)
            out.append(inline(arg, code))
            continue
        if c == "}":
            i += 1
            continue
        if c == "~":
            out.append("\u00a0")
            i += 1
            continue
        if not code:
            for tex, uni in (("---", "—"), ("--", "–"), ("``", "“"), ("''", "”"), ("`", "‘"), ("'", "’")):
                if s.startswith(tex, i):
                    out.append(uni)
                    i += len(tex)
                    break
            else:
                out.append(html.escape(c, quote=False))
                i += 1
            continue
        out.append(html.escape(c, quote=False))
        i += 1
    return "".join(out)


# ------------------------------------------------------------------------- block TeX -> HTML --
stash = []   # pre-rendered verbatim blocks (code listings), referenced as \x00n\x00


def stash_verbatim(t):
    # A font-size group around a listing ({\scriptsize \begin{verbatim}..\end{verbatim}}) only matters in print.
    t = re.sub(r"\{\\(?:scriptsize|footnotesize|small|tiny)\s*(\\begin\{(verbatim|lstlisting)\}.*?\\end\{\2\})\s*\}",
               r"\1", t, flags=re.S)

    def lst(m):
        opts, body = m.group(1) or "", m.group(2)
        lang = re.search(r"language=\{?([A-Za-z+#]+)", opts)
        cap = re.search(r"caption=", opts)
        caption = ""
        if cap:
            k = cap.end()
            if opts[k:k + 1] == "{":
                caption, _ = read_group(opts, k)
            else:
                caption = opts[k:].split(",")[0]
        body = body.strip("\n")
        h = '<figure class="code-figure">'
        if lang:
            h += f'<div class="code-lang">{html.escape(lang.group(1))}</div>'
        h += f'<pre class="code-block"{CE}><code>{html.escape(body)}</code></pre>'
        if caption:
            h += f'<div class="code-caption">{inline(strip_comments(caption))}</div>'
        stash.append(h + "</figure>")
        return f"\n\n\x00{len(stash) - 1}\x00\n\n"

    t = re.sub(r"\\begin\{lstlisting\}(?:\[((?:[^\[\]]|\{[^{}]*\})*)\])?\n?(.*?)\\end\{lstlisting\}", lst, t, flags=re.S)

    def verb(m):
        stash.append(f'<pre class="code-block"{CE}><code>{html.escape(m.group(1).strip(chr(10)))}</code></pre>')
        return f"\n\n\x00{len(stash) - 1}\x00\n\n"

    return re.sub(r"\\begin\{verbatim\}(.*?)\\end\{verbatim\}", verb, t, flags=re.S)


def unwrap(blocks_):
    """A list item / cell that rendered to one paragraph is shown without the <p>."""
    if len(blocks_) == 1:
        m = re.fullmatch(rf"<p{CE}>(.*)</p>", blocks_[0], flags=re.S)
        if m:
            return m.group(1), True
    return "\n".join(blocks_), False


def render_list(body, tag, cls=None):
    _, k = read_opt(body, 0)
    opts = body[:k]
    items = split_top(body[k:], r"\\item\b")[1:]
    sources = "lbrack" in opts
    lis = []
    for it in items:
        attrs = ""
        num = None
        m = re.match(r"\s*\\srcitem\{([^}]*)\}\{([^}]*)\}", it)
        if m:
            attrs = f' id="src-{slug(m.group(1))}-{m.group(2)}"'
            num = m.group(2)
            it = it[m.end():]
        inner, single = unwrap(blocks(it))
        if num:
            inner = f'<span class="src-num">[{num}]</span> ' + inner
        lis.append(f"<li{attrs}{CE if single else ''}>{inner}</li>")
    cls = cls or ("sources" if sources else None)
    return f"<{tag}{f' class={chr(34)}{cls}{chr(34)}' if cls else ''}>{''.join(lis)}</{tag}>"


def render_table(body, caption=None):
    m = re.search(r"\\begin\{tabular\}", body)
    _, k = read_group(body, m.end())          # column spec
    tab, _ = env_body(body, k, "tabular")
    head, rows = [], []
    seen_mid = "\\midrule" not in tab
    for row in split_top(tab, r"\\\\"):
        row = row.strip()
        if "\\midrule" in row:
            seen_mid = True
        row = re.sub(r"\\(toprule|midrule|bottomrule|hline)", "", row).strip()
        if not row:
            continue
        cells = [inline(c.strip()) for c in split_top(row, r"(?<!\\)&")]
        (rows if seen_mid else head).append(cells)
    h = f'<figure class="table-figure"><table>'
    if head:
        h += "<thead>" + "".join("<tr>" + "".join(f"<th{CE}>{c}</th>" for c in r) + "</tr>" for r in head) + "</thead>"
    h += "<tbody>" + "".join("<tr>" + "".join(f"<td{CE}>{c}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table>"
    if caption:
        h += f"<figcaption{CE}>{inline(caption)}</figcaption>"
    return h + "</figure>"


def take_cmd(body, name):
    """Remove \\name{...} from body; return (argument or None, body without it)."""
    m = re.search(r"\\" + name + r"\b", body)
    if not m:
        return None, body
    arg, j = read_group(body, m.end())
    return arg, body[:m.start()] + body[j:]


def render_figure(body, topic):
    caption, body = take_cmd(body, "caption")
    label, body = take_cmd(body, "label")
    if "\\begin{tabular}" in body:
        return render_table(body, caption)
    drawing = re.sub(r"\\centering\b", "", body).strip()
    name = (label or "").split(":", 1)[-1] or f"{topic}-fig{sum(1 for f in figures if f[0].startswith(topic)) + 1}"
    name = re.sub(r"[^A-Za-z0-9.-]+", "-", name)
    figures.append((name, drawing))
    cap = inline(caption or "")
    return (f'<figure class="diagram"><img src="figures/{name}.svg" alt="{html.escape(plain(cap))}" '
            f'loading="lazy"><figcaption{CE}>{cap}</figcaption></figure>')


def render_box(kind, label, body):
    return f'<div class="box box-{kind}"><p class="box-label">{label}</p>{"".join(blocks(body))}</div>'


def render_env(name, body, ctx):
    if name in ("enumerate", "itemize"):
        return render_list(body, "ol" if name == "enumerate" else "ul")
    if name == "reviewquestions":
        return f'<div class="review-questions">{render_list(body, "ol")}</div>'
    if name == "answerkey":
        return f'<div class="answer-key"><p class="box-label">Answer Key</p>{render_list(body, "ol")}</div>'
    if name == "definition":
        title, k = read_group(body, 0)
        return render_box("definition", f"Definition: {inline(title)}", body[k:])
    if name in ("misconception", "example"):
        title, k = read_opt(body, 0)
        default = "Common Misconception" if name == "misconception" else "Worked Example"
        return render_box(name, inline(title) if title else default, body[k:])
    if name == "apalignment":
        unit, k = read_group(body, 0)
        topic, k = read_group(body, k)
        objs = "".join(
            f'<li><span class="obj-code">{html.escape(c)}</span> <span class="obj-skill">{inline(sk)}</span> '
            f'<span{CE}>{inline(t)}</span></li>'
            for c, sk, t in re.findall(r"\\apobjective\{([^}]*)\}\{([^}]*)\}\{((?:[^{}]|\{[^{}]*\})*)\}", body))
        return (f'<aside class="ap-alignment"><h4>AP Course Alignment</h4>'
                f'<p class="ap-topic">{inline(unit)} · {inline(topic)}</p><ul>{objs}</ul>'
                f'<p class="ap-note">Objective codes (e.g., 1.1.A) are this book\'s own numbering, keyed to the '
                f'topic number. Objective content is paraphrased from the <em>AP Cybersecurity Course '
                f'Framework</em> (College Board, AP Career Kickstart).</p></aside>')
    if name == "figure":
        _, k = read_opt(body, 0)
        return render_figure(body[k:], ctx["topic"])
    if name in ("tikzpicture", "forest"):
        return render_figure(f"\\begin{{{name}}}{body}\\end{{{name}}}", ctx["topic"])
    if name == "table":
        _, k = read_opt(body, 0)
        caption, rest = take_cmd(body[k:], "caption")
        return render_table(rest, caption)
    if name == "tabular":
        return render_table(f"\\begin{{tabular}}{body}\\end{{tabular}}")
    if name == "center":
        if "\\begin{tabular}" in body:
            return render_table(body)
        return f'<div class="center">{"".join(blocks(body, ctx))}</div>'
    if name == "flushright":
        return f'<div class="flushright">{"".join(blocks(body, ctx))}</div>'
    unknown[f"\\begin{{{name}}}"] += 1
    return "".join(blocks(body, ctx))


BREAK = re.compile(r"\n[ \t]*\n\s*|\x00\d+\x00|\\\[|\\begin\{|\\(?:sub)?section\*?\{|\\chapterquote\{")


def blocks(s, ctx=None):
    """Block-level TeX -> list of HTML block strings."""
    ctx = ctx or {"topic": ""}
    out, para, i = [], [], 0

    def flush():
        txt = "".join(para).strip()
        para.clear()
        if txt and re.sub(r"\\(label|chaptertopic)\{[^}]*\}|\\(centering|noindent|medskip|bigskip|smallskip)\b", "", txt).strip():
            out.append(f"<p{CE}>{inline(txt).strip()}</p>")

    while i < len(s):
        m = BREAK.search(s, i)
        if not m:
            para.append(s[i:])
            break
        para.append(s[i:m.start()])
        tok = m.group(0)
        if tok.startswith("\x00"):
            flush()
            out.append(stash[int(tok[1:-1])])
            i = m.end()
        elif tok == "\\[":
            flush()
            j = s.index("\\]", m.end())
            out.append(f'<div class="math-block">\\[{math(s[m.end():j].strip())}\\]</div>')
            i = j + 2
        elif tok.startswith("\\begin"):
            name, j = read_group(s, m.end() - 1)
            body, i = env_body(s, j, name)
            flush()
            out.append(render_env(name, body, ctx))
        elif tok.startswith("\\chapterquote"):
            q, j = read_group(s, m.end() - 1)
            who, i = read_group(s, j)
            flush()
            out.append(f'<blockquote class="chapter-quote"><p{CE}>{inline(q)}</p><cite{CE}>{inline(who)}</cite></blockquote>')
        elif tok.startswith("\\"):
            title, i = read_group(s, m.end() - 1)
            flush()
            tag = "h4" if tok.startswith("\\sub") else "h3"
            out.append(f"<{tag}{CE}>{inline(title)}</{tag}>")
        else:
            flush()
            i = m.end()
    flush()
    return out


def parse_tex(path):
    t = strip_comments(stash_verbatim(path.read_text(encoding="utf-8")))
    return t


# --------------------------------------------------------------------------- book pieces --
def load_inserts():
    by_topic = {}
    for ins in json.loads(INSERTS.read_text(encoding="utf-8"))["inserts"]:
        by_topic.setdefault(ins["topic"], []).append(ins)
    return by_topic


def insert_html(ins):
    if ins["kind"] == "diagram":
        return (f'<figure class="diagram"><img src="{html.escape(ins["src"])}" alt="{html.escape(ins["alt"])}" '
                f'loading="lazy"><figcaption{CE}>{html.escape(ins["caption"])}</figcaption></figure>')
    body = ins["html"].replace("<p>", f"<p{CE}>")
    return f'<div class="box box-{ins["kind"]}"><p class="box-label">{html.escape(ins["title"])}</p>{body}</div>'


def norm(s):
    return re.sub(r"\s+", " ", s.replace("’", "'").replace("“", '"').replace("”", '"')).strip()


def place_inserts(out, inserts, tid):
    last = {}
    for ins in inserts:
        key = (ins["after_heading"], ins["after_text"])
        if key in last:
            pos = last[key]
        else:
            heads = [k for k, b in enumerate(out) if re.match(r"<h[34]", b) and plain(b) == ins["after_heading"]]
            if not heads:
                sys.exit(f"inserts.json: topic {tid} has no heading {ins['after_heading']!r}")
            pos = heads[0]
            if ins["after_text"]:
                want = norm(ins["after_text"])
                for k in range(pos + 1, len(out)):
                    if re.match(r"<h[34]", out[k]):
                        break
                    if norm(plain(out[k])).startswith(want):
                        pos = k
                        break
                else:
                    sys.exit(f"inserts.json: topic {tid} has no paragraph starting {ins['after_text'][:40]!r} "
                             f"under {ins['after_heading']!r}")
        out.insert(pos + 1, insert_html(ins))
        last[key] = pos + 1


def practice_html(tid):
    path = C.topic(tid)["src"] / "quizbank.xml"
    if not path.exists():
        return ""
    qs = topic_quiz(path)["questions"][:PRACTICE_PER_TOPIC]
    h = f'<div class="practice-check" aria-label="Check your understanding for Topic {tid}">'
    for n, q in enumerate(qs, 1):
        h += f'<div class="pq-question" data-answer="{q["answer_key"]}"><p class="pq-stem"{CE}>{n}. {html.escape(q["stem"])}</p><div class="pq-choices">'
        for c in q["choices"]:
            h += (f'<button type="button" class="pq-choice" data-key="{c["key"]}"><span class="pq-key">{c["key"]}.</span> '
                  f'<span>{html.escape(c["text"])}</span></button>')
        h += (f'</div><div class="pq-explain" hidden>{html.escape(q["explanation"])}</div>'
              f'<div class="pq-feedback" role="status" hidden></div></div>')
    return h + "</div>"


def chapter(path, unit, inserts):
    t = parse_tex(path)
    title, k = read_group(t, t.index("\\chapter{") + len("\\chapter"))
    label = re.search(r"\\label\{ch:([\d.]+)\}", t)
    tid = label.group(1) if label else re.search(r"ch-(\d+\.\d+)", path.name).group(1)
    out = blocks(t[k:], {"topic": tid})
    place_inserts(out, inserts.get(tid, []), tid)
    review = next((k for k, b in enumerate(out) if b.startswith("<h3") and plain(b) == "Review Questions"), len(out))
    pq = practice_html(tid)
    if pq:
        out[review:review] = [f"<h3{CE}>Check Your Understanding</h3>", pq]
    head = (f'<header class="topic-header"><img class="topic-cover" src="covers/topic-{slug(tid)}.svg" alt="" '
            f'loading="lazy"><h2 id="ch-{slug(tid)}"{CE}>{tid} {inline(title)}</h2></header>')
    return tid, plain(inline(title)), f'<section class="topic">{head}\n' + "\n".join(out) + "</section>"


def unit_html(udir, n, inserts):
    t = parse_tex(udir / "part.tex")
    title, k = read_group(t, t.index("\\part{") + len("\\part"))
    title = plain(inline(title))
    intro = "\n".join(blocks(t[k:]))
    chapters = [chapter(p, n, inserts) for p in sorted(udir.glob("ch-*.tex"), key=lambda p: [int(x) for x in re.findall(r"\d+", p.name.split("-")[1])])]
    head = (f'<section class="unit" id="unit-block-{n}"><header class="unit-header"><img class="unit-cover" '
            f'src="covers/unit-{n}-header.svg" alt="" loading="lazy"><h1 id="unit-{n}"{CE}>Unit {n}: {title}</h1>'
            f'</header><div class="unit-intro">{intro}</div>')
    nav = (f'<li class="nav-unit"><a href="#unit-{n}">Unit {n}: {html.escape(title)}</a><ul>\n'
           + "".join(f'<li><a href="#ch-{slug(tid)}">{tid} {html.escape(ct)}</a></li>\n' for tid, ct, _ in chapters)
           + "</ul></li>")
    return head + "".join(c[2] for c in chapters) + "</section>", nav, (n, title, [(tid, ct) for tid, ct, _ in chapters])


def front_matter():
    tp = strip_comments((TEX / "front-matter" / "titlepage.tex").read_text(encoding="utf-8"))
    tp = env_body(tp, tp.index("\\begin{titlepage}") + len("\\begin{titlepage}"), "titlepage")[0]
    lines = [plain(inline(g)) for g in re.findall(r"\{\\[A-Za-z]+(?:\\[A-Za-z]+)*(?:\\color\{[^}]*\})?\s+([^{}]+)\}", tp)]
    lines = [x for x in lines if x]
    if len(lines) < 4:
        sys.exit(f"titlepage.tex: expected title, subtitle x2, author; found {lines}")
    title, sub1, sub2, name = lines[:4]
    h = (f'<div class="titlepage">'
         f'<h1{CE}>{html.escape(title)}</h1><div class="subtitle1"{CE}>{html.escape(sub1)}</div>'
         f'<div class="subtitle2"{CE}>{html.escape(sub2)}</div><div class="author"><div class="name"{CE}>{html.escape(name)}</div>'
         f'</div></div>')
    for f in ("dedication", "about-the-author"):
        t = parse_tex(TEX / "front-matter" / f"{f}.tex")
        head, k = read_group(t, t.index("\\chapter*") + len("\\chapter*"))
        h += f'<div class="preface"><h2>{inline(head)}</h2>{"".join(blocks(t[k:]))}</div>'
    return h, title


def downloads_html(units):
    def link(rel, label):
        return f'<a href="{rel}">{label}</a>' if (BOOK / rel).exists() else ""

    def pair(rel):
        return " ".join(x for x in (link(rel + ".pdf", "PDF"), link(rel + ".docx", "DOCX")) if x) or "&ndash;"

    h = '<section class="downloads-section" id="downloads"><h2>Downloads</h2>'
    if (BOOK / "../downloads/AP_Cybersecurity_Textbook.pdf").exists():
        h += f'<div class="downloads-textbook">{store_html("../downloads/AP_Cybersecurity_Textbook.pdf", "../buy/index.html")}</div>'
    for n, title, chs in units:
        u = f"unit-{n}"
        h += (f'<div class="downloads-unit"><h3>Unit {n}: {html.escape(title)}</h3><div class="downloads-table-wrap">'
              '<table class="downloads-table"><thead><tr><th>Topic</th><th>Assignment</th><th>Quiz</th>'
              '<th>Flashcards</th></tr></thead><tbody>')
        for tid, ct in chs:
            cells = [pair(f"../downloads/{u}/Topic_{tid}_Assignment"),
                     pair(f"../downloads/{u}/Topic_{tid}_Quiz"),
                     link(f"../downloads/{u}/Topic_{tid}_Flashcards.apkg", "Anki") or "&ndash;"]
            h += f"<tr><td>{tid} {html.escape(ct)}</td>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"
        h += "</tbody></table></div></div>"
    return h + "</section>"


# ------------------------------------------------------------------------------- figures --
def figure_preamble():
    keep_pkgs = {"fontenc", "inputenc", "mathptmx", "helvet", "courier", "amsmath,amssymb", "amsmath", "amssymb",
                 "graphicx", "tikz", "pgfplots", "bytefield", "forest", "xcolor", "booktabs"}
    lines = []
    for ln in (TEX / "preamble.tex").read_text(encoding="utf-8").splitlines():
        ln = strip_comments(ln).strip()
        m = re.match(r"\\usepackage(\[[^\]]*\])?\{([^}]*)\}", ln)
        if (m and m.group(2) in keep_pkgs) or re.match(r"\\(definecolor|usetikzlibrary|pgfplotsset)\b", ln):
            lines.append(ln)
    return ("\\documentclass[dvisvgm,multi=bookfig,border=6pt]{standalone}\n" + "\n".join(lines) +
            "\n\\setlength{\\textwidth}{5.4in}\\setlength{\\linewidth}{\\textwidth}\n\\begin{document}\n")


def fig_hash(pre, drawing):
    return hashlib.sha1((pre + drawing).encode("utf-8")).hexdigest()[:16]


def build_figures():
    pre = figure_preamble()
    want = {name: fig_hash(pre, d) for name, d in figures}
    stale = [(n, d) for n, d in figures
             if not (FIGS / f"{n}.svg").exists()
             or f"<!-- book-figure {want[n]} -->" not in (FIGS / f"{n}.svg").read_text(encoding="utf-8")[:400]]
    for n in want:
        keep(FIGS / f"{n}.svg")
    if not stale:
        return []
    util.changed.extend(f"site/book/figures/{n}.svg" for n, _ in stale)
    if util.CHECK:
        return []
    if not (shutil.which("latex") and shutil.which("dvisvgm")):
        print("warning: latex/dvisvgm not found; these figures are shown as captions only:", ", ".join(n for n, _ in stale))
        return [n for n, _ in stale if not (FIGS / f"{n}.svg").exists()]
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        doc = pre + "\n".join(f"\\begin{{bookfig}}\n{d}\n\\end{{bookfig}}" for _, d in stale) + "\n\\end{document}\n"
        (tmp / "figs.tex").write_text(doc, encoding="utf-8")
        r = subprocess.run(["latex", "-interaction=nonstopmode", "-halt-on-error", "figs.tex"], cwd=tmp,
                           capture_output=True, text=True, errors="replace")
        if r.returncode != 0:
            sys.stdout.write(r.stdout[-3000:])
            raise RuntimeError("figure build failed (LaTeX error above)")
        r = subprocess.run(["dvisvgm", "--no-fonts", "--page=1-", "--output=fig-%p", "figs.dvi"], cwd=tmp,
                           capture_output=True, text=True, errors="replace")
        FIGS.mkdir(parents=True, exist_ok=True)
        for k, (name, _) in enumerate(stale, 1):
            src = tmp / f"fig-{k}.svg"
            if not src.exists():
                src = tmp / f"fig-{k:0{len(str(len(stale)))}d}.svg"
            if not src.exists():
                sys.stdout.write(r.stderr[-3000:])
                raise RuntimeError(f"dvisvgm produced no page {k} ({name})")
            svg = src.read_text(encoding="utf-8")
            svg = re.sub(r"(<\?xml[^>]*\?>)", rf"\1\n<!-- book-figure {want[name]} -->", svg, count=1)
            (FIGS / f"{name}.svg").write_text(svg, encoding="utf-8", newline="\n")
    return []


# ----------------------------------------------------------------------------------- main --
def run():
    inserts = load_inserts()
    units = sorted((d for d in (TEX / "parts").iterdir() if (d / "part.tex").exists()),
                   key=lambda d: int(re.search(r"unit-(\d+)", d.name).group(1)))
    front, book_title = front_matter()
    bodies, navs, meta = [], [], []
    for udir in units:
        n = int(re.search(r"unit-(\d+)", udir.name).group(1))
        body, nav, m = unit_html(udir, n, inserts)
        bodies.append(body)
        navs.append(nav)
        meta.append(m)
    missing = set(build_figures())
    page = "\n".join([front] + bodies + [downloads_html(meta)])
    for name in missing:   # no LaTeX and no earlier SVG: show the caption as a figure note instead
        page = re.sub(rf'<figure class="diagram"><img src="figures/{re.escape(name)}\.svg"[^>]*>'
                      rf'<figcaption{CE}>(.*?)</figcaption></figure>',
                      rf'<div class="box box-figurenote"><p class="box-label">Figure</p><p{CE}><em>\1</em></p></div>', page)
    for name, _ in figures:   # show each figure at 1.5x its printed size (CSS caps it at the column width)
        svg = FIGS / f"{name}.svg"
        w = re.search(r"<svg[^>]*\swidth='([\d.]+)pt'", svg.read_text(encoding="utf-8")[:1000]) if svg.exists() else None
        if w:
            page = page.replace(f'<img src="figures/{name}.svg"',
                                f'<img src="figures/{name}.svg" width="{round(float(w.group(1)) * 4 / 3 * 1.5)}"')
    tpl = TEMPLATE.read_text(encoding="utf-8")
    out = (tpl.replace("<title>Book · Aayat-AP-Prep</title>", f"<title>{html.escape(book_title)}</title>")
              .replace("__NAV__", "\n".join(navs)).replace("__BOOK__", page))
    emit(OUT, N.apply(OUT, out))
    if unknown:
        print("warning: unconverted LaTeX (dropped):", ", ".join(f"{k} x{v}" for k, v in unknown.most_common()))


# ------------------------------------------------------------------------------ PDF book --
PDF = SITE_DOWNLOADS / "AP_Cybersecurity_Textbook.pdf"


def store_html(rel_pdf, rel_buy):
    """The textbook block: the locked PDF and one button to the buy page (source/static/buy/index.html,
    which lists every store)."""
    return (f'<a href="{rel_pdf}">Download the textbook (PDF, password-protected)</a> '
            f'<a href="{rel_buy}">Buy the book</a>'
            ' <span class="store-note">Buy the PDF password or the ebook; after paying, the password is shown on '
            'the thank-you page. The web edition comes with the course.</span>')


def pdf_password():
    """BOOK_PDF_PASSWORD from the environment or the gitignored root .env; never stored in the repo."""
    import os
    if os.environ.get("BOOK_PDF_PASSWORD"):
        return os.environ["BOOK_PDF_PASSWORD"]
    env = util.ROOT / ".env"
    for ln in (env.read_text(encoding="utf-8").splitlines() if env.exists() else []):
        k, _, v = ln.partition("=")
        if k.strip() == "BOOK_PDF_PASSWORD" and v.strip():
            return v.strip().strip('"').strip("'")
    raise RuntimeError("BOOK_PDF_PASSWORD is not set (root .env); refusing to publish an unlocked textbook PDF")


def lock(src, dst):
    """Write src to dst encrypted with AES-256; the PDF opens only with the password buyers receive."""
    import fitz
    pw = pdf_password()
    with fitz.open(src) as doc:
        doc.save(dst, encryption=fitz.PDF_ENCRYPT_AES_256, user_pw=pw, owner_pw=pw,
                 permissions=-1, garbage=3, deflate=True)


def locked(path):
    import fitz
    with fitz.open(path) as doc:
        return doc.needs_pass


def pdf(force=False):
    """Compile source/textbook/main.tex with latexmk in a scratch folder, then lock it with the store password;
    skipped when the PDF is newer than every .tex and already locked."""
    keep(PDF)
    newest = max(p.stat().st_mtime for p in TEX.rglob("*.tex"))
    if PDF.exists() and PDF.stat().st_mtime >= newest and not force:
        if locked(PDF):
            return
        util.changed.append(PDF.relative_to(util.ROOT).as_posix())
        if not util.CHECK:   # up to date but published unlocked: lock it in place, no recompile
            with tempfile.TemporaryDirectory() as tmp:
                plain = Path(tmp) / "plain.pdf"
                shutil.copyfile(PDF, plain)
                lock(plain, PDF)
        return
    util.changed.append(PDF.relative_to(util.ROOT).as_posix())
    if util.CHECK:
        return
    if not shutil.which("latexmk"):
        raise RuntimeError("latexmk not found: install MiKTeX or TeX Live to build the textbook PDF")
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", f"-outdir={tmp}", "main.tex"],
                           cwd=TEX, capture_output=True, text=True, errors="replace")
        out = Path(tmp) / "main.pdf"
        if r.returncode != 0 or not out.exists():
            sys.stdout.write(r.stdout[-3000:])
            raise RuntimeError("LaTeX build failed (log above)")
        PDF.parent.mkdir(parents=True, exist_ok=True)
        lock(out, PDF)
