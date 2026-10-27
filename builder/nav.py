"""The top bar on every student page, and where each page of the course lives.

    [A] Aayat-AP-Prep / Cybersecurity v / Unit N v / X.Y Title v | Overview Notes Slides ... | <- X.Y   X.Y ->

    text = apply(path, text)              # add or refresh the bar on a page written to `path`
    text = shell(path, title, body)       # a whole new page in the site style, bar included

Pages under teacher/ never get the bar, and no student page links to them.
"""
import re
from functools import lru_cache
from pathlib import Path

from . import course as C
from .course import BRAND, SITE_URL, SUBJECT
from .paths import (BOOK, CAPSTONE, DOWNLOADS, LECTURES, LECTURES_SRC, SITE, TESTS, THEME, atom_dir,
                    topic_dir, unit_dir)
from .util import esc, rel

KINDS = [("topic", "Overview"), ("notes", "Notes"), ("slides", "Slides"), ("practice", "Practice"),
         ("simlab", "SimLab"), ("flashcards", "Flashcards"), ("quiz", "Quiz"),
         ("assignments", "Assignments"), ("activities", "Activities")]
KIND_LABEL = dict(KINDS)

GLOBAL = [  # (key, label, path)
    ("home", "Home", SITE / "index.html"),
    ("progress", "Progress", SITE / "progress.html"),
    ("book", "Book", BOOK / "index.html"),
    ("lectures", "Lectures", LECTURES / "index.html"),
    ("glossary", "Glossary", SITE / "glossary.html"),
    ("tests", "Unit tests", TESTS / "index.html"),
    ("hw", "CW/HW quizzes", TESTS / "hw" / "index.html"),
    ("capstone", "Capstone", CAPSTONE / "index.html"),
    ("calendar", "Calendar", SITE / "calendar.html"),
    ("report", "Report card", SITE / "report.html"),
    ("downloads", "Downloads", DOWNLOADS / "index.html"),
    ("support", "Support", SITE / "support.html"),
]


# ------------------------------------------------------------------ where pages live --
def target(tid, kind):
    """The page of one kind for a topic."""
    if kind == "topic":
        return topic_dir(tid) / "index.html"
    if kind == "practice":
        a = C.topic_atoms(tid)
        return atom_dir(a[0]["id"]) / "index.html" if a else None
    return topic_dir(tid) / f"{kind}.html"


def has(tid, kind):
    """Whether the topic has that material (decided from the sources, so build order does not matter)."""
    src = C.topic(tid)["src"]
    atoms = C.topic_atoms(tid)
    return {"topic": True,
            "notes": (src / "notes.html").exists(),
            "slides": (src / "slides.json").exists(),
            "practice": bool(atoms),
            "simlab": any((a["src"] / "sim.html").exists() for a in atoms),
            "flashcards": (src / "flashcards.json").exists(),
            "quiz": (src / "quizbank.xml").exists(),
            "assignments": bool(atoms),
            "activities": any((a["src"] / "activity.md").exists() for a in atoms)}[kind]


def unit_quiz(n):
    return unit_dir(n) / "quiz.html"


def unit_test(n):
    return TESTS / "index.html", f"?unit=U{n}"


def lesson_page(a):
    return atom_dir(a["id"]) / "index.html"


def quiz_page(a):
    return atom_dir(a["id"]) / "quiz.html"


def problem_page(a):
    return atom_dir(a["id"]) / "code.html"


def sim_page(a):
    return atom_dir(a["id"]) / "sim.html"


def lab_page(a):
    return atom_dir(a["id"]) / "lab.html"


def has_lab(a):
    return (a["src"] / "lab.html").exists()


def has_problem(a):
    return (a["src"] / "problem" / "prompt.md").exists()


def has_sim(a):
    return (a["src"] / "sim.html").exists()


@lru_cache(None)
def decks():
    """[(number, page path, title)] for the lecture decks, from their Markdown sources."""
    out = []
    for md in sorted(LECTURES_SRC.glob("[0-9][0-9]_*.md")):
        m = re.search(r"(?m)^\s*title:\s*[\"']?(.*?)[\"']?\s*$", md.read_text(encoding="utf-8"))   # the deck's own title comes first
        out.append((int(md.name[:2]), LECTURES / (md.stem + ".html"), m.group(1) if m else md.stem))
    return out


