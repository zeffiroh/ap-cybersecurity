import hashlib
import json
import re

from . import levels
from .paths import ASSETS, SITE, SRC
from .util import emit, emit_bytes

SEMINARS = SRC / "seminars"
MEDIA = SRC / "media"
CODE = {".sh": "sh", ".py": "py"}
NOT_STEPS = {"script.md", "README.md"}
TOOLS = ["grep", "awk", "sed", "sort", "uniq", "cut", "nmap", "curl", "wget", "tshark", "dig", "whois", "nc", "openssl",
         "sha256sum", "base64", "tar", "strings", "find", "nikto", "gobuster"]
ANSWER = re.compile(r"^(\s*\?>\s*.+?\s*::\s*)(?!sha256:)(.+?)\s*$", re.M)


def folders():
    if not SEMINARS.is_dir():
        return []
    return sorted(p for p in SEMINARS.iterdir() if p.is_dir() and (p / "seminar.json").exists())


def about(folder):
    return json.loads((folder / "seminar.json").read_text(encoding="utf-8"))


def norm(text):
    return re.sub(r"\s+", " ", text.lower().strip())


def hide_answers(text):
    return ANSWER.sub(lambda m: m.group(1) + "sha256:" + hashlib.sha256(norm(m.group(2)).encode("utf-8")).hexdigest(), text)


def heading(stem):
    m = re.match(r"^(\d+)[-_ ]*(.*)$", stem)
    words = (m.group(2) if m else stem).replace("-", " ").replace("_", " ").strip()
    words = words[:1].upper() + words[1:]
    return f"## {int(m.group(1))}. {words}" if m else f"## {words}"


def read(path):
    return path.read_text(encoding="utf-8").replace("\r", "").strip("\n")


def from_ipynb(path):
    cells = []
    for c in json.loads(path.read_text(encoding="utf-8")).get("cells", []):
        src = c.get("source", "")
        src = "".join(src) if isinstance(src, list) else src
        if not src.strip():
            continue
        if c.get("cell_type") == "markdown":
            cells.append({"t": "md", "s": hide_answers(src)})
        elif src.lstrip().startswith("%%bash"):
            cells.append({"t": "sh", "s": src.split("\n", 1)[1] if "\n" in src else ""})
        else:
            cells.append({"t": "py", "s": src})
    return cells


def evidence(folder):
    base = folder / "files"
    return sorted(p for p in base.rglob("*") if p.is_file()) if base.is_dir() else []


def problems(folder):
    out = []
    try:
        info = about(folder)
    except ValueError as e:
        return [f"seminar.json is not valid JSON: {e}"]
    if not str(info.get("title", "")).strip():
        out.append("seminar.json needs a title")
    items = [p for p in folder.iterdir() if p.is_file() and p.suffix in (".md", ".sh", ".py", ".ipynb") and p.name not in NOT_STEPS]
    if not items and not (folder / "lesson.json").exists():
        out.append("no .md, .sh, .py or .ipynb files yet")
    for p in items:
        if p.suffix == ".py":
            try:
                compile(read(p), p.name, "exec")
            except SyntaxError as e:
                out.append(f"{p.name} line {e.lineno}: {e.msg}")
    for p in evidence(folder):
        try:
            p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            out.append(f"files/{p.relative_to(folder / 'files').as_posix()} isn't text, so it can't go into the lab Linux")
    return out


def cells_of(folder, info):
    names = [p.relative_to(folder / "files").as_posix() for p in evidence(folder)]
    intro = f"# {info['title']}\n\n{info.get('summary', '')}".rstrip()
    if names:
        intro += "\n\nThe files for this seminar are in `~/case` (Linux) and `case/` (Python): " + ", ".join(f"`{n}`" for n in names) + "."
    cells = [{"t": "md", "s": intro}]
    compiled = folder / "lesson.json"
    if compiled.exists():
        for c in json.loads(compiled.read_text(encoding="utf-8")):
            cells.append(dict(c, s=hide_answers(c["s"])) if c["t"] == "md" else c)
        return cells
    items = [p for p in folder.iterdir() if p.is_file() and p.suffix in (".md", ".sh", ".py", ".ipynb") and p.name not in NOT_STEPS]
    for stem in sorted({p.stem for p in items}):
        group = {p.suffix: p for p in items if p.stem == stem}
        if ".md" in group:
            text = hide_answers(read(group[".md"]))
            cells.append({"t": "md", "s": text if text.lstrip().startswith("#") else heading(stem) + "\n\n" + text})
        elif ".sh" in group or ".py" in group:
            cells.append({"t": "md", "s": heading(stem)})
        for suffix, kind in CODE.items():
            if suffix in group:
                cells.append({"t": kind, "s": read(group[suffix])})
        if ".ipynb" in group:
            cells.extend(from_ipynb(group[".ipynb"]))
    return cells


