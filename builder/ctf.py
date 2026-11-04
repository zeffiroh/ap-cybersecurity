import base64
import hashlib
import json
import shutil
import urllib.request
import zipfile
from pathlib import Path

from .paths import ASSETS, ROOT, SITE, SRC
from .util import emit, keep, rd

CTF_SRC = SRC / "ctf" / "challenges.json"
LAB_KEY = "aayat-lab"
LABS = ("sqli.html", "shop.html")

CYBERCHEF = SITE / "cyberchef"
CYBERCHEF_VERSION = "v11.5.0"
CYBERCHEF_ZIP = ("https://github.com/gchq/CyberChef/releases/download/v11.5.0/"
                 "CyberChef_8cd426dd4f40f1423912d5fad91b578a86a65112.zip")
CYBERCHEF_SHA256 = "f6478925d3eaa16ec08626a85f5b85eed10d531a5e18700615fed7ecb024cccf"
CACHE = ROOT / ".cache"

NOTICE = f"""CyberChef {CYBERCHEF_VERSION}
Copyright Crown Copyright (GCHQ). Licensed under the Apache License, Version 2.0.
https://github.com/gchq/CyberChef  ·  https://www.apache.org/licenses/LICENSE-2.0
Unmodified release build, served as-is; the precompressed .gz/.br copies are left out.
"""


def teacher_case_challenges():
    out = []
    for path in sorted((SRC / "teacher-cases").glob("*.json")):
        bundle = json.loads(rd(path))
        if not bundle.get("published", True) or not bundle.get("flag"):
            continue
        meta = bundle["meta"]
        out.append({"id": "rb-tc-" + path.stem.removeprefix("case-"), "unit": int((meta.get("units") or [1])[0]), "points": 100, "type": "Lab",
                    "title": meta["title"], "body": meta.get("summary", "") + " Work the case in a notebook and find the flag.\n",
                    "hint": "Read each step of the runbook, then look through the evidence it points to.",
                    "link": "notebook.html#nb-cases-h", "flag": bundle["flag"], "solve": "See the last steps of this case's runbook.", "sort": 60})
    return out


def challenges():
    return json.loads(rd(CTF_SRC))["challenges"] + teacher_case_challenges()


def flag_hash(flag):
    return hashlib.sha256(flag.strip().lower().encode("utf-8")).hexdigest()


def hide(flag):
    b = bytes(c ^ ord(LAB_KEY[i % len(LAB_KEY)]) for i, c in enumerate(flag.encode("utf-8")))
    return base64.b64encode(b).decode()


def sql_text(s):
    return "'" + str(s).replace("'", "''") + "'"


def body_with_files(c):
    fs = c.get("files") or []
    return c["body"] + ("\n\nFiles: " + " ".join(fs) if fs else "")


def seed_sql(cs):
    cols = "id, unit, points, title, body, hint, link, flag_hash, flag, solve, sort, builtin, active"
    rows = ",\n".join("(" + ", ".join([sql_text(c["id"]), str(int(c["unit"])), str(int(c["points"])), sql_text(c["title"]),
                                       sql_text(body_with_files(c)), sql_text(c["hint"]), sql_text(c["link"]), sql_text(flag_hash(c["flag"])),
                                       sql_text(c["flag"]), sql_text(c["solve"]), str(int(c["sort"])), "true", "true"]) + ")"
                      for c in cs)
    keep = ", ".join(sql_text(c["id"]) for c in cs)
    return (f"insert into ctf_challenges ({cols}) values\n{rows}\n"
            "on conflict (id) do update set unit = excluded.unit, points = excluded.points, title = excluded.title,\n"
            "  body = excluded.body, hint = excluded.hint, link = excluded.link, flag_hash = excluded.flag_hash,\n"
            "  flag = excluded.flag, solve = excluded.solve, sort = excluded.sort, builtin = true;\n"
            f"update ctf_challenges set active = false where builtin and id not in ({keep});\n")


def publish_data():
    cs = challenges()
    public = [{k: c[k] for k in ("id", "unit", "points", "title", "body", "hint", "link", "sort")}
              | {"type": c.get("type", ""), "files": c.get("files") or [], "hash": flag_hash(c["flag"])} for c in cs]
    emit(ASSETS / "ctf" / "challenges.js",
         "window.AAYAT_CTF = " + json.dumps(public, ensure_ascii=False, separators=(",", ":")) + ";\n")
    lab = {c["id"]: hide(c["flag"]) for c in cs if c["link"] in LABS}
    emit(ASSETS / "ctf" / "lab-flags.js",
         "window.AAYAT_LABFLAGS = " + json.dumps({"key": LAB_KEY, "flags": lab}, separators=(",", ":")) + ";\n")
    emit(ROOT / "db" / "ctf_challenges.sql", seed_sql(cs))


def cyberchef():
    if (CYBERCHEF / "index.html").exists() and (CYBERCHEF / "NOTICE.txt").exists() \
            and CYBERCHEF_VERSION in (CYBERCHEF / "NOTICE.txt").read_text(encoding="utf-8"):
        return
    CACHE.mkdir(exist_ok=True)
    z = CACHE / f"CyberChef_{CYBERCHEF_VERSION}.zip"
    if not z.exists() or hashlib.sha256(z.read_bytes()).hexdigest() != CYBERCHEF_SHA256:
        print(f"  downloading CyberChef {CYBERCHEF_VERSION}")
        urllib.request.urlretrieve(CYBERCHEF_ZIP, z)
        if hashlib.sha256(z.read_bytes()).hexdigest() != CYBERCHEF_SHA256:
            z.unlink()
            raise RuntimeError("CyberChef download does not match its pinned SHA-256")
    if CYBERCHEF.exists():
        shutil.rmtree(CYBERCHEF)
    with zipfile.ZipFile(z) as zf:
        for info in zf.infolist():
            name = info.filename
            if info.is_dir() or name.endswith((".gz", ".br")) or ".." in Path(name).parts:
                continue
            out = CYBERCHEF / ("index.html" if name == f"CyberChef_{CYBERCHEF_VERSION}.html" else name)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(zf.read(info))
    (CYBERCHEF / "NOTICE.txt").write_text(NOTICE, encoding="utf-8")
    print(f"  CyberChef {CYBERCHEF_VERSION} -> site/cyberchef/")


def gate_tree(folder):
    from .publish import gate
    for page in folder.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        gated = gate(page, text)
        if gated != text:
            page.write_text(gated, encoding="utf-8")


def run():
    publish_data()
    cyberchef()
    gate_tree(CYBERCHEF)
    if (SITE / "lab").is_dir():
        gate_tree(SITE / "lab")
    for f in CYBERCHEF.rglob("*"):
        if f.is_file():
            keep(f)
