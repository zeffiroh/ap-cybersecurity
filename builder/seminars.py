import hashlib
import json
import re

from . import levels
from .course import fill_site
from .paths import ASSETS, SITE, SRC
from .util import emit, emit_bytes

SEMINARS = SRC / "seminars"
MEDIA = SRC / "media"
CODE = {".sh": "sh", ".py": "py"}
NOT_STEPS = {"script.md", "README.md"}
TOOLS = ["grep", "awk", "sed", "sort", "uniq", "cut", "nmap", "curl", "wget", "tshark", "dig", "whois", "nc", "openssl",
         "sha256sum", "base64", "tar", "strings", "find", "nikto", "gobuster"]
ANSWER = re.compile(r"^(\s*\?>\s*.+?\s*::\s*)(?!sha256:)(.+?)\s*$", re.M)
SLA_LEVELS = ("critical", "high", "medium", "low", "info")


def sla_of(raw):
    if raw is None:
        return None, []
    if not isinstance(raw, dict):
        return None, ['"sla" must be a block like {"critical": 30, "high": 60}']
    out, bad = {}, []
    for k, v in raw.items():
        if k == "note":
            if not isinstance(v, str):
                bad.append('"sla" note must be text')
            elif v.strip():
                out["note"] = v.strip()[:300]
        elif k not in SLA_LEVELS:
            bad.append(f'"sla" has "{k}"; use {", ".join(SLA_LEVELS)} or note')
        elif isinstance(v, bool) or not isinstance(v, int) or not 1 <= v <= 43200:
            bad.append(f'"sla" {k} must be whole minutes from 1 to 43200, not {v!r}')
        else:
            out[k] = v
    if not bad and not any(k in out for k in SLA_LEVELS):
        bad.append('"sla" needs minutes for at least one severity')
    return (None if bad else out), bad


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
            cells.append({"t": "md", "s": hide_answers(fill_site(src))})
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
    out.extend("seminar.json: " + p for p in sla_of(info.get("sla"))[1])
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


def intro_cell(title, text, names):
    intro = f"# {title}\n\n{text}".rstrip()
    if names:
        intro += "\n\nThe files for this seminar are in `~/case` (Linux) and `case/` (Python): " + ", ".join(f"`{n}`" for n in names) + "."
    return {"t": "md", "s": intro}


def step_groups(folder):
    items = [p for p in folder.iterdir() if p.is_file() and p.suffix in (".md", ".sh", ".py", ".ipynb") and p.name not in NOT_STEPS]
    out = {}
    for stem in sorted({p.stem for p in items}):
        group = {p.suffix: p for p in items if p.stem == stem}
        cells = []
        if ".md" in group:
            text = hide_answers(fill_site(read(group[".md"])))
            cells.append({"t": "md", "s": text if text.lstrip().startswith("#") else heading(stem) + "\n\n" + text})
        elif ".sh" in group or ".py" in group:
            cells.append({"t": "md", "s": heading(stem)})
        for suffix, kind in CODE.items():
            if suffix in group:
                cells.append({"t": kind, "s": read(group[suffix])})
        if ".ipynb" in group:
            cells.extend(from_ipynb(group[".ipynb"]))
        out[stem] = cells
    return out


def cells_of(folder, info):
    names = [p.relative_to(folder / "files").as_posix() for p in evidence(folder)]
    cells = [intro_cell(info["title"], info.get("summary", ""), names)]
    compiled = folder / "lesson.json"
    if compiled.exists():
        for c in json.loads(compiled.read_text(encoding="utf-8")):
            cells.append(dict(c, s=hide_answers(fill_site(c["s"]))) if c["t"] == "md" else c)
        return cells
    for group in step_groups(folder).values():
        cells.extend(group)
    return cells


PRACTICE = "practice"
HINT_BLOCK = re.compile(r"(?m)^>\s*Hint:.*(?:\n>.*)*\n?")
ASK_LINE = re.compile(r"(?m)^\s*\?>.*\n?")
TOOL_FENCE = re.compile(r"```tool\s")


def practice_info(folder):
    p = folder / PRACTICE / "practice.json"
    if not p.exists():
        return {}, []
    try:
        data = json.loads(read(p))
    except ValueError as e:
        return {}, [f"practice/practice.json is not valid JSON: {e}"]
    return (data, []) if isinstance(data, dict) else ({}, ["practice/practice.json must be a block like {\"steps\": {...}}"])


def practice_evidence(folder):
    base = folder / PRACTICE / "files"
    return sorted(p for p in base.rglob("*") if p.is_file()) if base.is_dir() else []


def step_rule(rules, stem):
    num = re.match(r"^(\d+)", stem)
    return rules.get(stem) or (rules.get(num.group(1)) if num else None) or {}


def harder(text, rule):
    text = HINT_BLOCK.sub("", text)
    asks = rule.get("ask")
    if isinstance(asks, list) and asks:
        text = ASK_LINE.sub("", text)
    text = re.sub(r"\n{3,}", "\n\n", text).rstrip()
    extra = []
    if isinstance(rule.get("hint"), str) and rule["hint"].strip():
        extra.append("> Hint: " + rule["hint"].strip())
    if isinstance(asks, list):
        extra += [hide_answers(f"?> {q} :: {a}") for q, a in asks]
    return "\n\n".join([text] + extra) if extra else text


