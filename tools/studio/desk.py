import json
import mimetypes
import os
import re
import secrets
import shutil
import socket
import subprocess
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from builder import levels, lesson as L
from builder import seminars as S

HERE = Path(__file__).resolve().parent
UI = HERE / "ui"
SITE = ROOT / "site"
PREVIEW = L.STUDIO / ".preview"
WIN = sys.platform == "win32"
STUDIOS = {}
VOICES = {}
LOCK = threading.Lock()
JOB_LOCK = threading.Lock()
ATOMS = []
TEACH = [sys.executable, "-u", str(ROOT / "tools" / "teach.py")]
ENV = dict(os.environ, AAYAT_DESK="1", PYTHONIOENCODING="utf-8")
DEMOS = ROOT / ".cache" / "demos"
LECTURES = ROOT / ".cache" / "lectures"
JOB = {"label": "", "name": "", "lines": [], "started": 0, "ended": 0, "code": None, "proc": None, "stopped": False}


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")


def shells():
    if not WIN:
        return ["bash"]
    try:
        out = subprocess.run(["wsl.exe", "-l", "-q"], capture_output=True, timeout=10).stdout.decode("utf-16-le", "ignore")
    except (OSError, subprocess.SubprocessError):
        return []
    names = [n.strip() for n in out.splitlines() if n.strip() and not n.strip().startswith("docker-")]
    names.sort(key=lambda n: (n != "kali-linux", n != "Ubuntu", n))
    return ["wsl:" + n for n in names]


def sources():
    global ATOMS
    if not ATOMS:
        from builder import course as C
        ATOMS = [{"id": a["id"], "title": f"{a['id']} {a['title']}", "kind": "Lesson"} for a in C.atom_order() if (a["src"] / "problem").is_dir()]
    out = []
    for d in sorted(p for p in L.CASES.iterdir() if (p / "meta.json").exists()):
        out.append({"id": d.name, "title": json.loads((d / "meta.json").read_text(encoding="utf-8"))["title"], "kind": "Case"})
    for p in sorted(L.TEACHER_CASES.glob("*.json")):
        out.append({"id": "tc-" + p.stem.removeprefix("case-"), "title": json.loads(p.read_text(encoding="utf-8"))["meta"]["title"], "kind": "Case"})
    return out + ATOMS


def alive(name):
    item = STUDIOS.get(name)
    if item and item["proc"].poll() is None:
        return item
    STUDIOS.pop(name, None)
    return None


def stop_studio(name):
    item = alive(name)
    if item:
        item["proc"].stdin.close()
        try:
            item["proc"].wait(timeout=25)
        except subprocess.TimeoutExpired:
            item["proc"].kill()
        STUDIOS.pop(name, None)


def start_studio(name, title="", source="", shell="auto"):
    item = alive(name)
    if item:
        return item["link"]
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    args = [sys.executable, "-u", str(ROOT / "tools" / "teach.py"), "studio", name, "--no-open", "--port", str(port), "--shell", shell]
    if title:
        args += ["--title", title]
    if source:
        args += ["--from", source]
    proc = subprocess.Popen(args, cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=dict(os.environ, AAYAT_DESK="1", PYTHONIOENCODING="utf-8"))
    link, seen = None, []
    for raw in proc.stdout:
        line = raw.decode("utf-8", "replace")
        seen.append(line.strip())
        m = re.search(r"http://127\.0\.0\.1:\d+/\?t=\S+", line)
        if m:
            link = m.group(0)
            break
    if not link:
        raise RuntimeError(" ".join(seen[-3:]) or "The studio didn't start.")
    threading.Thread(target=lambda: [None for _ in proc.stdout], daemon=True).start()
    STUDIOS[name] = {"proc": proc, "link": link}
    return link


def lesson_rows():
    names = set()
    if L.STUDIO.is_dir():
        names |= {p.name for p in L.STUDIO.iterdir() if p.is_dir() and not p.name.startswith(".")}
    names |= {p.name for p in S.folders()}
    rows = []
    for name in sorted(names):
        rows.append(lesson_row(name))
    rows.sort(key=lambda r: -r["changed"])
    return rows


def step_files(folder):
    return sorted(folder.glob("[0-9]*.md")) if folder.is_dir() else []


