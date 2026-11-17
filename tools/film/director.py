import json
import math
import os
import random
import re
import shlex
import subprocess
import sys
import time

ENV = dict(os.environ, DISPLAY=":1")
WPS = 2.5
rnd = random.Random(7)
log = []
t0 = None
chapter = None


def sh(*args, check=False):
    r = subprocess.run(list(args), env=ENV, capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit(f"{args[0]} failed: {r.stderr.strip()[:300]}")
    return r.stdout.strip()


def now():
    return time.time() - t0


def pointer():
    out = sh("xdotool", "getmouselocation", "--shell")
    vals = dict(l.split("=", 1) for l in out.splitlines() if "=" in l)
    return int(vals.get("X", 960)), int(vals.get("Y", 540))


def glide(x, y, secs=0.6):
    x0, y0 = pointer()
    steps = max(8, int(secs * 60))
    for i in range(1, steps + 1):
        f = 0.5 - 0.5 * math.cos(math.pi * i / steps)
        sh("xdotool", "mousemove", str(int(x0 + (x - x0) * f)), str(int(y0 + (y - y0) * f)))
        time.sleep(secs / steps)


def windows(pattern):
    out = sh("xdotool", "search", "--onlyvisible", "--name", pattern)
    return [w for w in out.split() if w]


def wait_window(pattern, timeout=40):
    end = time.time() + timeout
    while time.time() < end:
        found = windows(pattern)
        if found:
            return found[-1]
        time.sleep(0.3)
    raise SystemExit(f"No window matching {pattern!r} appeared")


def geometry(win):
    out = sh("xdotool", "getwindowgeometry", "--shell", win)
    v = dict(l.split("=", 1) for l in out.splitlines() if "=" in l)
    return int(v["X"]), int(v["Y"]), int(v["WIDTH"]), int(v["HEIGHT"])


def place(win, x, y, w, h):
    sh("xdotool", "windowsize", win, str(w), str(h))
    sh("xdotool", "windowmove", win, str(x), str(y))
    time.sleep(0.3)


def activate(win):
    sh("xdotool", "windowactivate", "--sync", win)
    time.sleep(0.2)


def point_at(win, fx=0.5, fy=0.5, secs=0.7):
    x, y, w, h = geometry(win)
    glide(x + int(w * fx), y + int(h * fy), secs)


def click(button="1"):
    sh("xdotool", "click", button)
    time.sleep(0.25)


def type_text(text, cps=14):
    for ch in text:
        if ch == "\n":
            sh("xdotool", "key", "Return")
        else:
            sh("xdotool", "type", "--delay", "0", ch)
        time.sleep(max(0.01, rnd.gauss(1 / cps, 0.25 / cps)))


def key(*names):
    for k in names:
        sh("xdotool", "key", k)
        time.sleep(0.15)


def cap(text, kind="say"):
    words = len(re.findall(r"\S+", text))
    start = now()
    hold = max(2.0, words / WPS)
    log.append({"start": round(start, 2), "end": round(start + hold, 2), "text": text, "kind": kind})
    return hold


def run(scenes):
    global chapter
    current = {}
    for sc in scenes:
        if "chapter" in sc:
            chapter = sc["chapter"]
            log.append({"start": round(now(), 2), "chapter": chapter})
        if "say" in sc:
            time.sleep(cap(sc["say"]))
        if "open" in sc:
            cmd = sc["open"]
            subprocess.Popen(cmd if isinstance(cmd, list) else shlex.split(cmd), env=ENV, cwd=sc.get("cwd", "/case"),
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            win = wait_window(sc["window"], sc.get("timeout", 40))
            current[sc.get("as", "main")] = win
            g = sc.get("geometry", [80, 60, 1760, 940])
            place(win, *g)
            activate(win)
            time.sleep(sc.get("settle", 1.0))
        if "use" in sc:
            win = current[sc["use"]]
            activate(win)
            point_at(win, *sc.get("at", [0.5, 0.5]))
        if "point" in sc:
            win = current[sc.get("in", "main")]
            point_at(win, *sc["point"], secs=sc.get("secs", 0.8))
            if sc.get("click"):
                click()
        if "keys" in sc:
            key(*sc["keys"])
        if "type" in sc:
            type_text(sc["type"], sc.get("cps", 14))
            if sc.get("enter", True):
                time.sleep(0.25)
                key("Return")
        if "close" in sc:
            win = current.pop(sc["close"], None)
            if win:
                sh("xdotool", "windowclose", win)
        if "wait" in sc:
            time.sleep(sc["wait"])
        if "after" in sc:
            time.sleep(cap(sc["after"], "after"))


def main():
    global t0
    film = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    while not os.path.exists("/tmp/desktop.ready"):
        time.sleep(0.2)
    for pre in film.get("setup", []):
        subprocess.run(pre, shell=True, env=ENV, cwd="/case")
    sh("xdotool", "mousemove", "960", "540")
    rec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "x11grab", "-draw_mouse", "1", "-framerate", "25",
                            "-video_size", "1920x1080", "-i", ":1", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "20",
                            "-pix_fmt", "yuv420p", out + ".mp4"], env=ENV, stdin=subprocess.PIPE)
    time.sleep(1.0)
    t0 = time.time()
    err = ""
    try:
        run(film["scenes"])
        time.sleep(1.5)
    except SystemExit as e:
        err = str(e)
    length = now()
    rec.stdin.write(b"q")
    rec.stdin.flush()
    rec.wait(timeout=60)
    json.dump({"log": log, "length": round(length, 2), "error": err}, open(out + ".json", "w", encoding="utf-8"), indent=1)
    print(json.dumps({"length": round(length, 1), "error": err}))


if __name__ == "__main__":
    main()