def practice_problems(folder):
    data, bad = practice_info(folder)
    pdir = folder / PRACTICE
    mine = step_groups(pdir) if pdir.is_dir() else {}
    for stem, group in mine.items():
        for c in group:
            if c["t"] == "py":
                try:
                    compile(c["s"], f"practice/{stem}.py", "exec")
                except SyntaxError as e:
                    bad.append(f"practice/{stem}.py line {e.lineno}: {e.msg}")
    for p in practice_evidence(folder):
        try:
            p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            bad.append(f"practice/files/{p.relative_to(pdir / 'files').as_posix()} isn't text")
    if not practice_evidence(folder) or (folder / "lesson.json").exists():
        return bad, []
    gaps = []
    for stem, group in step_groups(folder).items():
        if stem in mine:
            continue
        text = "\n".join(c["s"] for c in group if c["t"] == "md")
        if TOOL_FENCE.search(text):
            gaps.append(f"step {stem} uses a program on the first evidence: write practice/{stem}.md for the second evidence")
        elif "?>" in text:
            gaps.append(f"step {stem} asks about the first evidence: write practice/{stem}.md for the second evidence")
    return bad, gaps


def practice_cells(folder, info):
    data, _ = practice_info(folder)
    rules = data.get("steps") if isinstance(data.get("steps"), dict) else {}
    bad, gaps = practice_problems(folder)
    own = bool(practice_evidence(folder)) and not bad and not gaps
    pdir = folder / PRACTICE
    mine = step_groups(pdir) if pdir.is_dir() and not bad and (own or not practice_evidence(folder)) else {}
    if own:
        files, root = practice_evidence(folder), pdir / "files"
        text = str(data.get("intro") or "Practice uses a different case from the walkthrough: the same skills, new evidence, fewer hints.")
    else:
        files, root = evidence(folder), folder / "files"
        text = str(data.get("intro_same") or info.get("summary", ""))
    cells = [intro_cell(info["title"] + " (Practice)", text, [p.relative_to(root).as_posix() for p in files])]
    if (folder / "lesson.json").exists():
        return cells + [dict(c, s=harder(c["s"], {})) if c["t"] == "md" else c for c in cells_of(folder, info)[1:]], [], bad
    walk = step_groups(folder)
    for stem in sorted(set(walk) | set(mine)):
        if stem in mine:
            cells.extend(mine[stem])
            continue
        rule = {} if own else step_rule(rules, stem)
        for c in walk[stem]:
            if c["t"] == "md":
                cells.append(dict(c, s=harder(c["s"], rule)))
            else:
                cells.append({k: v for k, v in c.items() if not (own and k == "e")})
    return cells, files if own else [], bad + gaps


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
    extra = {}
    for kind in ("net", "replay"):
        base = folder / kind
        for p in sorted(base.rglob("*")) if base.is_dir() else []:
            if p.is_file():
                extra[kind + "/" + p.relative_to(base).as_posix()] = p.read_text(encoding="utf-8")
    for tool in info.get("replayTools") or []:
        extra["bin/" + tool] = f'exec aayat-replay --tool {tool} "$@"\n'
    for name, body in extra.items():
        files.append(name)
        emit(case_dir / name, body)
    practice = None
    if info.get("seminar_id"):
        p_cells, p_files, _ = practice_cells(folder, info)
        practice = {"template": p_cells}
        if p_files:
            p_dir = ASSETS / "linux" / "cases" / f"{slug}--guided"
            names = []
            for p in p_files:
                name = "case/" + p.relative_to(folder / PRACTICE / "files").as_posix()
                names.append(name)
                emit(p_dir / name, p.read_text(encoding="utf-8"))
            for name, body in extra.items():
                names.append(name)
                emit(p_dir / name, body)
            p_expected = folder / PRACTICE / "expected.json"
            if p_expected.exists():
                practice["template"] = levels.merge_expected(p_cells, json.loads(p_expected.read_text(encoding="utf-8")))
            practice.update(files=names, caseDir=f"{slug}--guided")
            p_info = practice_info(folder)[0]
            if p_info.get("handin"):
                practice["handin"] = str(p_info["handin"])
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
    if isinstance(info.get("app"), dict) and info["app"].get("name"):
        meta["app"] = {"name": str(info["app"]["name"]), "url": str(info["app"].get("url", ""))}
    if isinstance(info.get("rubric"), list) and info["rubric"]:
        meta["rubric"] = [[str(c), int(m)] for c, m in info["rubric"]][:20]
    if info.get("handin"):
        meta["handin"] = str(info["handin"])
    if isinstance(info.get("sim"), dict):
        meta["sim"] = True
    cast = folder / "replay.json"
    if cast.exists():
        meta["replay"] = True
        emit(case_dir / "replay.json", cast.read_text(encoding="utf-8"))
    man = dict(meta, files=files, template=levels.merge_expected(cells, expected_of(folder)))
    if isinstance(info.get("script"), dict):
        man["script"] = info["script"]
    if isinstance(info.get("sim"), dict):
        man["sim"] = info["sim"]
    sla = sla_of(info.get("sla"))[0]
    if sla:
        man["sla"] = sla
    man["levels"] = levels.publish(man, practice)
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
