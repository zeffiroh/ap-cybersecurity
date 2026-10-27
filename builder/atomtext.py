"""Reading a skill's sources (atom.md, quiz.yaml, problem/, tutor.md) and adapting problem text for the web."""
import re
import sys

import markdown

from .util import rd


def escape_tags(s):
    """Markdown passes HTML through as markup, so an example like <script> in prose would run.
    Escape tags written outside code; code spans and fences are escaped by Markdown itself."""
    parts = re.split(r"(```.*?```|`[^`\n]*`)", s, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r"(?<!\\)<(?=[A-Za-z/!])", "&lt;", parts[i])
    return "".join(parts)


def md(s, extensions=("tables", "fenced_code")):
    return markdown.markdown(escape_tags(s), extensions=list(extensions))


def sections(text):
    """Markdown -> (text before the first '## ', [(heading, body), ...])."""
    head, *rest = re.split(r"(?m)^## ", text)
    out = []
    for r in rest:
        t, _, b = r.partition("\n")
        out.append((t.strip(), b.strip("\n")))
    return head, out


def bullets(body):
    """'- item' lines with their wrapped continuation lines joined into one line each."""
    items = []
    for line in body.splitlines():
        if line.startswith("- "):
            items.append(line[2:].strip())
        elif line.strip() and items:
            items[-1] += " " + line.strip()
    return items


def one_line(s):
    return " ".join(s.split())


def lead(lesson):
    """Teaser for the pre-lecture post: the lesson's first prose paragraph, up to 3 sentences / 420 chars."""
    paras = [re.sub(r"^(#+ .*\n?)+", "", p.strip()).strip() for p in lesson.split("\n\n")]
    para = next(p for p in paras if p and not p.startswith(("#", "-", "|", "```")))
    sents = re.split(r"(?<=[.!?])(\s+)", para)                     # sentence, separator, sentence, ...
    out = sents[0]
    for i in range(2, min(len(sents), 5), 2):
        if len(out) + len(sents[i - 1]) + len(sents[i]) > 420:
            break
        out += sents[i - 1] + sents[i]
    return out


def card_text(s, limit=220):
    if len(s) <= limit:
        return s
    return s[:limit - 3].rsplit(" ", 1)[0] + "..."


def parse_atom(d):
    head, secs = sections(rd(d / "atom.md"))
    S = dict(secs)
    title = re.search(r"(?m)^# [^,]+, (.*)", head).group(1).strip()
    unit_line = re.search(r"> \*\*(Unit .*?)\*\*", head).group(1)
    los = re.search(r"\*\*AP Learning Objective\(s\):\*\*\s*(.*)", head).group(1).strip()
    skill = re.search(r"\*\*Course skill\(s\):\*\*\s*(.*)", head).group(1).strip()
    lesson = S["Lesson"]
    return {"title": title, "unit_line": unit_line, "los": los, "skill": skill, "S": S,
            "objective": one_line(S["Learning objective (student-facing)"]),
            "lead": lead(lesson),
            "lesson_paras": [p.strip() for p in lesson.split("\n\n") if p.strip()],
            "terms": bullets(S.get("Key terms", "")),
            "misconceptions": bullets(S.get("Common misconceptions", "")),
            "try": bullets(S.get("Try it", ""))}


# ------------------------------------------- web adaptation of problem text --
# In the browser the student works in an editor, so every reference to the command-line
# files is rewritten to the matching part of the web page.
FILE_REFS = [
    (r"[^\n]*`?python -m pytest[^\n]*\n?",
     "Your code passes when every test below shows a checkmark (some are hidden until you run them).\n"),
    (r" \(AGENTS\.md rule \d+\)", ""),
    (r"\(see `?blackbox\.yaml`?\)", "(see the hidden grading tests)"),
    (r"`?interface\.md`?\s*/\s*`?blackbox\.yaml`?", "the Reference section below"),
    (r"[Ss]ee `?prompt\.md`? and `?interface\.md`?", "See the problem statement above and the Reference section below"),
    (r"per `?prompt\.md`? and `?interface\.md`?", "per the problem statement above and the Reference section below"),
    (r"\bin `?starter\.py`?", "in the code editor"),
    (r"`?interface\.md`?", "the Reference section below"),
    (r"`?blackbox\.yaml`?", "the hidden grading tests"),
    (r"[Ss]ee `?prompt\.md`?", "see the problem statement above"),
    (r"`?prompt\.md`?", "the problem statement above"),
    (r"`?tests\.py`?", "the tests"),
    (r"`?solution\.py`?", "the reference solution"),
    (r"`?starter\.py`?", "the starter code"),
]


def web_text(s):
    for a, b in FILE_REFS:
        s = re.sub(a, b, s)
    return s


def web_prompt(s):
    s = web_text(s)
    s = re.sub(r"\n## How to run\n```\n.*?```\n?", "\n", s, flags=re.S)   # CLI instructions don't apply on the web
    s = re.sub(r'(".*?")\s{2,}(->)', r"\1 \2", s)                         # un-align example arrows
    return s.rstrip("\n") + "\n"


def web_code(s):
    return web_text(s)


def web_tests(s):
    """Replace the IMPL-env-var loader with `import impl` (the browser registers the student's code as impl)."""
    body = re.sub(r'(?s)^\s*""".*?"""\n', "", s, count=1)             # module docstring talks about IMPL / CLI
    body = re.sub(r"(?m)^def _load\(path\):\n(?:[ \t]+.*\n)+", "", body)   # the file loader
    body = re.sub(r"(?m)^(?:_HERE|_TARGET) = .*\n", "", body)
    body = re.sub(r"(?m)^impl = _load\(_TARGET\)\n", "", body)
    body = re.sub(r"(?m)^import importlib\.util, os, pathlib\n", "", body)
    body = re.sub(r"(?m)^import importlib\.util\n", "", body)
    for mod in ("os", "pathlib"):                                          # drop only if now unused
        if not re.search(rf"\b{mod}\.", re.sub(rf"(?m)^import {mod}\n", "", body)):
            body = re.sub(rf"(?m)^import {mod}\n", "", body)
    body = re.sub(r"\n{3,}", "\n\n\n", body)
    return "import impl\n\n" + body.lstrip("\n")


def verify_problems(atoms):
    """Run every web test file the way the browser does: the solution must pass, the starter must fail."""
    import types
    bad = []
    for a in atoms:
        p = a["src"] / "problem"
        if not (p / "tests.py").exists():
            continue
        tests_src = web_tests(rd(p / "tests.py"))
        for which, code, want_pass in (("solution", web_code(rd(p / "solution.py")), True),
                                       ("starter", web_code(rd(p / "starter.py")), False)):
            impl = types.ModuleType("impl")
            sys.modules["impl"] = impl
            try:
                exec(compile(code, f"{a['id']}-{which}", "exec"), impl.__dict__)
                ns = {}
                exec(compile(tests_src, f"{a['id']}-tests", "exec"), ns)
                results = []
                for name, fn in ns.items():
                    if name.startswith("test_") and callable(fn):
                        try:
                            fn()
                            results.append(True)
                        except Exception:
                            results.append(False)
                ok = bool(results) and all(results)
            except Exception as e:
                ok, results = False, [f"load error: {e}"]
            if ok != want_pass:
                bad.append(f"{a['id']} {which}: {'expected pass' if want_pass else 'expected a failure'} "
                           f"({sum(r is True for r in results)}/{len(results)} passed)")
    sys.modules.pop("impl", None)
    return bad
