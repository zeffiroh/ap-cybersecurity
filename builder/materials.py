"""Student materials of each topic and skill.

source/units/.../<topic>/quizbank.xml      -> assets/quizzes/data/<tid>.json, unit-N/<tid>/quiz.html
source/tests/quizbanks/unit_quizbank_U1.xml -> assets/quizzes/data/U1.json (Unit 1 classwork quiz)
source/units/unit-N/classwork-quiz.json    -> unit-N/quiz.html (data copied by the static step)
source/units/.../<topic>/flashcards.json   -> unit-N/<tid>/flashcards.html
<skill>/quiz.yaml + problem/               -> assets/assignments/data/<tid>.json, problems/<aid>.json,
                                              unit-N/<tid>/assignments.html, unit-N/<tid>/<aid>/code.html
<skill>/activity.md                        -> assets/activities/data/<aid>.json, unit-N/<tid>/activities.html
<skill>/atom.md                            -> assets/simlabs/data/<tid>.json, unit-N/<tid>/simlab.html,
                                              unit-N/<tid>/<aid>/index.html (lesson)
<skill>/quiz.yaml                          -> unit-N/<tid>/<aid>/quiz.html (skill quiz)
"""
import json
import re
from string import Template

import markdown
import yaml
from lxml import etree

from . import course as C
from . import nav as N
from .atomtext import card_text, md, parse_atom, sections, web_code, web_prompt, web_tests, web_text
from .course import BRAND
from .paths import ASSETS, TEMPLATES, TESTS_SRC, UNITS_SRC, atom_dir
from .util import dump_json, emit, esc, rd, rel

PAGES = TEMPLATES / "pages"


def page(name, path, **kw):
    """Fill a page template; ${assets} is the path to site/assets from the page."""
    text = Template(rd(PAGES / name)).substitute(assets=rel(path.parent, ASSETS), **kw)
    emit(path, N.apply(path, text))


def js(s):
    return json.dumps(str(s))[1:-1]


# ------------------------------------------------------------ quiz banks --
def txt(el, tag=None):
    if tag is not None:
        el = el.find(tag)
    return "" if el is None else (el.text or "").strip()


def choices(q):
    return [{"key": c.get("key"), "text": txt(c)} for c in q.find("choices")]


def rationale(q):
    dr = q.find("distractor_rationale")
    return {} if dr is None else {c.get("key"): txt(c) for c in dr}


def number(s):
    try:
        f = float(s)
    except ValueError:
        return s
    return int(f) if f.is_integer() and "." not in s else f


TOPIC_META = ["unit", "topic_id", "topic_title", "skill_code", "skill_name", "lo_ref", "difficulty",
              "source_register", "scenario_ref"]


def topic_quiz(path):
    root = etree.parse(str(path)).getroot()
    qs = []
    for q in root.iter("question"):
        meta = q.find("meta")
        item = {"id": q.get("id")}
        for k in TOPIC_META:
            if meta.find(k) is not None:
                item[k] = txt(meta, k)
        item.update({"stem": txt(q, "stem"), "choices": choices(q), "answer_key": q.find("answer").get("key"),
                     "explanation": txt(q, "explanation"), "distractor_rationale": rationale(q)})
        qs.append(item)
    return {"topic_id": root.get("topic_id"), "topic_title": root.get("topic_title"), "unit": root.get("unit"),
            "questions": qs}


def generic(el):
    """XML -> JSON the way the quiz engine expects artifact data:
    leaf elements become their text, repeated tags become lists, element attributes go in "@attrs"."""
    kids = [c for c in el if isinstance(c.tag, str)]
    if not kids:
        return txt(el)
    out, lists = {}, set()
    for c in kids:
        v = generic(c)
        if c.tag in out:
            if c.tag not in lists:
                out[c.tag] = [out[c.tag]]
                lists.add(c.tag)
            out[c.tag].append(v)
        else:
            out[c.tag] = v
    if el.attrib:
        out["@attrs"] = dict(el.attrib)
    return out


