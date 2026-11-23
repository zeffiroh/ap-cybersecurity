import json
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

from . import video as V

ROOT = V.ROOT
FILM = ROOT / "tools" / "film"
WORK = ROOT / ".cache" / "film"
OUT = ROOT / ".cache" / "demos"
IMAGE = "aayat-film:1"


def docker_path(p):
    s = str(Path(p).resolve()).replace("\\", "/")
    return s


def about(name):
    j = json.loads((ROOT / "source" / "seminars" / name / "seminar.json").read_text(encoding="utf-8"))
    kicker = j.get("kicker") or "Seminar"
    title = j.get("title") or name
    if title.lower().startswith(kicker.lower() + ":"):
        title = title[len(kicker) + 1:].strip()
    return j, title, j.get("summary") or "", kicker


def film_of(name):
    p = ROOT / "source" / "seminars" / name / "film.json"
    if not p.exists():
        sys.exit(f"{name} has no film.json yet, so there's nothing to record.")
    return json.loads(p.read_text(encoding="utf-8"))


def prepare(name, film):
    case = WORK / name / "case"
    if case.exists():
        shutil.rmtree(case)
    shutil.copytree(ROOT / "source" / "seminars" / name / "files", case)
    for rel, text in (film.get("files") or {}).items():
        p = case / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8", newline="\n")
    for rel in film.get("pcap") or []:
        src = case / rel
        src.rename(src.with_suffix(".txt"))
        film.setdefault("setup", []).insert(0, f"python3 /film-tools/pcap.py {shlex.quote(rel[:-5] + '.txt')} {shlex.quote(rel)} && rm {shlex.quote(rel[:-5] + '.txt')}")
    return case


def split_cues(log):
    cues = []
    for c in log:
        if not c.get("text"):
            continue
        parts = V.sentences(c["text"])
        total = sum(len(p.split()) for p in parts) or 1
        t, span = c["start"], c["end"] - c["start"]
        for p in parts:
            d = span * len(p.split()) / total
            cues.append({"start": round(t, 2), "end": round(t + d, 2), "text": p})
            t += d
    return cues


def hosts(film):
    out = []
    for name, ip in (film.get("hosts") or {}).items():
        out += ["--add-host", f"{name}:{ip}"]
    return out


def ensure_image():
    if subprocess.run(["docker", "image", "inspect", IMAGE], capture_output=True).returncode:
        print("Building the Linux desktop image (first time only, about 10 minutes).")
        subprocess.run(["docker", "build", "-t", IMAGE, str(FILM)], check=True)


def check(name):
    ensure_image()
    film = film_of(name)
    case = prepare(name, film)
    lines = ["shopt -s expand_aliases", "cd /case"] + list(film.get("setup") or []) + ["eval \"$(grep '^alias ' ~/.bashrc)\""]
    for sc in film["scenes"]:
        t = sc.get("type")
        if sc.get("use") != "term" or not t or "ctrl+u" not in (sc.get("keys") or []):
            continue
        if t.split()[0] in ("lnav", "duckdb", "less", "vim", "nano") and "<" not in t:
            continue
        lines.append(f"printf '\\n\\033[1m$ %s\\033[0m\\n' {shlex.quote(t)}")
        lines.append(t)
    cmd = ["docker", "run", "--rm", "-i", "--hostname", film.get("host", "analyst-ws")] + hosts(film) + ["-v", f"{docker_path(case)}:/case",
           "-v", f"{docker_path(FILM)}:/film-tools:ro", "-e", "COLUMNS=200", IMAGE, "bash"]
    r = subprocess.run(cmd, input=("\n".join(lines) + "\n").encode("utf-8"))
    return r.returncode


def run(name, keep=False):
    ensure_image()
    film = film_of(name)
    case = prepare(name, film)
    raw = WORK / name / "raw"
    if raw.exists():
        shutil.rmtree(raw)
    raw.mkdir(parents=True)
    (WORK / name / "film.json").write_text(json.dumps(film, ensure_ascii=False, indent=1), encoding="utf-8")
    cmd = ["docker", "run", "--rm", "--shm-size=512m", "--memory=4g","--hostname", film.get("host", "analyst-ws")] + hosts(film) + [
           "-v", f"{docker_path(case)}:/case", "-v", f"{docker_path(raw)}:/out",
           "-v", f"{docker_path(FILM)}:/film-tools:ro", "-v", f"{docker_path(ROOT / 'site' / 'cyberchef')}:/opt/cyberchef:ro", "-v", f"{docker_path(ROOT / 'site')}:/opt/site:ro", "-v", f"{docker_path(WORK / name / 'film.json')}:/film/film.json:ro",
           IMAGE, "desktop.sh", "python3", "/film-tools/director.py", "/film/film.json", "/out/take"]
    print("Recording", name, "in the Linux desktop. This plays in real time.")
    r = subprocess.run(cmd)
    took = raw / "take.json"
    if r.returncode or not took.exists():
        print("The recording didn't finish.")
        return 1
    result = json.loads(took.read_text(encoding="utf-8"))
    if result.get("error"):
        print("The film stopped:", result["error"])
        if not keep:
            return 1
    info, title, summary, kicker = about(name)
    folder = OUT / name
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page()
        start_card, end_card = V.make_cards(page, folder, kicker, title, summary)
        b.close()
    mp4 = folder / f"{name}.mp4"
    length = result["length"]
    V.run_ffmpeg(["-loop", "1", "-t", str(V.CARD_SECONDS), "-i", str(start_card),
                  "-ss", "1.0", "-t", f"{length + 1:.3f}", "-i", str(raw / "take.mp4"),
                  "-loop", "1", "-t", str(V.END_SECONDS), "-i", str(end_card),
                  "-filter_complex", "".join(f"[{i}:v]scale={V.W}:{V.H},setsar=1,fps=25,format=yuv420p[v{i}];" for i in range(3)) + "[v0][v1][v2]concat=n=3:v=1:a=0[out]",
                  "-map", "[out]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-movflags", "+faststart", str(mp4)])
    log = result.get("log") or []
    cues = split_cues(log)
    chapters = [(x["start"], x["chapter"]) for x in log if x.get("chapter")]
    cues, chapters = V.shift(cues, chapters, V.CARD_SECONDS)
    V.write_captions(folder, name, cues, chapters, f"{kicker}: {title}", summary)
    total = V.CARD_SECONDS + length + 1 + V.END_SECONDS
    (folder / "info.json").write_text(json.dumps({"kind": "film", "name": name, "title": f"{kicker}: {title}", "video": mp4.name,
                                                  "seconds": round(total, 1)}, indent=1), encoding="utf-8")
    (folder / "log.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    if not keep:
        shutil.rmtree(raw, ignore_errors=True)
    print(f"Saved in {folder}: {mp4.name} ({V.clock(total)}), subtitles, chapters, youtube.txt and record-voice.md.")
    print(f"Add your voice:  python tools/teach.py voice {name}")
    return 0