def lesson_row(name):
    session, folder = L.session_dir(name), S.SEMINARS / name
    info = {}
    if (session / "session.json").exists():
        info = json.loads((session / "session.json").read_text(encoding="utf-8"))
    about = S.about(folder) if (folder / "seminar.json").exists() else {}
    pages = not (folder / "lesson.json").exists() and bool(step_files(folder))
    built = (folder / "lesson.json").exists() or pages
    events = L.load_events(session) if session.is_dir() else []
    stamps = [p.stat().st_mtime for p in (session / "events.jsonl", folder / "lesson.json", folder / "seminar.json") if p.exists()]
    item = alive(name)
    return {"name": name, "title": about.get("title") or info.get("title") or name, "kind": "pages" if pages else "recorded",
            "recorded": bool(info), "built": built, "published": bool(about.get("published")),
            "running": bool(item), "link": item["link"] if item else "", "shell": info.get("shell", ""), "minutes": round(info.get("elapsed", 0) / 60, 1),
            "steps": sum(1 for e in events if e["k"] == "step"), "commands": sum(1 for e in events if e["k"] == "cmd"), "edited": (session / "edited").exists(), "changed": max(stamps, default=0)}


def lesson_detail(name):
    folder, session = S.SEMINARS / name, L.session_dir(name)
    data = lesson_row(name)
    data["cells"] = json.loads((folder / "lesson.json").read_text(encoding="utf-8")) if (folder / "lesson.json").exists() else []
    data["about"] = S.about(folder) if (folder / "seminar.json").exists() else {}
    review = session / "review.txt"
    data["review"] = [l for l in review.read_text(encoding="utf-8").splitlines() if l.strip()] if review.exists() else []
    if str(data["about"].get("summary", "")).strip():
        data["review"] = [l for l in data["review"] if not l.startswith("Add a summary")]
    data["problems"] = S.problems(folder) if (folder / "seminar.json").exists() else []
    chapters = folder / "chapters.txt"
    data["chapters"] = chapters.read_text(encoding="utf-8") if chapters.exists() else ""
    data["replay"] = (folder / "replay.json").exists()
    data["pages"] = []
    if data["kind"] == "pages":
        for p in step_files(folder):
            code = next((p.with_suffix(x) for x in (".sh", ".py") if p.with_suffix(x).exists()), None)
            data["pages"].append({"file": p.name, "text": S.read(p), "codeFile": code.name if code else "",
                                  "code": S.read(code) if code else ""})
    return data


def save_pages(name, pages):
    folder = S.SEMINARS / name
    allowed = {p.name for p in step_files(folder)}
    allowed |= {p.with_suffix(x).name for p in step_files(folder) for x in (".sh", ".py") if p.with_suffix(x).exists()}
    for page in pages:
        for key, text in (("file", "text"), ("codeFile", "code")):
            fname = page.get(key) or ""
            if not fname:
                continue
            if fname not in allowed or not isinstance(page.get(text), str):
                raise RuntimeError(f"{fname} isn't one of this lab's step files.")
            body = page[text].replace("\r\n", "\n")
            (folder / fname).write_text(body.rstrip("\n") + "\n", encoding="utf-8", newline="\n")
    return lesson_detail(name)


def lab_group(name):
    if name.startswith("t-"):
        return "Free tutorials"
    if re.match(r"(f-|s\d\d-)", name):
        return "Seminars"
    if re.match(r"n\d\d-", name):
        return "Network labs"
    if re.match(r"x\d\d-", name):
        return "Simulations"
    return ""


def newest(paths):
    return max((p.stat().st_mtime for p in paths if p.exists()), default=0)


def video_state(key, folder, source_time):
    info = {}
    if (folder / "info.json").exists():
        info = json.loads((folder / "info.json").read_text(encoding="utf-8"))
    voiced = sorted(folder.glob("*-voiced.mp4")) if folder.is_dir() else []
    segs = len(list((folder / "voice").glob("seg-*.webm"))) if (folder / "voice").is_dir() else 0
    made = (folder / "info.json").stat().st_mtime if info else 0
    voice = VOICES.get(key)
    live = bool(voice and voice["proc"].poll() is None)
    return {"silent": bool(info), "seconds": info.get("seconds", 0), "takes": segs, "voiced": voiced[0].name if voiced else "",
            "stale": bool(info) and source_time > made + 1, "voicing": live, "voiceLink": voice["link"] if live else ""}