def stimulus_question(q):
    meta, am = q.find("meta"), q.find("adaptive_meta")
    sv = {}
    for c in q.find("skill_vector"):
        if isinstance(c.tag, str):
            sv.setdefault(c.tag, []).append(dict(c.attrib))
    sv = {k: v[0] if len(v) == 1 else v for k, v in sv.items()}
    adaptive = {}
    for c in am:
        if isinstance(c.tag, str):
            adaptive[c.tag] = txt(c).split() if c.tag == "prerequisite_topics" else number(txt(c))
    return {"id": q.get("id"), "stimulus_ref": txt(meta, "stimulus_ref"),
            "topic_refs": txt(meta, "topic_refs").split(),
            "lo_refs": re.findall(r"LO\s+[\w.]+", txt(meta, "lo_refs")) or txt(meta, "lo_refs").split(),
            "skill_vector": sv, "adaptive_meta": adaptive,
            "stem": txt(q, "stem"), "choices": choices(q), "answer_key": q.find("answer").get("key"),
            "explanation": txt(q, "explanation"), "distractor_rationale": rationale(q)}


def stimulus_quiz(path):
    root = etree.parse(str(path)).getroot()
    sets = []
    for s in root.iter("stimulus_set"):
        st, art = s.find("stimulus"), s.find("stimulus").find("artifact")
        sets.append({"id": s.get("id"), "difficulty_range": s.get("difficulty_range"),
                     "stimulus": {"type": txt(st, "type"), "label": txt(st, "label"), "context": txt(st, "context"),
                                  "provenance": txt(st, "provenance") if st.find("provenance") is not None else None,
                                  "artifact": {"format": art.get("format"), "data": generic(art)}},
                     "questions": [stimulus_question(q) for q in s.iter("question")]})
    return {"unit_id": root.get("unit_id"), "unit_title": root.get("unit_title"), "stimulus_sets": sets}


MODE_TOOLBAR = """<nav class="top-nav">
  <div class="actions">
    <div class="mode-toggle">
      <button id="mode-practice" class="active" onclick="QuizEngine.setMode('practice')">Practice</button>
      <button id="mode-exam" onclick="QuizEngine.setMode('exam')">Exam</button>
    </div>
  </div>
</nav>
"""


def quizzes():
    for tid in C.order():
        x = C.topic(tid)["src"] / "quizbank.xml"
        if not x.exists():
            continue
        data = topic_quiz(x)
        out = ASSETS / "quizzes" / "data" / f"{tid}.json"
        emit(out, dump_json(data), json_equal=True)
        path = N.target(tid, "quiz")
        page("quiz.html", path, page_title=esc(N.title_for(N.context(path))), toolbar=MODE_TOOLBAR, mode="simple",
             data_url=rel(path.parent, out), title=f"Topic {tid} Quiz",
             subtitle=js(f"{data['topic_title']}, {len(data['questions'])} Questions"))
    emit(ASSETS / "quizzes" / "data" / "U1.json", dump_json(stimulus_quiz(TESTS_SRC / "quizbanks" / "unit_quizbank_U1.xml")),
         json_equal=True)
    for u in C.units():
        n = u["num"]
        src = (TESTS_SRC / "quizbanks" / "unit_quizbank_U1.xml") if n == 1 else (UNITS_SRC / f"unit-{n}" / "classwork-quiz.json")
        data = stimulus_quiz(src) if n == 1 else json.loads(rd(src))
        sets = data["stimulus_sets"]
        path = N.unit_quiz(n)
        page("quiz.html", path, page_title=esc(N.title_for(N.context(path))), toolbar=MODE_TOOLBAR, mode="stimulus",
             data_url=rel(path.parent, ASSETS / "quizzes" / "data" / f"U{n}.json"),
             title=js(f"Unit {n}: {data['unit_title']}, Classwork Quiz"),
             subtitle=js(f"Stimulus-based adaptive quiz, {sum(len(s['questions']) for s in sets)} questions "
                         f"across {len(sets)} exhibits"))


# ------------------------------------------------------------ flashcards --
def flashcards():
    from .paths import downloads_unit
    for tid in C.order():
        src = C.topic(tid)["src"] / "flashcards.json"
        if not src.exists():
            continue
        data = json.loads(rd(src))
        path = N.target(tid, "flashcards")
        page("flashcards.html", path, page_title=esc(N.title_for(N.context(path))),
             data_url=rel(path.parent, ASSETS / "flashcards" / "data" / f"{tid}.json"),
             apkg_url=rel(path.parent, downloads_unit(tid) / f"Topic_{tid}_Flashcards.apkg"),
             title=f"Topic {tid} Flashcards", subtitle=js(f"{data['topic_title']}, {len(data['flashcards'])} Cards"))


