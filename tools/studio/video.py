import html
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"
LIVE = "https://zeffiroh.github.io/ap-cybersecurity/"
AUTHOR = "Mitali Aayat Mahnoor Sharma"
BRAND = "Aayat-AP-Prep"
COURSE = "Beginner's Cybersecurity Kickstarter - Full Course"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
W, H = 1920, 1080
CARD_SECONDS = 5.0
END_SECONDS = 6.0
WPS = 2.5


def ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        raise SystemExit("ffmpeg is missing. Install it with: winget install Gyan.FFmpeg")


def run_ffmpeg(args):
    r = subprocess.run([ffmpeg(), "-hide_banner", "-loglevel", "error", "-y"] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        raise SystemExit("ffmpeg failed: " + (r.stderr or "").strip()[-800:])


def media_seconds(path):
    r = subprocess.run([ffmpeg(), "-hide_banner", "-i", str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr or "")
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 0.0


def stamp(s, comma=True):
    h, rest = divmod(max(0.0, s), 3600)
    m, sec = divmod(rest, 60)
    ms = min(999, int(round((sec - int(sec)) * 1000)))
    return f"{int(h):02d}:{int(m):02d}:{int(sec):02d}{',' if comma else '.'}{ms:03d}"


def clock(s):
    s = int(s)
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def plain(markup):
    text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", markup or "")
    text = re.sub(r"(?i)<br\s*/?>|</(p|li|h\d|div|tr)>", "\n", text)
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", text)).strip()


def sentences(text, most=26):
    out, cur = [], ""
    for s in re.split(r"(?<=[.!?:])\s+", re.sub(r"\s+", " ", text or "").strip()):
        if not s:
            continue
        if cur and len((cur + " " + s).split()) > most:
            out.append(cur)
            cur = s
        else:
            cur = (cur + " " + s).strip()
    if cur:
        out.append(cur)
    final = []
    for line in out:
        words = line.split()
        while len(words) > most + 8:
            final.append(" ".join(words[:most]))
            words = words[most:]
        final.append(" ".join(words))
    return final


def speak_seconds(text):
    return len((text or "").split()) / WPS


def card_html(kicker, title, sub, lines, end=False):
    rows = "".join(f"<p>{html.escape(x)}</p>" for x in lines)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:{W}px;height:{H}px;background:#0e1116;color:#f4f1ea;font-family:Georgia,'Times New Roman',serif}}
.c{{position:absolute;inset:0;padding:150px 170px;display:flex;flex-direction:column;justify-content:center}}
.k{{font:600 26px/1.2 'Segoe UI',system-ui,sans-serif;letter-spacing:.22em;text-transform:uppercase;color:#7fd4a8;margin-bottom:34px}}
h1{{font-size:{84 if len(title) < 42 else 66}px;line-height:1.08;margin:0 0 30px;font-weight:700;max-width:1500px}}
.s{{font-size:36px;line-height:1.35;color:#c9c4b8;max-width:1400px;margin:0 0 70px}}
.bar{{width:120px;height:6px;background:#b3001b;margin-bottom:46px}}
.f{{font:400 28px/1.5 'Segoe UI',system-ui,sans-serif;color:#d9d5cc}}.f p{{margin:0}}.f p:first-child{{font-weight:600;color:#fff}}
.mk{{position:absolute;right:170px;bottom:110px;font:600 24px 'Segoe UI',system-ui,sans-serif;letter-spacing:.12em;color:#7fd4a8}}
</style></head><body><div class="c"><div class="k">{html.escape(kicker)}</div><h1>{html.escape(title)}</h1>
{f'<p class="s">{html.escape(sub)}</p>' if sub else ''}<div class="bar"></div><div class="f">{rows}</div></div>
<div class="mk">{BRAND.upper()}{' · ' + LIVE.replace('https://', '').rstrip('/') if end else ''}</div></body></html>"""


def make_cards(page, folder, kicker, title, sub):
    start = folder / "card-start.png"
    end = folder / "card-end.png"
    page.set_viewport_size({"width": W, "height": H})
    page.set_content(card_html(kicker, title, sub, [AUTHOR, COURSE, "Aligned with AP Cybersecurity. Not affiliated with the College Board."]))
    page.screenshot(path=str(start))
    page.set_content(card_html("Keep going", "Now try it yourself", "Open the lab, the notebook and the hand-in on the course site.",
                               [AUTHOR, LIVE], end=True))
    page.screenshot(path=str(end))
    return start, end


def write_captions(folder, name, cues, chapters, title, about=""):
    cues = [c for c in cues if c.get("text")]
    srt, vtt = [], ["WEBVTT", ""]
    for i, c in enumerate(cues, 1):
        srt += [str(i), f"{stamp(c['start'])} --> {stamp(c['end'])}", c["text"], ""]
        vtt += [f"{stamp(c['start'], False)} --> {stamp(c['end'], False)}", c["text"], ""]
    (folder / f"{name}.srt").write_text("\n".join(srt), encoding="utf-8")
    (folder / f"{name}.vtt").write_text("\n".join(vtt), encoding="utf-8")
    seen, keep = set(), []
    for t, n in [(0.0, "Opening")] + list(chapters):
        if n and n not in seen:
            seen.add(n)
            keep.append((t, n))
    chap = "\n".join(f"{clock(t)} {n}" for t, n in keep)
    (folder / "chapters.txt").write_text(chap + "\n", encoding="utf-8")
    words, last = [f"# Transcript: {title}", ""], None
    marks = sorted(keep)
    for c in cues:
        head = [n for t, n in marks if t <= c["start"] + 0.01]
        if head and head[-1] != last:
            last = head[-1]
            words += ["", f"## {last}", ""]
        words.append(c["text"])
    (folder / "transcript.md").write_text("\n".join(words).strip() + "\n", encoding="utf-8")
    voice, last = [f"# Read-along script: {title}", "",
                   "Run `python tools/teach.py voice " + name + "` to record with the video playing beside these lines.",
                   "Times are where each line starts in the silent video. You don't need to hit them exactly: the voice studio keeps your voice and the video in step.", ""], None
    for c in cues:
        head = [n for t, n in marks if t <= c["start"] + 0.01]
        if head and head[-1] != last:
            last = head[-1]
            voice += ["", f"## {clock(c['start'])}  {last}", ""]
        voice.append(f"`{clock(c['start'])}`  {c['text']}  ")
    (folder / "record-voice.md").write_text("\n".join(voice).strip() + "\n", encoding="utf-8")
    desc = [title, "", about.strip(), "", f"By {AUTHOR}, {BRAND}.", f"{COURSE}, aligned with AP Cybersecurity (not affiliated with the College Board).",
            "", "Chapters", chap, "", f"Course: {LIVE}"]
    (folder / "youtube.txt").write_text("TITLE\n" + title + "\n\nDESCRIPTION\n" + "\n".join(x for x in desc if x is not None).replace("\n\n\n", "\n\n") +
                                        "\n\nSETTINGS\nVisibility: Unlisted\nMade for kids: No\nSubtitles: upload " + name + ".srt as English\n", encoding="utf-8")


def shift(cues, chapters, by):
    return ([dict(c, start=c["start"] + by, end=c["end"] + by) for c in cues], [(t + by, n) for t, n in chapters])