def video_items():
    from . import lecture as LEC
    items = []
    for folder in S.folders():
        group = lab_group(folder.name)
        if not group:
            continue
        about = S.about(folder)
        changed = newest([folder / "seminar.json", *step_files(folder)])
        items.append(dict(key=folder.name, kind="lab", group=group, title=about.get("title") or folder.name,
                          **video_state(folder.name, DEMOS / folder.name, changed)))
    for md in LEC.decks():
        title = LEC.front(md)[0] or md.stem
        items.append(dict(key=md.stem, kind="lecture", group="Lectures", title=f"Lecture {int(md.stem[:2])}: {title}",
                          **video_state(md.stem, LECTURES / md.stem, md.stat().st_mtime)))
    order = ["Lectures", "Free tutorials", "Seminars", "Network labs", "Simulations"]
    items.sort(key=lambda r: (order.index(r["group"]), r["key"]))
    return items


def job_state():
    running = bool(JOB["started"]) and not JOB["ended"]
    return {"running": running, "label": JOB["label"], "name": JOB["name"], "lines": JOB["lines"][-40:], "code": JOB["code"],
            "seconds": round((JOB["ended"] or time.time()) - JOB["started"]) if JOB["started"] else 0, "stopped": JOB["stopped"]}


def kill_tree(proc):
    if proc and proc.poll() is None:
        if WIN:
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True)
        else:
            proc.kill()


def run_job(steps):
    code = 0
    for args in steps:
        JOB["lines"].append("> teach " + " ".join(args))
        try:
            proc = subprocess.Popen(TEACH + args, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=ENV)
        except OSError as e:
            JOB["lines"].append(str(e))
            code = 1
            break
        JOB["proc"] = proc
        for raw in proc.stdout:
            JOB["lines"].append(raw.decode("utf-8", "replace").rstrip())
            del JOB["lines"][:-300]
        code = proc.wait()
        if code or JOB["stopped"]:
            break
    JOB["code"] = 1 if JOB["stopped"] else code
    JOB["proc"] = None
    JOB["ended"] = time.time()


def start_job(label, name, steps):
    with JOB_LOCK:
        if JOB["started"] and not JOB["ended"]:
            raise RuntimeError(f"Still making {JOB['label']}. One video at a time, or the computer runs out of memory. Wait, or press Stop.")
        JOB.update(label=label, name=name, lines=[], started=time.time(), ended=0, code=None, proc=None, stopped=False)
    threading.Thread(target=run_job, args=(steps,), daemon=True).start()
    return job_state()


def stop_job():
    JOB["stopped"] = True
    kill_tree(JOB["proc"])
    return job_state()


def start_voice(key):
    item = VOICES.get(key)
    if item and item["proc"].poll() is None:
        return item["link"]
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    proc = subprocess.Popen(TEACH + ["voice", key, "--no-open", "--port", str(port)], cwd=ROOT, stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=ENV)
    link, seen = None, []
    for raw in proc.stdout:
        line = raw.decode("utf-8", "replace")
        seen.append(line.strip())
        m = re.search(r"http://127\.0\.0\.1:\d+/", line)
        if m:
            link = m.group(0)
            break
    if not link:
        raise RuntimeError(" ".join(s for s in seen[-3:] if s) or "The voice studio didn't start.")
    threading.Thread(target=lambda: [None for _ in proc.stdout], daemon=True).start()
    VOICES[key] = {"proc": proc, "link": link}
    return link


def video_action(action, key):
    item = next((r for r in video_items() if r["key"] == key), None)
    if not item:
        raise RuntimeError(f"There's no video called {key}.")
    if action == "make":
        steps = [["lecture", key]] if item["kind"] == "lecture" else [["script", key], ["build", key], ["demo", key]]
        with JOB_LOCK:
            if JOB["started"] and not JOB["ended"]:
                raise RuntimeError(f"Still making {JOB['label']}. One video at a time, or the computer runs out of memory. Wait, or press Stop.")
            voice = VOICES.pop(key, None)
        if voice:
            kill_tree(voice["proc"])
        return {"job": start_job(item["title"], key, steps)}
    if action == "voice":
        if not item["silent"]:
            raise RuntimeError("Make the silent video first.")
        return {"link": start_voice(key)}
    if action == "mix":
        if not item["takes"]:
            raise RuntimeError("Nothing recorded yet. Record your voice first.")
        voice = VOICES.pop(key, None)
        if voice:
            kill_tree(voice["proc"])
        return {"job": start_job(item["title"] + " (final video)", key, [["voice", key, "--mix"]])}
    if action == "folder":
        folder = (LECTURES if item["kind"] == "lecture" else DEMOS) / key
        if not folder.is_dir():
            raise RuntimeError("There's no video folder yet. Make the silent video first.")
        if WIN:
            os.startfile(folder)
        else:
            subprocess.Popen(["xdg-open", str(folder)])
        return {"ok": True}
    raise RuntimeError("Unknown action.")


