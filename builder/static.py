"""Files used as they are: source/static/** keeps its path under site/; per-topic notes, images and
sims, flashcard decks, classwork quizzes, tutor-post banners, lecture images and the capstone world
go to their place in the site. Student pages get the top bar on the way."""
from . import course as C
from . import nav as N
from .paths import (ASSETS, CAPSTONE, CAPSTONE_SRC, LECTURES, LECTURES_SRC, SITE, STATIC_SRC, UNITS_SRC,
                    atom_dir, teacher_atom, topic_dir)
from .util import emit, emit_bytes, rd

TEXT = {".html", ".css", ".js", ".json", ".svg", ".xml", ".txt", ".md", ".mmd", ".yaml"}


def copy(src, dst):
    if src.suffix == ".html":
        emit(dst, N.apply(dst, rd(src)))
    elif src.suffix in TEXT:
        emit(dst, rd(src))
    else:
        emit_bytes(dst, src.read_bytes())


def tree(src_dir, dst_dir, skip=()):
    for p in sorted(src_dir.rglob("*")):
        if p.is_file() and p.suffix not in skip and "__pycache__" not in p.parts:
            copy(p, dst_dir / p.relative_to(src_dir))


def run():
    tree(STATIC_SRC, SITE)
    for tid in C.order():
        src = C.topic(tid)["src"]
        if (src / "notes.html").exists():
            copy(src / "notes.html", topic_dir(tid) / "notes.html")
        if (src / "images").is_dir():
            tree(src / "images", topic_dir(tid) / "images", skip={".mmd"})
        if (src / "flashcards.json").exists():
            copy(src / "flashcards.json", ASSETS / "flashcards" / "data" / f"{tid}.json")
        for a in C.topic_atoms(tid):
            if (a["src"] / "sim.html").exists():
                copy(a["src"] / "sim.html", atom_dir(a["id"]) / "sim.html")
            if (a["src"] / "lab.html").exists():
                copy(a["src"] / "lab.html", atom_dir(a["id"]) / "lab.html")
            if (a["src"] / "banner.png").exists():
                copy(a["src"] / "banner.png", teacher_atom(a["id"]) / "banner.png")
    for u in C.units():
        cw = UNITS_SRC / f"unit-{u['num']}" / "classwork-quiz.json"
        if cw.exists():
            copy(cw, ASSETS / "quizzes" / "data" / f"U{u['num']}.json")
    if (LECTURES_SRC / "images").is_dir():
        tree(LECTURES_SRC / "images", LECTURES / "images")
    tree(CAPSTONE_SRC / "world", CAPSTONE / "data" / "world")
    tree(CAPSTONE_SRC / "stages", CAPSTONE / "data" / "stages")
