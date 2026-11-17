import http.server
import json
import mimetypes
import re
import socketserver
import threading
import webbrowser
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from . import video as V

PLACES = [V.ROOT / ".cache" / "lectures", V.ROOT / ".cache" / "demos"]
PAGE = Path(__file__).resolve().parent / "ui" / "voice.html"


def find(name):
    for base in PLACES:
        if (base / name / "info.json").exists():
            return base / name
    have = [p.parent.name for base in PLACES if base.is_dir() for p in sorted(base.glob("*/info.json"))]
    raise SystemExit(f"No silent video called {name}. Make it first with: teach lecture N, or teach demo NAME.\n"
                     f"Ready to voice: {', '.join(have) or 'none yet'}")


def segments(folder):
    d = folder / "voice"
    return sorted(d.glob("seg-*.webm")) if d.is_dir() else []


def mix(folder):
    info = json.loads((folder / "info.json").read_text(encoding="utf-8"))
    src = folder / info["video"]
    total = V.media_seconds(src) or info.get("seconds", 0)
    segs = segments(folder)
    if not segs:
        raise SystemExit("Nothing recorded yet.")
    starts = [int(re.search(r"seg-(\d+)", p.name).group(1)) / 1000 for p in segs]
    args = ["-i", str(src)]
    parts = []
    for i, (p, at) in enumerate(zip(segs, starts)):
        until = starts[i + 1] if i + 1 < len(starts) else total
        args += ["-i", str(p)]
        parts.append(f"[{i + 1}:a]aresample=48000,atrim=0:{max(0.1, until - at):.3f},asetpts=PTS-STARTPTS,adelay={int(at * 1000)}:all=1[a{i}]")
    chain = ";".join(parts) + ";" + "".join(f"[a{i}]" for i in range(len(segs))) + \
        f"amix=inputs={len(segs)}:normalize=0:dropout_transition=0,highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11,apad,atrim=0:{total:.3f}[out]"
    out = folder / (Path(info["video"]).stem + "-voiced.mp4")
    V.run_ffmpeg(args + ["-filter_complex", chain, "-map", "0:v", "-map", "[out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "48000",
                         "-movflags", "+faststart", "-shortest", str(out)])
    return out


def serve(folder, port, open_browser=True):
    info = json.loads((folder / "info.json").read_text(encoding="utf-8"))
    vtt = next(folder.glob("*.vtt"), None)
    chapters = []
    chap = folder / "chapters.txt"
    if chap.exists():
        for line in chap.read_text(encoding="utf-8").splitlines():
            m = re.match(r"(?:(\d+):)?(\d+):(\d{2})\s+(.*)", line.strip())
            if m:
                chapters.append({"t": int(m.group(1) or 0) * 3600 + int(m.group(2)) * 60 + int(m.group(3)), "name": m.group(4)})
    state = {"done": None}

    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def send(self, code, body, kind="application/json"):
            data = body if isinstance(body, bytes) else (json.dumps(body) if not isinstance(body, str) else body).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)

        def file(self, path):
            size = path.stat().st_size
            kind = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
            rng = re.match(r"bytes=(\d*)-(\d*)", self.headers.get("Range") or "")
            start, end = 0, size - 1
            if rng:
                start = int(rng.group(1) or 0)
                end = int(rng.group(2)) if rng.group(2) else size - 1
                end = min(end, size - 1)
            length = end - start + 1
            self.send_response(206 if rng else 200)
            self.send_header("Content-Type", kind)
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Length", str(length))
            if rng:
                self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            self.end_headers()
            with path.open("rb") as f:
                f.seek(start)
                left = length
                while left > 0:
                    chunk = f.read(min(1 << 20, left))
                    if not chunk:
                        break
                    try:
                        self.wfile.write(chunk)
                    except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                        return
                    left -= len(chunk)

        def do_GET(self):
            u = urlparse(self.path)
            if u.path == "/":
                return self.send(200, PAGE.read_text(encoding="utf-8"), "text/html; charset=utf-8")
            if u.path == "/info":
                return self.send(200, {"title": info.get("title"), "name": folder.name, "video": "/media/" + info["video"],
                                       "vtt": "/media/" + vtt.name if vtt else "", "chapters": chapters,
                                       "segments": [int(re.search(r"seg-(\d+)", p.name).group(1)) for p in segments(folder)],
                                       "done": state["done"]})
            if u.path.startswith("/media/"):
                p = (folder / u.path[7:]).resolve()
                if p.parent == folder.resolve() and p.is_file():
                    return self.file(p)
            if u.path.startswith("/voice/"):
                p = (folder / "voice" / u.path[7:]).resolve()
                if p.parent == (folder / "voice").resolve() and p.is_file():
                    return self.file(p)
            self.send(404, {"error": "not found"})

        def do_POST(self):
            u = urlparse(self.path)
            q = parse_qs(u.query)
            if u.path == "/segment":
                at = max(0, int(float(q.get("at", ["0"])[0]) * 1000))
                body = self.rfile.read(int(self.headers.get("Content-Length") or 0))
                d = folder / "voice"
                d.mkdir(exist_ok=True)
                for p in segments(folder):
                    if int(re.search(r"seg-(\d+)", p.name).group(1)) >= at:
                        p.unlink()
                (d / f"seg-{at:09d}.webm").write_bytes(body)
                return self.send(200, {"ok": True, "segments": [int(re.search(r"seg-(\d+)", p.name).group(1)) for p in segments(folder)]})
            if u.path == "/finish":
                try:
                    out = mix(folder)
                except SystemExit as e:
                    return self.send(400, {"error": str(e)})
                state["done"] = out.name
                print("Saved", out)
                return self.send(200, {"ok": True, "file": str(out), "name": out.name})
            if u.path == "/clear":
                for p in segments(folder):
                    p.unlink()
                return self.send(200, {"ok": True})
            self.send(404, {"error": "not found"})

    class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
        daemon_threads = True
        allow_reuse_address = True

    with Server(("127.0.0.1", port), H) as server:
        url = f"http://127.0.0.1:{port}/"
        print(f"Voice studio for {folder.name}: {url}   Press Ctrl+C here when you are done.")
        if open_browser:
            threading.Timer(0.8, lambda: webbrowser.open(url)).start()
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


def run(name, port=8770, open_browser=True, mix_only=False):
    folder = find(name)
    if mix_only:
        print("Saved", mix(folder))
        return 0
    serve(folder, port, open_browser)
    return 0