# ------------------------------------------------- assignments and code --
def problems():
    for a in C.atom_order():
        p = a["src"] / "problem"
        if not (p / "prompt.md").exists():
            continue
        starter_src, tests_src = rd(p / "starter.py"), rd(p / "tests.py")
        pkgs = ["sqlite3"] if "import sqlite3" in (starter_src + tests_src) else []
        obj = {"atom_id": a["id"], "topic_id": C.tid_of(a["id"]), "title": a["title"],
               "prompt_md": web_prompt(rd(p / "prompt.md")), "starter_py": web_code(starter_src),
               "tests_py": web_tests(tests_src), "interface_md": web_text(rd(p / "interface.md")),
               "points": a["points"], "packages": pkgs}
        out = ASSETS / "assignments" / "problems" / f"{a['id']}.json"
        emit(out, dump_json(obj), json_equal=True)
        path = N.problem_page(a)
        page("code.html", path, page_title=esc(N.title_for(N.context(path))), title=esc(a["title"]), aid=a["id"],
             points=a["points"], data_url=rel(path.parent, out))


def assignment_data(tid):
    """quiz.yaml items (all but type: code, which are the coding problems) + the topic's coding problems."""
    items, coding = [], []
    for a in C.topic_atoms(tid):
        q = yaml.safe_load(rd(a["src"] / "quiz.yaml"))
        for it in q.get("items", []):
            if it.get("type") == "code":
                continue
            item = {"id": f"{a['id']}.{it['id']}", "atom_id": a["id"], "atom_title": a["title"]}
            item.update({k: v for k, v in it.items() if k != "id"})
            item.setdefault("accept", None)
            items.append(item)
        if N.has_problem(a):
            coding.append({"atom_id": a["id"], "title": a["title"], "points": a["points"]})
    keys = ["id", "atom_id", "atom_title", "type", "prompt", "options", "answer", "accept", "points", "explain"]
    return {"topic_id": tid, "topic_title": C.topic(tid)["title"], "unit": str(C.unit_of(tid)),
            "practice_items": [{k: it[k] for k in keys if k in it} | {k: v for k, v in it.items() if k not in keys}
                               for it in items],
            "coding_problems": coding}


def assignments():
    for tid in C.order():
        data = assignment_data(tid)
        items, coding = data["practice_items"], data["coding_problems"]
        out = ASSETS / "assignments" / "data" / f"{tid}.json"
        emit(out, dump_json(data), json_equal=True)
        path = N.target(tid, "assignments")
        cards = "".join(
            f'  <a class="problem-card" href="{rel(path.parent, N.problem_page(C.atom(c["atom_id"])))}">\n'
            f'    <div class="problem-id">Skill {c["atom_id"]}</div>\n'
            f'    <h3 class="problem-title">{esc(c["title"])}</h3>\n'
            f'    <p class="problem-points">{c["points"]} points &middot; auto-graded</p>\n  </a>\n' for c in coding)
        page("assignments.html", path, page_title=esc(N.title_for(N.context(path))), tid=tid,
             topic_title=esc(C.topic(tid)["title"]), n_items=len(items), n_coding=len(coding), cards=cards,
             data_url=rel(path.parent, out))


# ------------------------------------------------------------ activities --
ACT_STD = {"Goal", "Materials (all local)", "Steps", "Collaborate (AP skill 4)", "Exit ticket",
           "Instructor notes", "Answer key (instructor only)"}
ACT_KEY = ["Instructor notes", "Answer key (instructor only)"]


def checklist(h):
    def one(m):
        items = re.findall(r"<li>(.*?)</li>", m.group(1), re.S)
        return ('<ul class="material-checklist">' + "".join(
            '<li><label><input type="checkbox" class="material-check">' + x + "</label></li>" for x in items) + "</ul>")
    return re.sub(r"<ul>\n(.*?)\n</ul>\n?", one, h, flags=re.S)


def activity(a):
    head, secs = sections(rd(a["src"] / "activity.md"))
    S = dict(secs)
    m = re.search(r"\*\*Format:\*\*\s*(.*?)\s*·\s*\*\*Time:\*\*\s*(.*?)\s*·\s*\*\*Offline:\*\*\s*(.*)", head)
    return {
        "atom_id": a["id"], "topic_id": C.tid_of(a["id"]), "title": a["title"],
        "meta": {"format": m.group(1), "time": m.group(2), "offline": m.group(3).strip()},
        "goal_html": md(S["Goal"]),
        "materials_html": checklist(md(S.get("Materials (all local)", ""))),
        "reference_html": "\n".join(f"<h2>{t}</h2>\n" + md(b) for t, b in secs if t not in ACT_STD),
        "steps_html": md(S["Steps"]).replace("<ol>", '<ol class="flowchart">').replace("<h3>", '<h3 class="flow-phase-title">'),
        "collaborate_html": md(S.get("Collaborate (AP skill 4)", "")),
        "exit_html": md(S["Exit ticket"]),
    }, [(t, b) for t, b in secs if t in ACT_KEY]


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

