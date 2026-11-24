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


TARGET = 20 * 60
LONGEST = 25 * 60
SHORTEST = 15 * 60


def plan_slides(slides):
    rows = []
    for s in slides:
        lines = V.sentences(V.plain(s["notes"]))
        talk = sum(max(1.4, V.speak_seconds(x)) for x in lines)
        rows.append({"lines": lines, "dur": max(5.0, talk + 1.5), "unit": s["unit"].strip()})
    return rows


def sections(rows):
    out, last = [], None
    for i, r in enumerate(rows):
        if i == 0 or (r["unit"] and r["unit"] != last):
            out.append([])
        out[-1].append(i)
        last = r["unit"] or last
    return out


def split_parts(rows, whole=False):
    total = sum(r["dur"] for r in rows)
    if whole or total <= LONGEST:
        return [list(range(len(rows)))]
    pieces = []
    for sec in sections(rows):
        dur = sum(rows[i]["dur"] for i in sec)
        if dur <= LONGEST:
            pieces.append(sec)
            continue
        chunks = -(-int(dur) // TARGET)
        each = dur / chunks
        cur, acc = [], 0.0
        for i in sec:
            if cur and acc + rows[i]["dur"] / 2 > each:
                pieces.append(cur)
                cur, acc = [], 0.0
            cur.append(i)
            acc += rows[i]["dur"]
        pieces.append(cur)
    length = lambda idx: sum(rows[i]["dur"] for i in idx)
    goal = total / max(2, round(total / TARGET))
    parts, cur = [], []
    for piece in pieces:
        if cur and (length(cur) + length(piece) > LONGEST or (length(cur) >= SHORTEST and abs(length(cur) + length(piece) - goal) > abs(length(cur) - goal))):
            parts.append(cur)
            cur = []
        cur = cur + piece
    if cur:
        if parts and length(cur) < SHORTEST // 2 and length(parts[-1]) + length(cur) <= LONGEST + 180:
            parts[-1] = parts[-1] + cur
        else:
            parts.append(cur)
    return parts


def part_name(stem, n, of):
    return stem if of == 1 else f"{stem}-p{n}"


def clear_old(stem):
    for old in [OUT / stem, *OUT.glob(f"{stem}-p[0-9]*")]:
        if old.exists():
            shutil.rmtree(old)
    playlist = OUT / f"{stem}-playlist.txt"
    if playlist.exists():
        playlist.unlink()


def record_part(cards, page, folder, name, kicker, title, about, slides, rows, idx, label):
    frames = folder / "frames"
    frames.mkdir(parents=True)
    start_card, end_card = V.make_cards(cards, folder, kicker, title, about)
    t = V.CARD_SECONDS
    cues, chapters, plan, broken = [], [], [(start_card, V.CARD_SECONDS)], []
    last_unit = None
    for k, i in enumerate(idx):
        broken += page.evaluate(SHOW, i)
        shot = frames / f"s{k + 1:03d}.png"
        page.screenshot(path=str(shot))
        r = rows[i]
        if r["unit"] and r["unit"] != last_unit and k > 0:
            chapters.append((t, r["unit"]))
        last_unit = r["unit"] or last_unit
        at = t + 0.6
        for x in r["lines"]:
            d = max(1.4, V.speak_seconds(x))
            cues.append({"start": at, "end": at + d - 0.05, "text": x})
            at += d
        plan.append((shot, r["dur"]))
        t += r["dur"]
    plan.append((end_card, V.END_SECONDS))
    listing = folder / "frames.txt"
    lines = []
    for p, d in plan:
        lines += [f"file '{p.as_posix()}'", f"duration {d:.3f}"]
    lines.append(f"file '{plan[-1][0].as_posix()}'")
    listing.write_text("\n".join(lines) + "\n", encoding="utf-8")
    mp4 = folder / f"{name}.mp4"
    V.run_ffmpeg(["-f", "concat", "-safe", "0", "-i", str(listing), "-vf", f"fps={FPS},format=yuv420p", "-c:v", "libx264",
                  "-preset", "veryfast", "-tune", "stillimage", "-crf", "20", "-g", str(FPS * 10), "-movflags", "+faststart", str(mp4)])
    V.write_captions(folder, name, cues, chapters, label, about)
    shutil.rmtree(frames, ignore_errors=True)
    listing.unlink()
    return t + V.END_SECONDS, sorted(set(broken)), chapters


def record_one(cards, page, port, md, whole=False):
    stem = md.stem
    title, about, kicker = front(md)
    clear_old(stem)
    page.goto(f"http://127.0.0.1:{port}/lectures/{stem}.html")
    page.wait_for_function("typeof SLIDES !== 'undefined' && document.getElementById('panel-slide')", timeout=30000)
    slides = page.evaluate(PREP)
    rows = plan_slides(slides)
    parts = split_parts(rows, whole)
    of = len(parts)
    made, broken_all, outline = [], [], []
    for n, idx in enumerate(parts, 1):
        name = part_name(stem, n, of)
        folder = OUT / name
        folder.mkdir(parents=True)
        k = kicker if of == 1 else f"{kicker} · Part {n} of {of}"
        label = f"{kicker}: {title}" if of == 1 else f"{kicker}, part {n} of {of}: {title}"
        secs, broken, chapters = record_part(cards, page, folder, name, k, title, about, slides, rows, idx, label)
        info = {"kind": "lecture", "name": name, "title": label, "video": f"{name}.mp4", "slides": len(idx), "seconds": round(secs, 1)}
        if of > 1:
            info.update({"lecture": stem, "part": n, "parts": of, "firstSlide": idx[0] + 1, "lastSlide": idx[-1] + 1})
        (folder / "info.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
        made.append((folder, secs, len(idx)))
        broken_all += broken
        outline.append((n, label, secs, [u for u in ([rows[idx[0]]["unit"]] + [c[1] for c in chapters]) if u]))
    if of > 1:
        write_playlist(stem, kicker, title, about, outline)
    return made, sorted(set(broken_all))


def write_playlist(stem, kicker, title, about, outline):
    rows = [f"PLAYLIST TITLE\n{kicker}: {title}", "", f"PLAYLIST DESCRIPTION\n{about.strip()}", "",
            "SETTINGS\nVisibility: Unlisted. Add the parts in this order, then paste each part's video link on the site (Teacher -> Lesson videos),",
            "one post per part, in the same order, on this lecture's lesson. Students see them in the order you post them.", "", "PARTS"]
    for n, label, secs, units in outline:
        rows.append(f"{n}. {label}  ({V.clock(secs)})  folder: {stem}-p{n}")
        rows.append("   covers: " + ", ".join(dict.fromkeys(units)))
    (OUT / f"{stem}-playlist.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")


def run(which="", whole=False):
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
                made, broken = record_one(cards, page, port, md, whole)
                for folder, secs, n in made:
                    print(f"{folder.name}: {n} slides, {V.clock(secs)} long  ->  {folder}")
                for b in broken:
                    print(f"  picture didn't load: {b}")
            browser.close()
        server.shutdown()
    print("A lecture over 25 minutes is split by section into parts of about 15 to 25 minutes (folders NN_name-p1, -p2...), with a NN_name-playlist.txt. Add --whole for one long video.")
    print("Each folder has the silent video (.mp4), subtitles (.srt/.vtt), chapters.txt, youtube.txt, transcript.md and record-voice.md.")
    print("Record your voice:  python tools/teach.py voice LECTURE-FOLDER")
    return 0