# ------------------------------------------------------------------ page context --
def context(path):
    """What a page is: {kind, tid, unit, atom, sub, label}, or None for pages that get no bar."""
    p = Path(path).resolve()
    try:
        rp = p.relative_to(SITE.resolve()).as_posix()
    except ValueError:
        return None
    if rp == "tests/hw/quiz.html":
        p = (TESTS / "hw" / "index.html").resolve()
    for key, label, gp in GLOBAL:
        if p == gp.resolve():
            return {"kind": "global", "key": key, "label": label}
    m = re.fullmatch(r"unit-(\d)/(index|quiz)\.html", rp)
    if m:
        return {"kind": "unit", "unit": int(m.group(1)), **({"sub": "quiz"} if m.group(2) == "quiz" else {})}
    m = re.fullmatch(r"unit-\d/(\d\.\d)/index\.html", rp)
    if m:
        return {"kind": "topic", "tid": m.group(1)}
    m = re.fullmatch(r"unit-\d/(\d\.\d)/(notes|slides|simlab|flashcards|quiz|assignments|activities)\.html", rp)
    if m:
        return {"kind": m.group(2), "tid": m.group(1)}
    m = re.fullmatch(r"unit-\d/(\d\.\d)/(\d\.\d\.[a-z])/(index|quiz|code)\.html", rp)
    if m:
        if m.group(3) == "code":
            return {"kind": "assignments", "tid": m.group(1), "atom": m.group(2), "sub": "problem"}
        return {"kind": "practice", "tid": m.group(1), "atom": m.group(2),
                "sub": "lesson" if m.group(3) == "index" else "quiz"}
    m = re.fullmatch(r"lectures/(\d\d)_[^/]+\.html", rp)
    if m:
        return {"kind": "deck", "n": int(m.group(1))}
    return None


# ------------------------------------------------------------------ bar --
def title_for(c):
    if c is None:
        return None
    k = c["kind"]
    if k == "global":
        return f"{c['label']} · {BRAND}" if c["key"] != "home" else f"{BRAND} · {SUBJECT}"
    if k == "unit":
        u = C.unit(c["unit"])
        return f"Unit {u['num']} {u['title']}{' · Unit quiz' if c.get('sub') == 'quiz' else ''} · {BRAND}"
    if k == "deck":
        return None
    t = C.topic(c["tid"])
    if k == "topic":
        return f"{c['tid']} {t['title']} · {BRAND}"
    if c.get("atom"):
        a = C.atom(c["atom"])
        what = {"lesson": "", "quiz": " · Quiz", "problem": " · Code"}[c["sub"]]
        return f"{a['id']} {a['title']}{what} · {BRAND}"
    return f"{c['tid']} {t['title']} · {KIND_LABEL[k]} · {BRAND}"


def _track(c):
    """data-k/r/t: what progress.js records when this page is opened."""
    k = c["kind"]
    if k == "global":
        kr = {"book": ("book", "book"), "capstone": ("capstone", "capstone"),
              "tests": ("test", "unit-test"), "hw": ("test", "cw-hw")}.get(c["key"])
        if not kr:
            return ""
        kind, ref, tid = kr[0], kr[1], ""
    elif k == "deck":
        kind, ref, tid = "lecture", f"{c['n']:02d}", ""
    elif k == "unit":
        kind, ref, tid = ("quiz" if c.get("sub") == "quiz" else "unit"), f"U{c['unit']}", ""
    else:
        kind, ref, tid = k, c.get("atom") or c["tid"], c["tid"]
    return f' data-k="{kind}" data-r="{ref}" data-t="{tid}"'


def _on(flag):
    return ' class="on"' if flag else ""