POSTER = """<div class="poster" data-topic-id="{topic_id}" data-atom-id="{atom_id}">
  <div class="poster-meta">Skill {atom_id} &middot; {fmt} &middot; {time} &middot; Offline: {offline}</div>
  <h1>{title}</h1>

  <section class="sec sec-goal">
    <h2>Goal</h2>
    {goal_html}
  </section>

  <section class="sec sec-materials">
    <h2>Materials</h2>
    {materials_html}
    {reference_html}
  </section>

  <section class="sec sec-steps locked">
    <h2>Steps</h2>
    <div class="steps-lock-notice">Check off all materials above to unlock the steps.</div>
    {steps_html}
  </section>

  <section class="sec sec-collaborate">
    <h2>Collaborate</h2>
    {collaborate_html}
    <div class="collab-widget">
      <label>Your name <input type="text" class="collab-name"></label>
      <label>Partner's name <input type="text" class="collab-partner"></label>
      <label>What did you and your partner discover?</label>
      <textarea class="collab-notes" placeholder="A sentence or two is plenty."></textarea>
      <button class="collab-submit">Log</button>
      <span class="collab-status"></span>
    </div>
  </section>

  <section class="sec sec-exit">
    <h2>Exit Ticket</h2>
    <div class="certificate">
      <div class="certificate-seal">AP</div>
      <h3>Certificate of Completion</h3>
      <div class="certificate-instructions">{exit_html}</div>
      <div class="exit-form">
        <label>Name <input type="text" class="exit-name"></label>
        <label>Your response</label>
        <textarea class="exit-response" placeholder="Write your response here..."></textarea>
        <button class="exit-submit">Submit Exit Ticket</button>
        <span class="exit-status"></span>
      </div>
      <div class="exit-result"></div>
    </div>
  </section>
</div>
"""


def activities():
    for tid in C.order():
        items = [a for a in C.topic_atoms(tid) if (a["src"] / "activity.md").exists()]
        if not items:
            continue
        path = N.target(tid, "activities")
        r = lambda p: rel(path.parent, p)
        posters = []
        for a in items:
            data, _ = activity(a)
            emit(ASSETS / "activities" / "data" / f"{a['id']}.json", dump_json(data), json_equal=True)
            posters.append(POSTER.format(fmt=data["meta"]["format"], time=data["meta"]["time"],
                                         offline=data["meta"]["offline"], **data))
        text = (PAGE_HEAD.format(title=f"{tid} Activities", css=r(ASSETS / "activities" / "activity-theme.css"))
                + '<nav class="top-nav">\n  <button class="print-btn" onclick="window.print()">Print</button>\n</nav>\n'
                  f'<div class="hub-header">\n  <h1 class="hub-title">{tid} Activities</h1>\n'
                  f'  <p class="hub-subtitle">{C.topic(tid)["title"]} &middot; {len(items)}</p>\n</div>\n'
                + "".join(posters)
                + f'<script src="{r(ASSETS / "config.js")}"></script>\n<script src="{r(ASSETS / "shared" / "neon.js")}"></script>\n'
                  f'<script src="{r(ASSETS / "shared" / "identity.js")}"></script>\n'
                  f'<script src="{r(ASSETS / "shared" / "backend-client.js")}"></script>\n'
                  f'<script src="{r(ASSETS / "activities" / "activity-app.js")}"></script>\n'
                  "</body>\n</html>\n")
        emit(path, N.apply(path, text))


