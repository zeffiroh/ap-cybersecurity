import functools
import http.server
import json
import shutil
import socketserver
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
OUT = ROOT / ".cache" / "demos"


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def stamp(s, comma=True):
    h, rest = divmod(max(0.0, s), 3600)
    m, sec = divmod(rest, 60)
    ms = int(round((sec - int(sec)) * 1000))
    return f"{int(h):02d}:{int(m):02d}:{int(sec):02d}{',' if comma else '.'}{ms:03d}"


def chapter(s):
    s = int(s)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def write_outputs(folder, name, log):
    lines = [x for x in log if x.get("text")]
    srt = []
    for i, x in enumerate(lines, 1):
        srt += [str(i), f"{stamp(x['start'])} --> {stamp(x['end'])}", x["text"], ""]
    (folder / f"{name}.srt").write_text("\n".join(srt), encoding="utf-8")
    vtt = ["WEBVTT", ""]
    for x in lines:
        vtt += [f"{stamp(x['start'], False)} --> {stamp(x['end'], False)}", x["text"], ""]
    (folder / f"{name}.vtt").write_text("\n".join(vtt), encoding="utf-8")
    chapters = [(0.0, "Opening")] + [(x["start"], x["chapter"]) for x in log if x.get("chapter")]
    seen, keep = set(), []
    for t, n in chapters:
        if n not in seen:
            seen.add(n)
            keep.append((t, n))
    (folder / "chapters.txt").write_text("\n".join(f"{chapter(t)} {n}" for t, n in keep) + "\n", encoding="utf-8")
    words, cur = [], None
    for x in log:
        if x.get("chapter"):
            words += ["", f"## {x['chapter']}", ""]
        elif x.get("text"):
            if x.get("label") != cur and x.get("label") in ("Opening", "Wrap-up"):
                words += ["", f"## {x['label']}", ""]
            cur = x.get("label")
            words.append(x["text"])
    (folder / "transcript.md").write_text(("# Transcript: " + name + "\n" + "\n".join(words)).strip() + "\n", encoding="utf-8")


def run(name, speed=1.0, level=""):
    from playwright.sync_api import sync_playwright
    cid = "sem-" + name + (f"--{level}" if level else "")
    if not (SITE / "assets" / "linux" / "cases" / cid / "manifest.json").exists():
        print(f"There's no built lab called {cid}. Run: ./teach build {name}")
        return 1
    folder = OUT / name
    if folder.exists():
        shutil.rmtree(folder)
    (folder / "raw").mkdir(parents=True)
    handler = functools.partial(Quiet, directory=str(SITE))
    with socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler) as server:
        port = server.server_address[1]
        threading.Thread(target=server.serve_forever, daemon=True).start()
        with sync_playwright() as p:
            browser = p.chromium.launch()
            ctx = browser.new_context(viewport={"width": 1280, "height": 720}, record_video_dir=str(folder / "raw"), record_video_size={"width": 1280, "height": 720})
            page = ctx.new_page()
            page.set_default_timeout(4 * 3600 * 1000)
            url = f"http://127.0.0.1:{port}/notebook.html?ref=demo-{cid}&runbook={cid}&demo=rec&speed={speed}"
            print("Playing", url)
            page.goto(url)
            page.wait_for_function("window.__demo && window.__demo.done", polling=2000)
            result = page.evaluate("window.__demo")
            video = page.video.path() if page.video else None
            ctx.close()
            browser.close()
        server.shutdown()
    if result.get("error"):
        print("The demo stopped:", result["error"])
        return 1
    if video and Path(video).exists():
        shutil.move(video, folder / f"{name}.webm")
    shutil.rmtree(folder / "raw", ignore_errors=True)
    write_outputs(folder, name, result.get("log") or [])
    (folder / "log.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Saved in {folder}:")
    print(f"  {name}.webm      the run-through video (upload to YouTube as Unlisted, or record your voice over it)")
    print(f"  {name}.srt/.vtt  subtitles, the lecture script as captions")
    print("  chapters.txt     paste into the YouTube description")
    print("  transcript.md    what is said, in order, to read over the video")
    print(f"  length: {round(result.get('length', 0) / 60, 1)} minutes")
    return 0
