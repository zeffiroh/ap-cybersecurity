import ast
import hashlib
import html
import io
import json
import re
from string import Template

from . import course as C
from . import nav as N
from .atomtext import bullets, md, one_line, parse_atom, sections, web_code, web_prompt, web_tests, web_text
from .course import BRAND, SITE_URL
from .paths import ASSETS, TEACHER, TEMPLATES, teacher_atom, teacher_topic
from .util import dump_json, emit, emit_bytes, esc, rd, rel

TUTOR_CSS = ASSETS / "teacher" / "tutor-theme.css"

PAGE_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="stylesheet" href="{css}">
</head>
<body>
"""


def solutions():
    for a in C.atom_order():
        p = a["src"] / "problem"
        if not (p / "solution.py").exists():
            continue
        d = teacher_atom(a["id"])
        emit(d / "solution.json", dump_json({"atom_id": a["id"], "topic_id": C.tid_of(a["id"]), "title": a["title"],
                                             "solution_py": web_code(rd(p / "solution.py"))}), json_equal=True)
        path = d / "solution.html"
        text = Template(rd(TEMPLATES / "pages" / "solution.html")).substitute(
            assets=rel(d, ASSETS), aid=a["id"], tid=C.tid_of(a["id"]), title=esc(a["title"]),
            topic_page=rel(d, teacher_topic(C.tid_of(a["id"])) / "index.html"), problem_page=rel(d, N.problem_page(a)))
        emit(path, text)


POST_SCRIPT = """<script>
function toggleMode() {
  var rendered = document.getElementById("rendered");
  var source = document.getElementById("source");
  var btn = document.getElementById("mode-toggle");
  var showingSource = !source.hidden;
  rendered.hidden = !showingSource;
  source.hidden = showingSource;
  btn.textContent = showingSource ? "View Markdown" : "View the post";
}
function copyPost(btn) {
  var text = document.getElementById("pp-title").innerText + "\\n\\n" + document.getElementById("rendered").innerText;
  var done = function () { btn.textContent = "Copied"; setTimeout(function () { btn.textContent = "Copy text"; }, 1500); };
  if (navigator.clipboard) navigator.clipboard.writeText(text).then(done);
}
</script>
</body>
</html>
"""


def post_markdown(aid, a, t, kind):
    if kind == "pre":
        parts = [f"## {aid}, {a['title']}\n**Before class today.** {a['lead']}",
                 f"**The intuition to hold onto:** {t['The intuition to hold onto']}"]
        if a["misconceptions"]:
            parts.append(f"**A myth worth busting before we start:** {a['misconceptions'][0]}")
        parts.append(f"**Today's goal:** {a['objective']}\nHandout: `pre-lecture-handout.docx`.")
    else:
        parts = [f"## {aid} recap, {a['title']}\nNice work today. Here's what to lock in:",
                 "- Recap handout: `post-lecture-handout.docx`\n- Simulation: SimLab\n- Self-check quiz: due before next class",
                 f"**The big picture:** {t['The big picture']}"]
        if a["terms"]:
            parts.append("**Key terms to lock in:**\n\n" +"\n".join(f"- {x}" for x in a["terms"]))
        if a["misconceptions"]:
            parts.append("**Common misconceptions to watch for:**\n\n" +"\n".join(f"- {x}" for x in a["misconceptions"]))
        parts.append(f"**Learning objective(s):** {a['los']}")
    return "\n\n".join(parts) + "\n"


KINDS = (("pre", "Pre-Lecture", "Before class"), ("post", "Post-Lecture", "After class"))


def post_page(d, aid, a, kind, src, prev, nxt):
    tid = C.tid_of(aid)
    tp = C.topic(tid)
    label = dict((k, l) for k, _, l in KINDS)
    other = "post" if kind == "pre" else "pre"
    blog = rel(d, TEACHER / "blog.html")
    navlink = lambda x, cls, arrow: (f'<a class="{cls}" href="{rel(d, teacher_atom(x[0]) / (kind + "-lecture-post.html"))}">'
                                     f'<small>{arrow}</small><span class="pp-nid">{esc(x[0])}</span>{esc(x[1])}</a>') if x else "<span></span>"
    body_md = src.split("\n", 1)[1]
    return (PAGE_HEAD.format(title=f"{aid} {label[kind]} · {esc(a['title'])} · {BRAND}", css=rel(d, TUTOR_CSS)).replace("<body>", '<body class="pp">')
            + f'<nav class="pp-top"><div class="pp-crumb"><a href="{blog}">Blog</a><span>/</span>'
              f'<a href="{rel(d, teacher_topic(tid) / "index.html")}">{tid} teacher page</a><span>/</span>{aid}</div>'
              '<div class="pp-tools"><button class="pp-btn" onclick="copyPost(this)">Copy text</button>'
              '<button class="pp-btn" id="mode-toggle" onclick="toggleMode()">View Markdown</button></div></nav>\n'
              f'<header class="pp-hero"><div class="pp-switch">'
              + "".join(f'<a class="{"on" if k == kind else ""}" href="{k}-lecture-post.html">{l}</a>' for k, _, l in KINDS)
              + f'</div><div class="pp-id">{esc(aid)}</div><h1 id="pp-title">{esc(a["title"])}</h1>'
              f'<p class="pp-meta">Unit {tp["unit"]} · {esc(C.unit(tp["unit"])["title"])} · {tid} {esc(tp["title"])}</p></header>\n'
              f'<main class="post-wrap"><div class="post-rendered" id="rendered">\n{md(body_md)}\n</div>\n'
              f'<pre class="post-source" id="source" hidden>{html.escape(src, quote=False)}</pre>\n'
              f'<p class="pp-other"><a href="{other}-lecture-post.html">Read the {label[other].lower()} post for {esc(aid)} →</a></p></main>\n'
              f'<footer class="pp-nav">{navlink(prev, "prev", "Previous lesson")}{navlink(nxt, "next", "Next lesson")}</footer>\n'
            + POST_SCRIPT)


def posts():
    feed = []
    blog = []
    rows = []
    for atom in C.atom_order():
        aid = atom["id"]
        a = parse_atom(atom["src"])
        t = dict(sections(rd(atom["src"] / "tutor.md"))[1])
        rows.append((aid, a, t))
    for i, (aid, a, t) in enumerate(rows):
        d = teacher_atom(aid)
        prev = (rows[i - 1][0], rows[i - 1][1]["title"]) if i else None
        nxt = (rows[i + 1][0], rows[i + 1][1]["title"]) if i + 1 < len(rows) else None
        for kind, label, _ in KINDS:
            src = post_markdown(aid, a, t, kind)
            path = d / f"{kind}-lecture-post.html"
            emit(path, post_page(d, aid, a, kind, src, prev, nxt))
            feed.append((f"{label}: {aid}, {a['title']}", path.relative_to(TEACHER).as_posix()))
            blog.append({"id": aid, "kind": kind, "title": a["title"], "topic": C.tid_of(aid),
                         "href": path.relative_to(TEACHER).as_posix(),
                         "banner": (d / "banner.png").relative_to(TEACHER).as_posix(),
                         "html": md(src.split("\n", 1)[1])})
    base = SITE_URL + "teacher/"
    items = "".join(f"    <item><title>{esc(t)}</title><link>{base}{p}</link><guid>{base}{p}</guid></item>\n" for t, p in feed)
    emit(TEACHER / "feed.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>\n'
         f"  <title>{BRAND} Cybersecurity, Tutor Posts</title>\n  <link>{SITE_URL}</link>\n"
         "  <description>Pre/post-lecture classroom posts, in course order.</description>\n"
         f"{items}</channel></rss>\n")
    emit(TEACHER / "posts.js", "window.AAYAT_POSTS = " + json.dumps(blog, ensure_ascii=False, separators=(",", ":")) + ";\n")


NB_RUNNER = '''

# ---- run every test above ------------------------------------------------
_results = []
for _name, _fn in list(globals().items()):
    if _name.startswith("test_") and callable(_fn):
        try:
            _fn()
            _results.append((_name, None))
        except Exception as _e:
            _results.append((_name, _e))
for _name, _e in _results:
    print(("PASS  " if _e is None else "FAIL  ") + _name + ("" if _e is None else f": {_e!r}"))
print(f"{sum(e is None for _, e in _results)}/{len(_results)} tests passed")
'''

NB_STYLE = """<style>
.nb-cell { margin-bottom: 14px; }
.nb-md { font-family: var(--font-serif); font-size: 15.5px; }
.nb-code { font-family: var(--font-mono); font-size: 13px; background: #1e1e1e; color: #d4d4d4; padding: 14px 16px; white-space: pre-wrap; overflow-x: auto; }
body { padding: 20px 26px; }
</style>
"""

ASSIGN_STYLE = """<style>
.assign-wrap { max-width: 900px; margin: 0 auto; padding: 30px; }
.assign-actions { display: flex; gap: 12px; margin: 18px 0 24px; flex-wrap: wrap; }
.assign-btn { font-family: var(--font-sans); font-size: 13px; text-transform: uppercase; letter-spacing: .5px; padding: 10px 18px; text-decoration: none; font-weight: 600; }
.assign-btn.primary { background: var(--accent-color); color: #fff; }
.assign-btn.primary:hover { background: var(--accent-dark); }
.assign-btn.secondary { background: #fff; color: var(--accent-color); border: 1px solid var(--accent-color); }
.assign-frame { width: 100%; height: 640px; border: 1px solid var(--border-color); background: #fff; }
</style>
"""


def prompt_sections(text):
    head, out, cur = [], {}, None
    for line in text.splitlines():
        m = re.match(r"## (.+)$", line)
        if m:
            cur = m.group(1).strip().lower()
            out[cur] = []
        elif cur is None:
            head.append(line)
        else:
            out[cur].append(line)
    return "\n".join(head).strip(), {k: "\n".join(v).strip() for k, v in out.items()}


def pyexpr(text):
    t = text.strip().rstrip(",").strip()
    for cand in (t, re.sub(r"\btrue\b", "True", re.sub(r"\bfalse\b", "False", re.sub(r"\bnull\b", "None", t)))):
        try:
            ast.parse(cand, mode="eval")
            return cand
        except SyntaxError:
            continue
    return None


def examples(block, funcs, nargs):
    body = re.sub(r"(?m)^```\w*\s*$", "", block.strip())
    lines = [l for l in body.splitlines() if l.strip()]
    if lines and all("->" in l for l in lines):
        chunks = lines
    else:
        chunks = re.split(r"\n\s*\n", body)
    out = []
    for ch in chunks:
        ch = "\n".join(re.sub(r"\s+#.*$", "", l) for l in ch.splitlines()).strip()
        i = ch.rfind("->")
        if i < 0:
            continue
        inp, exp = pyexpr(ch[:i]), pyexpr(ch[i + 2:])
        if inp is None or exp is None:
            continue
        node = ast.parse(inp, mode="eval").body
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            call = inp if node.func.id in funcs else "solve" + inp[len(node.func.id):]
        else:
            try:
                val = ast.literal_eval(inp)
            except ValueError:
                continue
            if nargs > 1:
                if not (isinstance(val, tuple) and len(val) == nargs):
                    continue
                call = "solve(*" + inp + ")"
            else:
                call = "solve(" + inp + ")"
        out.append((call, exp))
    return out


def test_examples(tests, limit=4):
    out = []
    try:
        tree = ast.parse(tests)
    except SyntaxError:
        return out
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Assert) and isinstance(node.test, ast.Compare) and len(node.test.ops) == 1
                and isinstance(node.test.ops[0], ast.Eq) and isinstance(node.test.left, ast.Call)):
            continue
        f = node.test.left.func
        if not (isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) and f.value.id == "impl"):
            continue
        call = ast.unparse(node.test.left).replace("impl.", "", 1)
        if len(call) > 400:
            continue
        out.append((call, ast.unparse(node.test.comparators[0])))
        if len(out) >= limit:
            break
    return out


def verified(cases, solution_code):
    env = {"__name__": "aayat_reference"}
    try:
        exec(compile(solution_code, "reference", "exec"), env)
    except Exception:
        return []
    keep = []
    for call, exp in cases:
        try:
            ast.parse("(" + call + ",\n" + exp + ")", mode="eval")
            if eval(call, dict(env)) == eval(exp, dict(env)):
                keep.append((call, exp))
        except Exception:
            continue
    return keep


def functions(code):
    try:
        return {n.name: len(n.args.args) for n in ast.walk(ast.parse(code)) if isinstance(n, ast.FunctionDef)}
    except SyntaxError:
        return {}


def checklist(text):
    items = [re.sub(r"^\s*-\s*", "", l).strip() for l in text.splitlines() if re.match(r"\s*-\s+\S", l)]
    return "\n".join("- [ ] " + i for i in items)


def notebook_cells(a, solution):
    p = a["src"] / "problem"
    info = parse_atom(a["src"])
    head, sec = prompt_sections(web_prompt(rd(p / "prompt.md")))
    skill = next((l for l in head.splitlines() if l.startswith("**Skill:**")), "")
    code_src = web_code(rd(p / "solution.py")) if solution else web_code(rd(p / "starter.py"))
    reference = re.sub(r"(?m)^#( |#)", r"###\1", web_text(rd(p / "interface.md"))).split("\n", 1)[-1].strip()
    title = f"# Runbook {a['id']}: {a['title']}" + ("  (MODEL SOLUTION, instructor copy, do not distribute)" if solution else "")
    steps = "1 Brief · 2 Plan · 3 Build · 4 Test · 5 Try it on the evidence · 6 Wrap up"
    brief = (f"{title}\n\n{skill}\n\n**Steps:** {steps}\n\n## 1. Brief\n\n**The situation.** {sec.get('problem', '')}\n\n"
             f"**Lesson objective.** {one_line(info['objective'])}\n\n"
             + (f"### What comes in\n{sec['input']}\n\n" if sec.get("input") else "")
             + (f"### What must come out\n{sec['output']}\n\n" if sec.get("output") else "")
             + "- [ ] Read the situation and say in one sentence what the tool must decide\n"
               "- [ ] Find the input and the output above")
    plan = "## 2. Plan\n\nWork it out on paper before you write code.\n\n"
    if sec.get("examples"):
        plan += "### Worked examples\n" + sec["examples"] + "\n\n- [ ] Work the first example by hand and get the same answer\n"
    rules = checklist(sec.get("constraints", ""))
    plan += ("\n### Rules to respect\n" + rules + "\n" if rules else "") + \
        "- [ ] Write the steps your function will take, in plain words\n- [ ] List two edge cases (an empty input, a tricky value)\n\n" + \
        "<details><summary>Reference: the exact contract</summary>\n\n" + reference + "\n\n</details>"
    build = "## 3. Build it\n\n" + ("This is the model solution." if solution else
                                    "Fill in `solve` below. Run the cell (Shift+Enter) after each change.") + \
        "\n\n- [ ] `solve` handles the worked examples\n- [ ] `solve` handles your edge cases"
    tests = web_tests(rd(p / "tests.py")).replace("import impl\n", "import __main__ as impl\n", 1)
    tests = re.sub(r"(?m)^(import __main__ as impl)\s+#.*$", r"\1", tests)
    tests = tests.rstrip("\n") + "\n" + NB_RUNNER
    test_md = "## 4. Test it\n\nThe tests are the acceptance check, like a change review before a fix goes live.\n\n" \
              "- [ ] Run the tests\n- [ ] Every test says PASS (if not, read the message, go back to step 3)"
    fns = functions(code_src)
    ref = web_code(rd(p / "solution.py"))
    ex = verified(examples(sec.get("examples", ""), fns, fns.get("solve", 1)), ref)
    if not ex:
        ex = verified(test_examples(web_tests(rd(p / "tests.py")), limit=12), ref)[:4]
    cells = [("markdown", brief), ("markdown", plan), ("markdown", build), ("code", code_src), ("markdown", test_md), ("code", tests)]
    if ex:
        run = "checks = [\n" + "".join(f"    (lambda: {c},\n     {e}),\n" for c, e in ex) + "]\n\n" + \
            "for n, (run, want) in enumerate(checks, 1):\n" + \
            "    try:\n        got = run()\n    except Exception as e:\n        got = \"error: \" + repr(e)\n" + \
            "    print(\"example\", n, \"OK  \" if got == want else \"DIFF\", \"got:\", got, \" expected:\", want)\n"
        cells += [("markdown", "## 5. Try it on the evidence\n\nRun your finished tool on the examples from the brief, then change one value and predict "
                               "the answer before you run it again.\n\n- [ ] Every example says OK\n- [ ] Your own changed example gives the answer you predicted"),
                  ("code", run)]
    else:
        cells += [("markdown", "## 5. Try it on the evidence\n\nCall `solve` on an input you make up, and predict the answer first.\n\n"
                               "- [ ] Your prediction matched")]
    cells.append(("markdown", "## 6. Wrap up\n\n- [ ] Explain in one sentence why your rule catches the problem\n"
                              "- [ ] Name one way an attacker could slip past it (a false negative)\n"
                              "- [ ] Name one harmless input it might wrongly flag (a false positive)\n"
                              "- [ ] Say where this check would run in a real organisation, and who would act on it"))
    return cells


def ipynb(aid, cells, salt):
    nb = {"cells": [], "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                    "language_info": {"name": "python"}},
          "nbformat": 4, "nbformat_minor": 5}
    for i, (kind, src) in enumerate(cells):
        cid = hashlib.sha1(f"{aid}-{salt}-{i}".encode()).hexdigest()[:8]
        c = {"cell_type": kind, "id": cid, "metadata": {}, "source": src.splitlines(keepends=True)}
        if kind == "code":
            c = {"cell_type": kind, "execution_count": None, "id": cid, "metadata": {}, "outputs": [],
                 "source": src.splitlines(keepends=True)}
        nb["cells"].append(c)
    return json.dumps(nb, ensure_ascii=False, indent=1) + "\n"


def preview(cells, title, css):
    body = "".join(
        f'<div class="nb-cell nb-md">{md(src)}</div>\n' if kind == "markdown"
        else f'<div class="nb-cell nb-code">{html.escape(src, quote=False)}</div>\n'
        for kind, src in cells)
    return PAGE_HEAD.format(title=title, css=css).replace("</head>", NB_STYLE + "</head>") + body + "</body>\n</html>\n"


def notebooks():
    for a in C.atom_order():
        if not N.has_problem(a):
            continue
        aid, d = a["id"], teacher_atom(a["id"])
        css = rel(d, TUTOR_CSS)
        cells = notebook_cells(a, solution=False)
        emit(d / f"{aid}-student.ipynb", ipynb(aid, cells, "student"))
        emit(d / "student-preview.html", preview(cells, f"{a['title']}, Student", css))
        emit(d / "assign.html",
             PAGE_HEAD.format(title=f"Assignment {aid} · {BRAND}", css=css).replace("</head>", ASSIGN_STYLE + "</head>")
             + f'<nav class="top-nav">\n  <div class="crumb"><a href="{rel(d, teacher_topic(C.tid_of(aid)) / "index.html")}">'
               f'{C.tid_of(aid)} teacher page</a> &gt; Assignment &gt; {aid}</div>\n</nav>\n'
               f'<div class="assign-wrap">\n  <h1 class="hub-title">{a["title"]}</h1>\n  <p class="hub-subtitle">Skill {aid} &middot; Coding Assignment</p>\n'
               '  <div class="assign-actions">\n'
               f'    <a class="assign-btn primary" href="{rel(d, N.problem_page(a))}">Open Live Playground &rarr;</a>\n'
               f'    <a class="assign-btn secondary" href="{aid}-student.ipynb" download>Download Notebook (.ipynb)</a>\n  </div>\n'
               '  <iframe class="assign-frame" src="student-preview.html"></iframe>\n</div>\n</body>\n</html>\n')
        scells = notebook_cells(a, solution=True)
        emit(d / f"{aid}-solution.ipynb", ipynb(aid, scells, "solution"))
        emit(d / "solution-preview.html", preview(scells, f"{a['title']}, Model Solution", css))


INK = (0x1B, 0x1B, 0x3A)


def docx_runs(par, text):
    for tok in re.split(r"(\*\*[^*]+\*\*|`[^`]+`|\*[^*\s][^*]*\*)", one_line(text)):
        if not tok:
            continue
        if tok.startswith("**"):
            par.add_run(tok[2:-2]).bold = True
        elif tok.startswith("`"):
            r = par.add_run(tok[1:-1])
            r.font.name = "Consolas"
        elif tok.startswith("*"):
            par.add_run(tok[1:-1]).italic = True
        else:
            par.add_run(tok)


def handout(aid, a, kind):
    import docx
    from docx.shared import RGBColor
    doc = docx.Document()
    for st in ("Title", "Heading 2"):
        doc.styles[st].font.color.rgb = RGBColor(*INK)
    doc.core_properties.title = f"{aid} {kind}-lecture handout"
    doc.add_paragraph(f"{aid}, {a['title']}", style="Title")

    def para(text):
        docx_runs(doc.add_paragraph(), text)

    def items(xs):
        for x in xs:
            docx_runs(doc.add_paragraph(style="List Bullet"), x)

    if kind == "pre":
        para(a["unit_line"])
        para(f"AP Learning Objective(s): {a['los']}   |   Skill: {a['skill']}")
        doc.add_heading("Before class", level=2)
        para(a["lead"])
        doc.add_heading("Terms you'll see today", level=2)
        items([re.match(r"\*\*(.+?)\*\*", x).group(1) if x.startswith("**") else re.split(r"[,:]", x)[0] for x in a["terms"]])
        doc.add_heading("Come ready to", level=2)
        para("Think about a time a message tried to rush, flatter, scare, or pressure you into acting quickly. "
             "Be ready to describe it in one sentence." if aid.startswith("1.1.") else
             "Skim the terms above and write down one question you want answered in class.")
    else:
        para(f"{a['unit_line']}  ·  Recap / take-home reference")
        doc.add_heading("Lesson recap", level=2)
        for p in a["lesson_paras"]:
            if p.startswith("### "):
                doc.add_heading(p[4:].split("\n")[0], level=3)
                p = p.split("\n", 1)[1] if "\n" in p else ""
            if re.match(r"^(- |\d+\. )", p):
                items([re.sub(r"^\d+\. ", "", x) for x in bullets(re.sub(r"(?m)^\d+\. ", "- ", p))])
            elif p.startswith("```"):
                r = doc.add_paragraph().add_run(p.strip("`").strip("\n"))
                r.font.name = "Consolas"
            elif p:
                para(p)
        doc.add_heading("Key terms", level=2)
        items(a["terms"])
        doc.add_heading("Common misconceptions", level=2)
        items(a["misconceptions"])
        doc.add_heading("Try it", level=2)
        items(a["try"])
        doc.add_heading("Self-check", level=2)
        para("Complete the quiz for this skill before the next class.")
    return doc


def docx_signature(blob):
    import docx
    d = docx.Document(io.BytesIO(blob))
    return [(p.style.name, p.text, tuple((r.bold, r.italic) for r in p.runs)) for p in d.paragraphs]


def handouts():
    for atom in C.atom_order():
        a = parse_atom(atom["src"])
        for kind in ("pre", "post"):
            buf = io.BytesIO()
            handout(atom["id"], a, kind).save(buf)
            emit_bytes(teacher_atom(atom["id"]) / f"{atom['id']}-{kind}-lecture-handout.docx", buf.getvalue(),
                       same=lambda old, new: docx_signature(old) == docx_signature(new))


def activity_keys():
    from .materials import activity
    for tid in C.order():
        keys = [(a, key) for a in C.topic_atoms(tid) if (a["src"] / "activity.md").exists() for key in [activity(a)[1]] if key]
        if not any((a["src"] / "activity.md").exists() for a in C.topic_atoms(tid)):
            continue
        d = teacher_topic(tid)
        k = len(keys)
        body = "".join(f'<div class="poster">\n  <div class="poster-meta">Skill {a["id"]}</div>\n  <h1>{a["title"]}</h1>\n'
                       + "".join(f"  <h2>{t}</h2>\n{md(b)}\n" for t, b in key) + "</div>\n" for a, key in keys)
        emit(d / "activity-keys.html",
             PAGE_HEAD.format(title=f"{tid} Activity Answer Keys · {BRAND}", css=rel(d, ASSETS / "activities" / "activity-theme.css"))
             + '<nav class="top-nav">\n  <div class="crumb"><a href="index.html">' + f'{tid} teacher page</a> &gt; '
               'Activity answer keys</div>\n  <button class="print-btn" onclick="window.print()">Print All</button>\n</nav>\n'
               f'<div class="hub-header">\n  <h1 class="hub-title">Topic {tid} Activity Answer Keys</h1>\n'
               f'  <p class="hub-subtitle">{C.topic(tid)["title"]} &middot; instructor-only &middot; {k} entr{"y" if k == 1 else "ies"}</p>\n</div>\n'
             + body + "</body>\n</html>\n")


def run():
    solutions()
    posts()
    notebooks()
    handouts()
    activity_keys()
