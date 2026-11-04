import json

from . import course as C
from . import nav as N
from . import seminars
from .paths import (ASSETS, CAPSTONE, CAPSTONE_SRC, LECTURES, LECTURES_SRC, SITE, STATIC_SRC, UNITS_SRC,
                    atom_dir, teacher_atom, topic_dir)
from .util import emit, emit_bytes, rd

TOOLKIT = STATIC_SRC.parent / "toolkit"
TEACHER_CASES = STATIC_SRC.parent / "teacher-cases"
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


def cases():
    src = STATIC_SRC / "assets" / "linux" / "cases"
    if not src.is_dir():
        return
    skip = {"meta.json", "template.json", "manifest.json", "answers.json"}
    index = []
    for d in sorted(x for x in src.iterdir() if x.is_dir()):
        meta = dict(json.loads(rd(d / "meta.json")), id=d.name)
        files = sorted(p.relative_to(d).as_posix() for p in d.rglob("*") if p.is_file() and p.name not in skip)
        man = dict(meta, files=files, template=json.loads(rd(d / "template.json")))
        emit(ASSETS / "linux" / "cases" / d.name / "manifest.json", json.dumps(man, ensure_ascii=False, indent=1) + "\n")
        index.append(meta)
    for path in sorted(TEACHER_CASES.glob("*.json")):
        bundle = json.loads(rd(path))
        if not bundle.get("published", True):
            continue
        slug = "tc-" + path.stem.removeprefix("case-")
        meta = dict(bundle["meta"], id=slug, teacher=True)
        if meta.get("ctf"):
            meta["ctf"] = meta["ctf"].replace("Show it to your teacher.", "Submit it on the CTF board.")
        names = sorted(bundle["files"])
        for name in names:
            emit(ASSETS / "linux" / "cases" / slug / name, bundle["files"][name])
        man = dict(meta, files=names, template=bundle["template"])
        emit(ASSETS / "linux" / "cases" / slug / "manifest.json", json.dumps(man, ensure_ascii=False, indent=1) + "\n")
        index.append(meta)
    index.extend(seminars.publish())
    index.sort(key=lambda m: (m.get("order", 99), m["id"]))
    emit(ASSETS / "linux" / "cases" / "index.json", json.dumps(index, ensure_ascii=False, indent=1) + "\n")


def toolkit():
    conf = json.loads(rd(TOOLKIT / "toolkit.json"))
    known = {s["name"]: s for s in conf["scripts"]}
    groups = list(conf["groups"])
    scripts = []
    for path in sorted((TOOLKIT / "scripts").glob("tk-*.sh")):
        info = known.get(path.stem, {"name": path.stem, "group": "More", "title": path.stem, "what": "", "args": []})
        if info["group"] not in groups:
            groups.append(info["group"])
        scripts.append(dict(info, src=rd(path).replace("\r", "").rstrip("\n")))
    order = [s["name"] for s in conf["scripts"]]
    scripts.sort(key=lambda s: (groups.index(s["group"]), order.index(s["name"]) if s["name"] in order else len(order)))
    emit(ASSETS / "toolkit" / "scripts.json", json.dumps({"groups": groups, "scripts": scripts}, ensure_ascii=False, indent=1) + "\n")


def run():
    tree(STATIC_SRC, SITE)
    cases()
    toolkit()
    seminars.media()
    for tid in C.order():
        src = C.topic(tid)["src"]
        if (src / "notes.html").exists():
            copy(src / "notes.html", topic_dir(tid) / "notes.html")
        if (src / "images").is_dir():
            tree(src / "images", topic_dir(tid) / "images", skip={".mmd"})
        if (src / "flashcards.json").exists():
            copy(src / "flashcards.json", ASSETS / "flashcards" / "data" / f"{tid}.json")
        for a in C.topic_atoms(tid):
            for kind in ("sim", "lab"):
                if (a["src"] / f"{kind}.html").exists():
                    dst = atom_dir(a["id"]) / f"{kind}.html"
                    emit(dst, N.with_taskbar(dst, a, kind, rd(a["src"] / f"{kind}.html")))
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
