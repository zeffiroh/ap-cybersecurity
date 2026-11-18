import functools
import re
import sys
import http.server
import json
import shutil
import socketserver
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
OUT = ROOT / ".cache" / "demos"
sys.path.insert(0, str(ROOT))

from . import video as V


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def groups(which):
    from builder import seminars as S
    names = [p.name for p in S.folders()]
    if which in ("all", ""):
        return [n for n in names if re.match(r"(t-|f-|s\d\d-|n\d\d-|x\d\d-)", n)]
    pick = {"tutorials": r"t-", "seminars": r"(f-|s\d\d-)", "network": r"n\d\d-", "sims": r"x\d\d-"}
    if which in pick:
        return [n for n in names if re.match(pick[which], n)]
    return [w.strip() for w in which.split(",") if w.strip()]


def about(name):
    p = ROOT / "source" / "seminars" / name / "seminar.json"
    j = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    kicker = j.get("kicker") or ("Free tutorial" if name.startswith("t-") else "Network lab" if re.match(r"n\d\d-", name) else "Simulation" if re.match(r"x\d\d-", name) else "Seminar")
    title = j.get("title") or name
    if title.lower().startswith(kicker.lower() + ":"):
        title = title[len(kicker) + 1:].strip()
    return title, j.get("summary") or "", kicker


def run(name, speed=1.0, level=""):
    todo = groups(name) if name in ("all", "tutorials", "seminars", "network", "sims") or "," in name else [name]
    bad = 0
    for one in todo:
        print(f"== {one}")
        bad += run_one(one, speed, level) or 0
    if len(todo) > 1:
        print(f"Made {len(todo) - bad} of {len(todo)} videos in {OUT}")
    return 1 if bad else 0


def run_one(name, speed=1.0, level=""):
    from playwright.sync_api import sync_playwright
    sim = bool(re.match(r"x\d\d-", name))
    cid = "sem-" + name + (f"--{level}" if level and not sim else "")
    if not (SITE / "assets" / "linux" / "cases" / cid / "manifest.json").exists():
        print(f"There's no built lab called {cid}. Run: ./teach build {name}")
        return 1
    folder = OUT / name
    if folder.exists():
        shutil.rmtree(folder)
    (folder / "raw").mkdir(parents=True)
    title, summary, kicker = about(name)
    handler = functools.partial(Quiet, directory=str(SITE))
    with socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler) as server:
        port = server.server_address[1]
        threading.Thread(target=server.serve_forever, daemon=True).start()
        with sync_playwright() as p:
            browser = p.chromium.launch()
            cards = browser.new_page(viewport={"width": V.W, "height": V.H})
            start_card, end_card = V.make_cards(cards, folder, kicker, title, summary)
            cards.close()
            ctx = browser.new_context(viewport={"width": V.W, "height": V.H}, record_video_dir=str(folder / "raw"),
                                      record_video_size={"width": V.W, "height": V.H}, user_agent=V.UA)
            if sim:
                import importlib.util
                spec = importlib.util.spec_from_file_location("browser_bench", ROOT / "tests" / "browser_bench.py")
                bench = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(bench)
                ctx.add_init_script(bench.LABS)
            page = ctx.new_page()
            began = page.evaluate("Date.now()")
            page.set_default_timeout(4 * 3600 * 1000)
            url = (f"http://127.0.0.1:{port}/workstation.html?case={cid}&lab=1&sim={level or 'walk'}&demo=rec&speed={speed}" if sim else
                   f"http://127.0.0.1:{port}/notebook.html?ref=demo-{cid}&runbook={cid}&demo=rec&speed={speed}")
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
    if not (video and Path(video).exists()):
        print("No video was recorded.")
        return 1
    skip = max(0.0, (result.get("t0", began) - began) / 1000)
    length = result.get("length", 0)
    mp4 = folder / f"{name}.mp4"
    V.run_ffmpeg(["-loop", "1", "-t", str(V.CARD_SECONDS), "-i", str(start_card),
                  "-ss", f"{skip:.3f}", "-t", f"{length + 1:.3f}", "-i", str(video),
                  "-loop", "1", "-t", str(V.END_SECONDS), "-i", str(end_card),
                  "-filter_complex", "".join(f"[{i}:v]scale={V.W}:{V.H},setsar=1,fps=25,format=yuv420p[v{i}];" for i in range(3)) + "[v0][v1][v2]concat=n=3:v=1:a=0[out]",
                  "-map", "[out]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-movflags", "+faststart", str(mp4)])
    shutil.rmtree(folder / "raw", ignore_errors=True)
    log = result.get("log") or []
    cues = [{"start": x["start"], "end": x["end"], "text": x["text"]} for x in log if x.get("text")]
    chapters = [(x["start"], x["chapter"]) for x in log if x.get("chapter")]
    cues, chapters = V.shift(cues, chapters, V.CARD_SECONDS)
    V.write_captions(folder, name, cues, chapters, f"{kicker}: {title}", summary)
    total = V.CARD_SECONDS + length + 1 + V.END_SECONDS
    (folder / "info.json").write_text(json.dumps({"kind": "demo", "name": name, "title": f"{kicker}: {title}", "video": mp4.name,
                                                  "seconds": round(total, 1)}, indent=1), encoding="utf-8")
    (folder / "log.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Saved in {folder}:")
    print(f"  {name}.mp4       the silent run-through, with your title and end cards")
    print(f"  {name}.srt/.vtt  subtitles (upload the .srt to YouTube; nothing is burned into the picture)")
    print("  chapters.txt, youtube.txt, transcript.md, record-voice.md")
    print(f"  length: {V.clock(total)}.  Add your voice:  python tools/teach.py voice {name}")
    return 0