def nav_html(page_dir, c):
    page_dir = Path(page_dir)
    r = lambda p, q="": rel(page_dir, p, q)
    k = c["kind"]
    tid = c.get("tid")
    unum = c.get("unit") or (C.topic(tid)["unit"] if tid else None)
    parts = [f'<a class="apn-brand" href="{r(SITE / "index.html")}"><img class="apn-mark" src="{r(THEME / "icon.svg")}" alt="">'
             f'<span class="apn-name">{BRAND}</span></a>']

    gl = "".join(f'<a{_on(k == "global" and c["key"] == key)} href="{r(p)}">{esc(label)}</a>'
                 for key, label, p in GLOBAL)
    cur = ' class="apn-cur"' if k == "global" else ""
    glabel = c["label"] if k == "global" and c["key"] != "home" else SUBJECT
    if k == "deck":
        glabel = "Lectures"
    parts.append(f'<span class="apn-sep">/</span><details><summary{cur}>{esc(glabel)}</summary>'
                 f'<div class="apn-menu">{gl}</div></details>')

    if k == "deck":
        ds = decks()
        items = "".join(f'<a{_on(n == c["n"])} href="{r(p)}"><span class="apn-n">{n:02d}</span>{esc(t)}</a>'
                        for n, p, t in ds)
        parts.append(f'<span class="apn-sep">/</span><details><summary class="apn-cur">Class {c["n"]:02d}</summary>'
                     f'<div class="apn-menu">{items}</div></details>')
        i = [n for n, _, _ in ds].index(c["n"])
        step = []
        if i > 0:
            n, p, t = ds[i - 1]
            step.append(f'<a href="{r(p)}" title="{esc(t)}">&larr; {n:02d}</a>')
        if i < len(ds) - 1:
            n, p, t = ds[i + 1]
            step.append(f'<a class="apn-next" href="{r(p)}" title="{esc(t)}">{n:02d} &rarr;</a>')
        parts.append(f'<div class="apn-step">{"".join(step)}</div>')
        return f'<nav class="apnav" aria-label="Course"{_track(c)}>{"".join(parts)}</nav>'

    us = C.units()
    items = "".join(f'<a{_on(u["num"] == unum)} href="{r(unit_dir(u["num"]) / "index.html")}">'
                    f'<span class="apn-n">U{u["num"]}</span>{esc(u["title"])}</a>' for u in us)
    label = f'Unit {unum}<span class="apn-long"> {esc(C.unit(unum)["title"])}</span>' if unum else "Units"
    cur = ' class="apn-cur"' if k == "unit" else ""
    parts.append(f'<span class="apn-sep">/</span><details><summary{cur}>{label}</summary>'
                 f'<div class="apn-menu">{items}</div></details>')

    if unum:
        same = k if k in KIND_LABEL else "topic"

        def link(t):
            return r(target(t, same) if has(t, same) else target(t, "topic"))

        groups = "".join(
            f'<div class="apn-h"><a href="{r(unit_dir(u["num"]) / "index.html")}">Unit {u["num"]} &middot; {esc(u["title"])}</a></div>'
            + "".join(f'<a{_on(t == tid)} href="{link(t)}"><span class="apn-n">{t}</span>'
                      f'{esc(C.topic(t)["title"])}</a>' for t in u["topics"]) for u in us)
        label = f'{tid}<span class="apn-long"> {esc(C.topic(tid)["title"])}</span>' if tid else "Topics"
        cur = ' class="apn-cur"' if tid and k == "topic" else ""
        parts.append(f'<span class="apn-sep">/</span><details><summary{cur}>{label}</summary>'
                     f'<div class="apn-menu">{groups}</div></details>')

    if tid:
        tabs = []
        for kk, lbl in KINDS:
            if has(tid, kk):
                on = ' class="on" aria-current="page"' if kk == k else ""
                tabs.append(f'<a{on} href="{r(target(tid, kk))}">{lbl}</a>')
        parts.append(f'<span class="apn-div"></span><div class="apn-tabs">{"".join(tabs)}</div>')

    step = []
    if c.get("atom"):
        seq = C.atom_order()
        if c["sub"] == "problem":
            seq = [a for a in seq if has_problem(a)]
        i = [a["id"] for a in seq].index(c["atom"])

        def apage(a):
            return {"problem": problem_page, "quiz": quiz_page, "lesson": lesson_page}[c["sub"]](a)
        if i > 0:
            step.append(f'<a href="{r(apage(seq[i - 1]))}" title="{esc(seq[i - 1]["title"])}">&larr; {seq[i - 1]["id"]}</a>')
        if i < len(seq) - 1:
            step.append(f'<a class="apn-next" href="{r(apage(seq[i + 1]))}" title="{esc(seq[i + 1]["title"])}">'
                        f'{seq[i + 1]["id"]} &rarr;</a>')
    elif tid:
        seq = [t for t in C.order() if has(t, k)]
        i = seq.index(tid)
        if i > 0:
            p = seq[i - 1]
            step.append(f'<a href="{r(target(p, k))}" title="{esc(C.topic(p)["title"])}">&larr; {p}</a>')
        if i < len(seq) - 1:
            n = seq[i + 1]
            step.append(f'<a class="apn-next" href="{r(target(n, k))}" title="{esc(C.topic(n)["title"])}">'
                        f'{n}<span class="apn-long"> {esc(C.topic(n)["title"])}</span> &rarr;</a>')
    elif k == "unit":
        i = [u["num"] for u in us].index(unum)
        if i > 0:
            step.append(f'<a href="{r(unit_dir(us[i - 1]["num"]) / "index.html")}">&larr; Unit {us[i - 1]["num"]}</a>')
        if i < len(us) - 1:
            step.append(f'<a class="apn-next" href="{r(unit_dir(us[i + 1]["num"]) / "index.html")}">Unit {us[i + 1]["num"]} &rarr;</a>')
    if step:
        parts.append(f'<div class="apn-step">{"".join(step)}</div>')
    return f'<nav class="apnav" aria-label="Course"{_track(c)}>{"".join(parts)}</nav>'