# --------------------------------------------------------------- simlabs --
def simlabs():
    for tid in C.order():
        items = [a for a in C.topic_atoms(tid) if N.has_sim(a)]
        if not items:
            continue
        recs = [{"atom_id": a["id"], "title": a["title"], "objective": card_text(parse_atom(a["src"])["objective"])}
                for a in items]
        emit(ASSETS / "simlabs" / "data" / f"{tid}.json",
             dump_json({"topic_id": tid, "topic_title": C.topic(tid)["title"], "atoms": recs}), json_equal=True)
        path = N.target(tid, "simlab")
        cards = "".join(
            f'  <a class="atom-card" href="{rel(path.parent, N.sim_page(C.atom(r["atom_id"])))}" target="_blank" rel="noopener">\n'
            f'    <div class="atom-id">Skill {r["atom_id"]}</div>\n    <h3 class="atom-title">{r["title"]}</h3>\n'
            f'    <p class="atom-objective">{r["objective"]}</p>\n    <div class="atom-cta">Open &rarr;</div>\n  </a>\n'
            for r in recs)
        text = (PAGE_HEAD.format(title=f"{tid} SimLab", css=rel(path.parent, ASSETS / "simlabs" / "simlab-theme.css"))
                + f'<div class="hub-header">\n  <h1 class="hub-title">{tid} SimLab</h1>\n'
                  f'  <p class="hub-subtitle">{C.topic(tid)["title"]} &middot; {len(recs)}</p>\n</div>\n'
                  f'<div class="atom-grid">\n{cards}</div>\n'
                  "</body>\n</html>\n")
        emit(path, N.apply(path, text))


# ------------------------------------------------- skill lesson and quiz --
def strip_sources(text):
    """Drop '## Sources ...' sections (provenance notes, not for the page)."""
    return re.sub(r"(?ms)^#{1,6}\s+Sources.*?(?=^#{1,6}\s|\Z)", "", text.replace(chr(13), ""))


def lesson_html(src):
    """atom.md for the web: the page shows the title and metadata itself."""
    text = strip_sources(rd(src / "atom.md"))
    text = re.sub(r"\A#\s+.*\n+(>.*\n)*", "", text)
    text = re.sub(r"(?m)^##\s+Learning objective.*$", "## Objective", text)
    return md(text, extensions=("tables", "fenced_code", "sane_lists"))


def atom_head(a, here, sub):
    """Title, the topic's skills as a strip, and the skill's other pages."""
    r = lambda p: rel(here.parent, p)
    sibs = C.topic_atoms(C.tid_of(a["id"]))
    strip = "".join(f'<span class="on">{s["id"]}</span>' if s["id"] == a["id"] else
                    f'<a href="{r(atom_dir(s["id"]) / here.name)}" title="{esc(s["title"])}">{s["id"]}</a>' for s in sibs)
    pages = [("Lesson", N.lesson_page(a), "lesson"), ("Quiz", N.quiz_page(a), "quiz"),
             ("Sim", N.sim_page(a), "sim"), ("Code", N.problem_page(a), "code")]
    if N.has_lab(a):
        pages.append(("Lab", N.lab_page(a), "lab"))
    ls = "".join(f'<span class="on">{lbl}</span>' if key == sub else f'<a href="{r(p)}">{lbl}</a>' for lbl, p, key in pages)
    tags = "".join(f'<span class="aa-tag">{esc(x)}</span>' for x in ["LO " + " ".join(a["lo"])] + a["skills"])
    return (f'<h1><span class="aa-id">{a["id"]}</span>{esc(a["title"])}</h1>\n<p class="aa-sub">{tags}</p>\n'
            f'<div class="aa-strip">{strip}</div>\n<div class="aa-strip">{ls}</div>\n')


def practice():
    for a in C.atom_order():
        path = N.lesson_page(a)
        emit(path, N.shell(path, "", atom_head(a, path, "lesson") + lesson_html(a["src"])))
        path = N.quiz_page(a)
        r = lambda p: rel(path.parent, p)
        qf = a["src"] / "quiz.yaml"
        quiz = (yaml.safe_load(rd(qf)) if qf.exists() else None) or {}
        quiz_json = json.dumps({"atom": a["id"], "title": quiz.get("title", a["title"]), "items": quiz.get("items", [])})
        body = (atom_head(a, path, "quiz") + '<div id="bb-root"></div>\n'
                f'<script>\nwindow.QUIZ = {quiz_json};\n</script>\n'
                f'<script src="{r(ASSETS / "config.js")}"></script>\n'
                f'<script src="{r(ASSETS / "shared" / "neon.js")}"></script>\n'
                f'<script src="{r(ASSETS / "shared" / "identity.js")}"></script>\n'
                f'<script src="{r(ASSETS / "shared" / "backend-client.js")}"></script>\n'
                f'<script src="{r(ASSETS / "practice" / "bluebook.js")}"></script>')
        emit(path, N.shell(path, "", body))


def run():
    quizzes()
    flashcards()
    problems()
    assignments()
    activities()
    simlabs()
    practice()
