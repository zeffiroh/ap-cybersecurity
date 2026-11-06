import json
import re
from functools import lru_cache

from . import course as C
from .paths import BOOK, LECTURES, LECTURES_SRC, SITE, SRC

MAP_FILE = SRC / "topic-map.json"
CASES_SRC = SRC / "static" / "assets" / "linux" / "cases"
TEACHER_CASES = SRC / "teacher-cases"
LABS = {"cyberchef": ("CyberChef", SITE / "cyberchef" / "index.html"), "linux": ("Linux lab", SITE / "linux.html"),
        "sqli": ("SQL injection lab", SITE / "sqli.html"), "shop": ("Hack the shop", SITE / "shop.html")}


@lru_cache(None)
def data():
    return json.loads(MAP_FILE.read_text(encoding="utf-8"))


@lru_cache(None)
def decks():
    out = {}
    for md in sorted(LECTURES_SRC.glob("[0-9][0-9]_*.md")):
        m = re.search(r"(?m)^\s*title:\s*[\"']?(.*?)[\"']?\s*$", md.read_text(encoding="utf-8"))
        out[int(md.name[:2])] = {"n": int(md.name[:2]), "stem": md.stem, "title": m.group(1) if m else md.stem,
                                 "path": LECTURES / (md.stem + ".html")}
    return out


@lru_cache(None)
def all_cases():
    out = {}
    for meta in sorted(CASES_SRC.glob("*/meta.json")):
        info = json.loads(meta.read_text(encoding="utf-8"))
        out[meta.parent.name] = {"id": meta.parent.name, "title": info["title"], "level": info.get("level", ""), "minutes": info.get("minutes")}
    for path in sorted(TEACHER_CASES.glob("*.json")):
        info = json.loads(path.read_text(encoding="utf-8"))
        if info.get("published", True):
            slug = "tc-" + path.stem.removeprefix("case-")
            m = info["meta"]
            out[slug] = {"id": slug, "title": m["title"], "level": m.get("level", ""), "minutes": m.get("minutes")}
    return out


def entry(tid):
    return data()["topics"].get(tid, {"lectures": [], "labs": [], "cases": []})


def lectures(tid):
    return [decks()[n] for n in entry(tid)["lectures"] if n in decks()]


def cases(tid):
    return [all_cases()[c] for c in entry(tid)["cases"] if c in all_cases()]


def labs(tid):
    return [(k, *LABS[k]) for k in entry(tid)["labs"] if k in LABS]


def topics_for_lecture(n):
    return [t for t in C.order() if n in entry(t)["lectures"]]


def topics_for_case(cid):
    return [t for t in C.order() if cid in entry(t)["cases"]]


def topics_for_lab(key):
    return [t for t in C.order() if key in entry(t)["labs"]]


def book_anchor(tid):
    return BOOK / "index.html", "#ch-" + tid.replace(".", "-")


def case_href(cid):
    return f"?ref=rb-{cid}&runbook={cid}"


def code_book_href(aid):
    return f"?ref={aid}&book=1"


def _text(p):
    return p.read_text(encoding="utf-8", errors="replace")


def title_sources(tid):
    src = C.topic(tid)["src"]
    found = {}
    notes = src / "notes.html"
    if notes.exists():
        t = _text(notes)
        m = re.search(r'topicTitle:\s*"([^"]*)"', t)
        if m:
            found["notes"] = m.group(1)
        m = re.search(r'class="textbook-subtitle">([^<]*)<', t)
        if m:
            found["notes heading"] = m.group(1).strip().replace("&amp;", "&")
    quiz = src / "quizbank.xml"
    if quiz.exists():
        m = re.search(r'topic_title="([^"]*)"', _text(quiz))
        if m:
            found["quiz"] = m.group(1).replace("&amp;", "&")
    cards = src / "flashcards.json"
    if cards.exists():
        found["flashcards"] = json.loads(_text(cards)).get("topic_title")
    slides = src / "slides.json"
    if slides.exists():
        found["slides"] = json.loads(_text(slides)).get("subunit_title")
    return found


def check():
    problems = []
    m = data()
    for tid in C.order():
        if tid not in m["topics"]:
            problems.append(f"topic {tid} is not in topic-map.json")
        elif not entry(tid)["lectures"]:
            problems.append(f"topic {tid} has no lecture")
        want = C.topic(tid)["title"]
        for where, got in title_sources(tid).items():
            if got != want:
                problems.append(f"topic {tid} {where} title is \"{got}\", course.json says \"{want}\"")
    for tid, e in m["topics"].items():
        if tid not in C.order():
            problems.append(f"topic-map.json has unknown topic {tid}")
        for n in e["lectures"]:
            if n not in decks():
                problems.append(f"topic {tid} names missing lecture {n}")
        for k in e["labs"]:
            if k not in LABS:
                problems.append(f"topic {tid} names unknown lab {k}")
        for c in e["cases"]:
            if c not in all_cases():
                problems.append(f"topic {tid} names unknown runbook {c}")
    used = {n for e in m["topics"].values() for n in e["lectures"]} | set(m["course_wide_lectures"])
    for n in sorted(set(decks()) - used):
        problems.append(f"lecture {n:02d} is not linked to a topic or marked course-wide")
    usedc = {c for e in m["topics"].values() for c in e["cases"]}
    for c in sorted(set(all_cases()) - usedc):
        problems.append(f"runbook {c} is not linked to a topic")
    for a in C.atom_order():
        if not (a["src"] / "problem" / "prompt.md").exists():
            problems.append(f"skill {a['id']} has no coding problem")
    atom_los = {lo for a in C.atom_order() for lo in a["lo"]}
    unlinked = []
    for tid in C.order():
        for lo in C.topic(tid)["los"]:
            code = re.match(r"LO ([\d.A-Z]+)", lo).group(1)
            if code not in atom_los:
                unlinked.append(code)
    return problems, unlinked


