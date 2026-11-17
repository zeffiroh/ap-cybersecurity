import functools
import http.server
import json
import re
import shutil
import socketserver
import threading
from pathlib import Path

from . import video as V

SRC = V.ROOT / "source" / "lectures"
OUT = V.ROOT / ".cache" / "lectures"
FPS = 5

PREP = """() => {
  document.querySelectorAll('.pw-gate,nav.apnav').forEach(e => e.remove());
  document.documentElement.className = '';
  document.body.className = '';
  const s = document.createElement('style');
  s.textContent = '#stage{top:0!important;height:100vh!important}#btn-notes,#btn-prev,#btn-next,#anno-toolbar,#anno-canvas,.pw-gate{visibility:hidden!important}';
  document.head.appendChild(s);
  return SLIDES.map(x => ({ unit: x.unit || '', title: x.slideTitle || '', notes: x.notesBody || '' }));
}"""

SHOW = """async (i) => {
  CUR = i; render();
  document.querySelectorAll('#panel-slide img').forEach(im => { im.loading = 'eager'; });
  const imgs = [...document.querySelectorAll('#panel-slide img')];
  await Promise.race([
    Promise.all(imgs.map(im => im.complete ? 0 : new Promise(ok => { im.onload = im.onerror = ok; }))),
    new Promise(ok => setTimeout(ok, 6000))
  ]);
  await new Promise(ok => setTimeout(ok, 350));
  return imgs.filter(im => !im.naturalWidth).map(im => im.getAttribute('src'));
}"""


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def decks():
    return sorted(SRC.glob("[0-9][0-9]_*.md"))


def pick(which):
    all_ = decks()
    if not which or which == "all":
        return all_
    out = []
    for w in which.split(","):
        w = w.strip()
        m = [p for p in all_ if p.stem == w or p.stem[:2] == w.zfill(2) or p.stem.startswith(w)]
        if not m:
            raise SystemExit(f"No lecture called {w}. Use a number from 1 to {len(all_)}, or all.")
        out += m
    return out


def front(md):
    text = md.read_text(encoding="utf-8")
    get = lambda k: (re.search(rf"(?m)^\s*{k}:\s*[\"']?(.*?)[\"']?\s*$", text) or [None, ""])[1]
    return get("title"), get("description"), get("kicker") or f"Lecture {int(md.stem[:2])}"


def record_one(cards, page, port, md):
    stem = md.stem
    title, about, kicker = front(md)
    folder = OUT / stem
    if folder.exists():
        shutil.rmtree(folder)
    frames = folder / "frames"
    frames.mkdir(parents=True)
    start_card, end_card = V.make_cards(cards, folder, kicker, title, about)
    page.goto(f"http://127.0.0.1:{port}/lectures/{stem}.html")
    page.wait_for_function("typeof SLIDES !== 'undefined' && document.getElementById('panel-slide')", timeout=30000)
    slides = page.evaluate(PREP)
    t = V.CARD_SECONDS
    cues, chapters, plan, broken = [], [], [(start_card, V.CARD_SECONDS)], []
    last_unit = None
    for i, s in enumerate(slides):
        broken += page.evaluate(SHOW, i)
        shot = frames / f"s{i + 1:03d}.png"
        page.screenshot(path=str(shot))
        lines = V.sentences(V.plain(s["notes"]))
        talk = sum(max(1.4, V.speak_seconds(x)) for x in lines)
        dur = max(5.0, talk + 1.5)
        unit = s["unit"].strip()
        if unit and unit != last_unit and i > 0:
            chapters.append((t, unit))
        last_unit = unit or last_unit
        at = t + 0.6
        for x in lines:
            d = max(1.4, V.speak_seconds(x))
            cues.append({"start": at, "end": at + d - 0.05, "text": x})
            at += d
        plan.append((shot, dur))
        t += dur
    plan.append((end_card, V.END_SECONDS))
    listing = folder / "frames.txt"
    rows = []
    for p, d in plan:
        rows += [f"file '{p.as_posix()}'", f"duration {d:.3f}"]
    rows.append(f"file '{plan[-1][0].as_posix()}'")
    listing.write_text("\n".join(rows) + "\n", encoding="utf-8")
    mp4 = folder / f"{stem}.mp4"
    V.run_ffmpeg(["-f", "concat", "-safe", "0", "-i", str(listing), "-vf", f"fps={FPS},format=yuv420p", "-c:v", "libx264",
                  "-preset", "veryfast", "-tune", "stillimage", "-crf", "20", "-g", str(FPS * 10), "-movflags", "+faststart", str(mp4)])
    V.write_captions(folder, stem, cues, chapters, f"{kicker}: {title}", about)
    (folder / "info.json").write_text(json.dumps({"kind": "lecture", "name": stem, "title": f"{kicker}: {title}", "video": mp4.name,
                                                  "slides": len(slides), "seconds": round(t + V.END_SECONDS, 1)}, indent=1), encoding="utf-8")
    shutil.rmtree(frames, ignore_errors=True)
    listing.unlink()
    return folder, t + V.END_SECONDS, len(slides), sorted(set(broken))


def run(which=""):
    from playwright.sync_api import sync_playwright
    todo = pick(which)
    if not (V.SITE / "lectures").is_dir():
        raise SystemExit("The lecture decks aren't built. Run: python build.py --only lectures")
    handler = functools.partial(Quiet, directory=str(V.SITE))
    with socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler) as server:
        port = server.server_address[1]
        threading.Thread(target=server.serve_forever, daemon=True).start()
        with sync_playwright() as p:
            browser = p.chromium.launch()
            cards = browser.new_page(viewport={"width": V.W, "height": V.H})
            page = browser.new_page(viewport={"width": 1536, "height": 864}, device_scale_factor=1.25, user_agent=V.UA)
            for md in todo:
                folder, secs, n, broken = record_one(cards, page, port, md)
                print(f"{md.stem}: {n} slides, {V.clock(secs)} long  ->  {folder}")
                for b in broken:
                    print(f"  picture didn't load: {b}")
            browser.close()
        server.shutdown()
    print("Each folder has the silent video (.mp4), subtitles (.srt/.vtt), chapters.txt, youtube.txt, transcript.md and record-voice.md.")
    print("Record your voice:  python tools/teach.py voice LECTURE-FOLDER")
    return 0
