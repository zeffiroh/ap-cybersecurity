"""The course map: units, topics and skills ("atoms"), read from source/course.json, source/atoms.json
and the folders under source/units/."""
import json
import re
from functools import lru_cache

from .paths import SRC, UNITS_SRC

BRAND = "Aayat-AP-Prep"
SUBJECT = "Cybersecurity"
SITE_URL = "https://zeffiroh.github.io/ap-cybersecurity/"


def tkey(tid):
    return [int(x) if x.isdigit() else x for x in tid.split(".")]


@lru_cache(None)
def _course():
    return json.loads((SRC / "course.json").read_text(encoding="utf-8"))


@lru_cache(None)
def units():
    """[{num, title, topics: [tid]}] in order."""
    c = _course()
    out = []
    for n, title in sorted(c["units"].items(), key=lambda kv: int(kv[0])):
        tids = sorted((t for t, v in c["topics"].items() if v["unit"] == int(n)), key=tkey)
        out.append({"num": int(n), "title": title, "topics": tids})
    return out


def unit(n):
    return next(u for u in units() if u["num"] == int(n))


@lru_cache(None)
def order():
    return [t for u in units() for t in u["topics"]]


@lru_cache(None)
def topic(tid):
    """{unit, title, los, src (source folder)}."""
    t = dict(_course()["topics"][tid])
    hits = sorted((UNITS_SRC / f"unit-{t['unit']}").glob(f"{tid}-*"))
    t["src"] = hits[0]
    return t


@lru_cache(None)
def atoms():
    """{tid: [{id, title, unit, lo, skills, points, src}]} in id order."""
    out = {}
    for a in json.loads((SRC / "atoms.json").read_text(encoding="utf-8")):
        tid = a["id"].rsplit(".", 1)[0]
        src = next(topic(tid)["src"].glob(f"{a['id']}-*"))
        out.setdefault(tid, []).append({
            "id": a["id"], "title": a["bullet"], "unit": a["unit"], "lo": a["lo"], "skills": a["skills"],
            "lab": a.get("lab", False), "port": a.get("port"), "points": a.get("points", 3), "src": src})
    for v in out.values():
        v.sort(key=lambda a: tkey(a["id"]))
    return out


@lru_cache(None)
def atom_order():
    return [a for t in order() for a in atoms().get(t, [])]


def atom(aid):
    return next(a for a in atom_order() if a["id"] == aid)


def topic_atoms(tid):
    return atoms().get(tid, [])


def tid_of(aid):
    return aid.rsplit(".", 1)[0]


def unit_of(tid):
    return int(tid.split(".")[0])


def slug_title(s):
    return re.sub(r"\s+", " ", s).strip()