# ---------------------------------------------------------------- apply --
_OLD = [
    re.compile(r'[ \t]*<nav class="apnav".*?</nav>\n?', re.S),
    re.compile(r'[ \t]*<link id="apnav-(?:css|icon|icon32|touch)"[^>]*>\n?'),
    re.compile(r'[ \t]*<script id="apnav-(?:js|map|progress)"[^>]*></script>\n?'),
    re.compile(r'[ \t]*<meta id="apnav-(?:og-site|og-desc|og-image|card)"[^>]*>\n?'),
]
SHARE_DESC = "The complete AP Cybersecurity course: textbook, lectures, practice, quizzes and a capstone. Free to use."


def head_links(page_dir):
    r = lambda p: rel(page_dir, p)
    return (f'<link id="apnav-icon" rel="icon" href="{r(THEME / "icon.svg")}" type="image/svg+xml">\n'
            f'<link id="apnav-icon32" rel="icon" href="{r(THEME / "icon-32.png")}" sizes="32x32" type="image/png">\n'
            f'<link id="apnav-touch" rel="apple-touch-icon" href="{r(THEME / "apple-touch-icon.png")}">\n'
            f'<link id="apnav-css" rel="stylesheet" href="{r(THEME / "aayat.css")}">\n'
            f'<script id="apnav-map" src="{r(THEME / "course-map.js")}" defer></script>\n'
            f'<script id="apnav-js" src="{r(THEME / "aayat.js")}" defer></script>\n'
            f'<script id="apnav-progress" src="{r(THEME / "progress.js")}" defer></script>\n'
            f'<meta id="apnav-og-site" property="og:site_name" content="{esc(BRAND)} · {esc(SUBJECT)}">\n'
            f'<meta id="apnav-og-desc" property="og:description" content="{esc(SHARE_DESC)}">\n'
            f'<meta id="apnav-og-image" property="og:image" content="{SITE_URL}assets/theme/share-banner.png">\n'
            f'<meta id="apnav-card" name="twitter:card" content="summary_large_image">\n')


def apply(path, text):
    """Bar, stylesheet, icon and title for a student page. Idempotent; pages with no context come back as they are."""
    path = Path(path)
    c = context(path)
    if c is None:
        return text
    for rx in _OLD:
        text = rx.sub("", text)
    page_dir = path.parent
    text = text.replace("</head>", head_links(page_dir) + "</head>", 1)
    text = re.sub(r"(<body[^>]*>)\n?", lambda m: m.group(1) + "\n" + nav_html(page_dir, c) + "\n", text, count=1)
    t = title_for(c)
    if t:
        text = re.sub(r"<title>.*?</title>", f"<title>{esc(t)}</title>", text, count=1, flags=re.S)
    return text


def shell(path, title, body, cls=""):
    """A whole page in the site style. The bar is added when the page has a context."""
    page_dir = Path(path).parent
    text = (f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{esc(title)}</title>\n</head>\n<body class="aa{(" " + cls) if cls else ""}">\n'
            f'<main class="aa-main">\n{body}\n</main>\n</body>\n</html>\n')
    if context(path) is None:
        return text.replace("</head>", head_links(page_dir) + "</head>", 1)
    return apply(path, text)