def save_lesson(name, body):
    folder, session = S.SEMINARS / name, L.session_dir(name)
    if not (folder / "seminar.json").exists():
        raise RuntimeError("Build this lesson before you edit it.")
    if "cells" in body:
        cells = []
        for c in body["cells"]:
            if c.get("t") not in ("md", "sh", "py") or not isinstance(c.get("s"), str):
                raise RuntimeError("A step has text the site can't read.")
            cell = {k: c[k] for k in ("t", "s", "e", "r", "a") if k in c}
            if isinstance(c.get("k"), dict) and all(isinstance(v, list) and all(isinstance(x, str) for x in v) for k, v in c["k"].items() if k in ("out", "cmd")):
                cell["k"] = {k: c["k"][k] for k in ("out", "cmd") if k in c["k"]}
            cells.append(cell)
        (folder / "lesson.json").write_text(json.dumps(cells, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
        if session.is_dir():
            (session / "edited").write_text("1", encoding="utf-8")
    if "about" in body:
        about = S.about(folder)
        given = body["about"]
        for key in ("title", "summary", "level"):
            if key in given:
                about[key] = str(given[key]).strip()
        if "minutes" in given:
            about["minutes"] = max(1, int(given["minutes"] or 1))
        if "units" in given:
            about["units"] = [int(u) for u in re.findall(r"\d+", str(given["units"]))]
        if "published" in given:
            about["published"] = bool(given["published"])
        (folder / "seminar.json").write_text(json.dumps(about, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    return lesson_detail(name)


def build_lesson(name, force):
    session = L.session_dir(name)
    if (session / "edited").exists() and not force:
        return {"needsConfirm": True}
    report = L.finish(name)
    (session / "edited").unlink(missing_ok=True)
    return dict(lesson_detail(name), report=report)


def make_preview(name):
    folder = S.SEMINARS / name
    bad = S.problems(folder)
    if bad:
        raise RuntimeError(bad[0])
    with LOCK:
        kept = S.ASSETS, S.SITE, levels.ASSETS, levels.GUIDES
        shutil.rmtree(PREVIEW, ignore_errors=True)
        S.ASSETS, S.SITE = PREVIEW / "assets", PREVIEW
        levels.ASSETS, levels.GUIDES = PREVIEW / "assets", PREVIEW / "media" / "guides"
        try:
            S.publish_one(folder)
        finally:
            S.ASSETS, S.SITE, levels.ASSETS, levels.GUIDES = kept
    cid = "sem-" + name
    base = f"/site/notebook.html?ref=preview-{secrets.token_hex(3)}"
    return {"worked": f"{base}a&runbook={cid}", "guided": f"{base}b&runbook={cid}--guided", "solo": f"{base}c&runbook={cid}--solo",
            "guide": f"/site/media/guides/{cid}/index.html", "replay": f"/site/replay.html?case={cid}" if (folder / "replay.json").exists() else ""}


def dry_run():
    if WIN:
        args = ["cmd", "/c", str(ROOT / "publish.cmd"), "-n"]
    else:
        args = ["bash", "publish", "-n"]
    done = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
    return {"code": done.returncode, "output": (done.stdout + done.stderr)[-6000:]}


class Desk(BaseHTTPRequestHandler):
    token = ""
    port = 0
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):
        pass

    def send_body(self, code, body, kind):
        self.send_response(code)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, obj, code=200):
        self.send_body(code, json.dumps(obj, ensure_ascii=False).encode("utf-8"), "application/json")

    def send_path(self, path, base):
        path = path.resolve()
        if path != base.resolve() and base.resolve() not in path.parents:
            return self.send_body(403, b"Forbidden", "text/plain")
        if path.is_dir():
            path = path / "index.html"
        if not path.is_file():
            return self.send_body(404, b"Not found", "text/plain")
        kind = "application/wasm" if path.suffix == ".wasm" else mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self.send_body(200, path.read_bytes(), kind)

    def allowed(self):
        return self.headers.get("Host") in {f"127.0.0.1:{self.port}", f"localhost:{self.port}"}

    def api_ok(self):
        return self.allowed() and self.headers.get("X-Desk") == self.token

    def do_GET(self):
        if not self.allowed():
            return self.send_body(403, b"Forbidden", "text/plain")
        url = urlsplit(self.path)
        path = unquote(url.path)
        query = parse_qs(url.query)
        if path == "/":
            if query.get("t", [""])[0] != self.token:
                return self.send_body(403, b"Open the link the Teaching Desk printed in your terminal.", "text/plain")
            return self.send_path(UI / "desk.html", UI)
        if path.startswith("/ui/"):
            return self.send_path(UI / path[4:], UI)
        if path.startswith("/site/"):
            rel = path[6:]
            if rel == "assets/shared/paywall.js":
                return self.send_body(200, b"", "text/javascript")
            draft = PREVIEW / rel
            return self.send_path(draft, PREVIEW) if draft.is_file() else self.send_path(SITE / rel, SITE)
        if not self.api_ok():
            return self.send_json({"error": "This page is out of date. Reopen the Teaching Desk link."}, 403)
        try:
            if path == "/api/state":
                return self.send_json({"lessons": lesson_rows(), "sources": sources(), "shells": shells(), "windows": WIN})
            if path == "/api/lesson":
                return self.send_json(lesson_detail(slugify(query.get("name", [""])[0])))
            if path == "/api/videos":
                return self.send_json({"items": video_items(), "job": job_state()})
            if path == "/api/job":
                return self.send_json(job_state())
        except Exception as e:
            return self.send_json({"error": str(e)}, 500)
        self.send_body(404, b"Not found", "text/plain")

    def do_POST(self):
        size = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(size) if size else b"{}"
        origin = {f"http://127.0.0.1:{self.port}", f"http://localhost:{self.port}"}
        if not self.api_ok() or self.headers.get("Origin") not in origin:
            return self.send_json({"error": "This page is out of date. Reopen the Teaching Desk link."}, 403)
        try:
            body = json.loads(raw)
            name = slugify(body.get("name", ""))
            path = urlsplit(self.path).path
            if path == "/api/video":
                return self.send_json(video_action(str(body.get("action", "")), str(body.get("name", ""))))
            if path == "/api/video-stop":
                return self.send_json(stop_job())
            if path != "/api/dryrun" and not name:
                raise RuntimeError("Give the lesson a short name.")
            if path == "/api/pages":
                return self.send_json(save_pages(name, body.get("pages") or []))
            if path == "/api/rebuild":
                return self.send_json({"job": start_job(lesson_row(name)["title"] + " (build)", name, [["build", name]])})
            if path == "/api/new":
                if L.session_dir(name).exists() or (S.SEMINARS / name).exists():
                    raise RuntimeError(f"You already have a lesson called {name}. Choose another name.")
                return self.send_json({"name": name, "link": start_studio(name, body.get("title", ""), body.get("source", ""), body.get("shell") or "auto")})
            if path == "/api/open":
                return self.send_json({"name": name, "link": start_studio(name, shell=body.get("shell") or "auto")})
            if path == "/api/stop":
                stop_studio(name)
                return self.send_json({"ok": True})
            if path == "/api/build":
                stop_studio(name)
                return self.send_json(build_lesson(name, bool(body.get("force"))))
            if path == "/api/save":
                return self.send_json(save_lesson(name, body))
            if path == "/api/preview":
                return self.send_json(make_preview(name))
            if path == "/api/dryrun":
                return self.send_json(dry_run())
            self.send_json({"error": "Unknown action."}, 404)
        except Exception as e:
            self.send_json({"error": str(e)}, 400)


def run(port=8760, open_page=True):
    Desk.token, Desk.port = secrets.token_urlsafe(24), port
    server = ThreadingHTTPServer(("127.0.0.1", port), Desk)
    link = f"http://127.0.0.1:{port}/?t={Desk.token}"
    print(f"Teaching Desk is open.\n  {link}\n  Press Ctrl+C here to close it. Recordings save as you go.", flush=True)
    if open_page:
        webbrowser.open(link)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        for name in list(STUDIOS):
            stop_studio(name)
        for item in list(VOICES.values()):
            kill_tree(item["proc"])
        JOB["stopped"] = True
        kill_tree(JOB["proc"])
        shutil.rmtree(PREVIEW, ignore_errors=True)