def tools_in(cells):
    text = "\n".join(c["s"] for c in cells if c["t"] == "sh")
    return [t for t in TOOLS if re.search(rf"\b{t}\b", text)]


def ipynb(cells):
    out = []
    for c in cells:
        if c["t"] == "md":
            out.append({"cell_type": "markdown", "metadata": {}, "source": c["s"]})
        else:
            out.append({"cell_type": "code", "metadata": {"aayat": "sh"} if c["t"] == "sh" else {}, "execution_count": None, "outputs": [],
                        "source": ("%%bash\n" + c["s"]) if c["t"] == "sh" else c["s"]})
    return {"nbformat": 4, "nbformat_minor": 5, "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}}, "cells": out}


def expected_of(folder):
    p = folder / "expected.json"
    try:
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    except ValueError:
        return {}


def publish_one(folder):
    info = about(folder)
    slug = "sem-" + folder.name
    cells = cells_of(folder, info)
    case_dir = ASSETS / "linux" / "cases" / slug
    media = SITE / "media" / "seminars" / folder.name
    files = []
    for p in evidence(folder):
        name = "case/" + p.relative_to(folder / "files").as_posix()
        files.append(name)
        emit(case_dir / name, p.read_text(encoding="utf-8"))
    for kind in ("net", "replay"):
        base = folder / kind
        for p in sorted(base.rglob("*")) if base.is_dir() else []:
            if p.is_file():
                name = kind + "/" + p.relative_to(base).as_posix()
                files.append(name)
                emit(case_dir / name, p.read_text(encoding="utf-8"))
    for tool in info.get("replayTools") or []:
        name = "bin/" + tool
        files.append(name)
        emit(case_dir / name, f'exec aayat-replay --tool {tool} "$@"\n')
    meta = {"order": int(info.get("order", 60)), "title": info["title"], "kicker": info.get("kicker", "Seminar"),
            "units": info.get("units", []), "level": info.get("level", "Beginner"), "minutes": int(info.get("minutes", 30)),
            "summary": info.get("summary", ""), "tools": info.get("tools") or tools_in(cells),
            "titlePrefix": info["title"], "teacher": True, "id": slug}
    if info.get("seminar_id"):
        meta["seminarId"] = int(info["seminar_id"])
    if info.get("free"):
        meta["free"] = True
    if info.get("next"):
        meta["next"] = info["next"]
    if isinstance(info.get("rubric"), list) and info["rubric"]:
        meta["rubric"] = [[str(c), int(m)] for c, m in info["rubric"]][:20]
    if info.get("handin"):
        meta["handin"] = str(info["handin"])
    cast = folder / "replay.json"
    if cast.exists():
        meta["replay"] = True
        emit(case_dir / "replay.json", cast.read_text(encoding="utf-8"))
    man = dict(meta, files=files, template=levels.merge_expected(cells, expected_of(folder)))
    if isinstance(info.get("script"), dict):
        man["script"] = info["script"]
    man["levels"] = levels.publish(man)
    man["guide"] = f"media/guides/{slug}/index.html"
    emit(case_dir / "manifest.json", json.dumps(man, ensure_ascii=False, indent=1) + "\n")
    emit_bytes(media / f"{folder.name}.ipynb", (json.dumps(ipynb(cells), ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    for p in sorted(folder.iterdir()):
        if p.is_file() and p.suffix in CODE:
            emit_bytes(media / p.name, read(p).encode("utf-8") + b"\n")
    return meta


def publish():
    return [publish_one(f) for f in folders() if about(f).get("published", True) and not problems(f)]


def media():
    if not MEDIA.is_dir():
        return
    for p in sorted(MEDIA.rglob("*")):
        if p.is_file():
            emit_bytes(SITE / "media" / p.relative_to(MEDIA), p.read_bytes())
