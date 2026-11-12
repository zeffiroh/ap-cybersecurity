import asyncio
import base64
import hashlib
import json
import mimetypes
import os
import re
import secrets
import shutil
import struct
import subprocess
import sys
import time
import webbrowser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from builder import lesson as L

HERE = Path(__file__).resolve().parent
UI = HERE / "ui"
XTERM = ROOT / "source" / "static" / "assets" / "vendor" / "xterm"
SITE = ROOT / "site"
WIN = sys.platform == "win32"
MARK = re.compile(rb"\x1b\]7771;([^\x07]*)\x07")
PARTIAL = re.compile(rb"\x1b(\](7(7(7(1(;[^\x07]*)?)?)?)?)?)?$")
ANSI = re.compile(r"\x1b(\[[0-9;?<>=]*[ -/]*[@-~]|\][^\x07\x1b]*(\x07|\x1b\\)|[@-Z\\^_()*+][0-9A-Za-z]?)")
GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
OUTPUT_CAP = 200_000
SCAN_FILES = 3000
SNAP_BYTES = 1_000_000


def to_wsl(path):
    p = Path(path).resolve().as_posix()
    m = re.match(r"^([A-Za-z]):/(.*)$", p)
    return f"/mnt/{m.group(1).lower()}/{m.group(2)}" if m else p


def clean_output(raw):
    interactive = "\x1b[?1049h" in raw
    lines = []
    for line in ANSI.sub("", raw).replace("\r\n", "\n").split("\n"):
        line = line.rstrip("\r").rsplit("\r", 1)[-1]
        while re.search(r"[^\x08]\x08", line):
            line = re.sub(r"[^\x08]\x08", "", line, count=1)
        lines.append(line.replace("\x08", ""))
    return "\n".join(lines).strip("\n"), interactive


def default_shell():
    if not WIN:
        return "bash"
    try:
        out = subprocess.run(["wsl.exe", "-l", "-q"], capture_output=True, timeout=10).stdout.decode("utf-16-le", "ignore")
    except (OSError, subprocess.SubprocessError):
        sys.exit("Recording needs bash. Install WSL with: wsl --install")
    names = [n.strip() for n in out.splitlines() if n.strip() and not n.strip().startswith("docker-")]
    if not names:
        sys.exit("Recording needs a Linux under WSL. Install one with: wsl --install -d Ubuntu")
    for want in ("kali-linux", "Ubuntu"):
        if want in names:
            return "wsl:" + want
    return "wsl:" + names[0]


FILE_LIMIT = 5_000_000
FILES_LIMIT = 30_000_000


class Session:
    def __init__(self, name, title, shell):
        self.name = name
        self.dir = L.session_dir(name)
        self.work = self.dir / "case"
        self.work.mkdir(parents=True, exist_ok=True)
        (self.dir / "snapshots").mkdir(exist_ok=True)
        self.info_path = self.dir / "session.json"
        self.info = json.loads(self.info_path.read_text(encoding="utf-8")) if self.info_path.exists() else {"name": name, "title": title or name, "elapsed": 0.0, "seq": 0, "takes": 0}
        self.info["title"] = title or self.info["title"]
        self.info["shell"] = shell
        self.info["takes"] += 1
        self.t0 = time.monotonic() - float(self.info.get("elapsed", 0.0))
        self.paused = False
        self.seq = int(self.info.get("seq", 0))
        self.events = open(self.dir / "events.jsonl", "a", encoding="utf-8", newline="\n")
        cast = self.dir / "terminal.cast"
        fresh = not cast.exists()
        self.cast = open(cast, "a", encoding="utf-8", newline="\n")
        if fresh:
            self.cast.write(json.dumps({"version": 2, "width": 120, "height": 34, "title": self.info["title"]}) + "\n")
        self.listing = self.scan()
        base = self.dir / "baseline.json"
        if not base.exists():
            base.write_text(json.dumps(sorted(self.listing)), encoding="utf-8")
        self.save_info()

    def now(self):
        return round(time.monotonic() - self.t0, 3)

    def save_info(self):
        self.info.update(elapsed=self.now(), seq=self.seq)
        tmp = self.info_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.info, indent=1), encoding="utf-8")
        os.replace(tmp, self.info_path)

    def log(self, kind, **data):
        event = dict(k=kind, t=self.now(), **data)
        self.events.write(json.dumps(event, ensure_ascii=False) + "\n")
        self.events.flush()
        self.save_info()
        return event

    def scan(self):
        out, count = {}, 0
        for base, dirs, files in os.walk(self.work):
            dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "node_modules", ".venv")]
            for f in files:
                count += 1
                if count > SCAN_FILES:
                    return out
                p = Path(base) / f
                try:
                    st = p.stat()
                except OSError:
                    continue
                out[p.relative_to(self.work).as_posix()] = [st.st_size, st.st_mtime_ns]
        return out

    def delta(self, seq):
        now = self.scan()
        changed = sorted(k for k, v in now.items() if self.listing.get(k) != v)
        removed = sorted(k for k in self.listing if k not in now)
        self.listing = now
        kept = []
        for rel in changed:
            src = self.work / rel
            if src.stat().st_size > SNAP_BYTES:
                continue
            dest = self.dir / "snapshots" / f"{seq:05d}" / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            kept.append(rel)
        return changed, kept, removed


class Video:
    def __init__(self, session):
        self.session = session
        self.proc = None
        self.file = None

    def folder(self):
        return Path.home() / "Videos" / "Aayat-Studio" / self.session.name

    def mics(self):
        ff = shutil.which("ffmpeg")
        if not ff:
            return []
        if WIN:
            out = subprocess.run([ff, "-hide_banner", "-list_devices", "true", "-f", "dshow", "-i", "dummy"], capture_output=True, text=True, errors="ignore").stderr
            return re.findall(r'"([^"]+)" \(audio\)', out)
        return ["default"] if shutil.which("pactl") else []

    def command(self, target, mic):
        args = [shutil.which("ffmpeg"), "-hide_banner", "-loglevel", "error", "-y"]
        if WIN:
            args += ["-f", "gdigrab", "-framerate", "30", "-draw_mouse", "1", "-i", "desktop"]
            if mic:
                args += ["-f", "dshow", "-i", f"audio={mic}"]
        else:
            if not os.environ.get("DISPLAY"):
                raise RuntimeError("Screen recording needs an X11 session (DISPLAY is not set). Record with OBS and press Mark video start.")
            args += ["-f", "x11grab", "-framerate", "30", "-i", os.environ["DISPLAY"]]
            if mic:
                args += ["-f", "pulse", "-i", mic]
        args += ["-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2", "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23", "-pix_fmt", "yuv420p",
                 "-threads", "2", "-movflags", "+frag_keyframe+empty_moov"]
        if mic:
            args += ["-c:a", "aac", "-b:a", "128k"]
        return args + [str(target)]

    def start(self, mic):
        if self.proc:
            return self.file
        if not shutil.which("ffmpeg"):
            raise RuntimeError("ffmpeg isn't installed. Install it, or record with OBS and press Mark video start.")
        folder = self.folder()
        folder.mkdir(parents=True, exist_ok=True)
        n = 1 + len(list(folder.glob("take-*.mp4")))
        self.file = folder / f"take-{n:02d}.mp4"
        self.proc = subprocess.Popen(self.command(self.file, mic), stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.session.log("video_start", take=n)
        return self.file

    def stop(self):
        if not self.proc:
            return None
        proc, self.proc = self.proc, None
        try:
            proc.stdin.write(b"q")
            proc.stdin.flush()
            proc.wait(timeout=20)
        except (OSError, subprocess.TimeoutExpired):
            proc.kill()
        self.session.log("video_stop")
        return self.file


class Terminal:
    def __init__(self, app):
        self.app = app
        self.proc = None
        self.tail = b""
        self.current = None
        self.last_hist = None
        self.ready = False

    async def start(self):
        s = self.app.session
        shell = s.info["shell"]
        rc = s.dir / "shell.rc"
        rc.write_bytes((HERE / "shell.rc").read_bytes().replace(b"\r\n", b"\n"))
        host = HERE / "ptyhost.py"
        if shell.startswith("wsl:"):
            argv = ["wsl.exe", "-d", shell[4:], "--", "python3", to_wsl(host), to_wsl(rc), to_wsl(s.work)]
        elif shell == "bash":
            argv = [shutil.which("python3") or sys.executable, str(host), str(rc), str(s.work)]
        else:
            sys.exit("Choose --shell bash or --shell wsl:NAME. Recording commands needs bash.")
        self.proc = await asyncio.create_subprocess_exec(*argv, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        asyncio.create_task(self.pump())
        asyncio.create_task(self.errors())

    async def errors(self):
        while True:
            line = await self.proc.stderr.readline()
            if not line:
                return
            self.app.toast(line.decode("utf-8", "replace").strip())

    async def pump(self):
        read = self.proc.stdout.readexactly
        try:
            while True:
                head = await read(5)
                self.feed(await read(struct.unpack(">I", head[1:5])[0]))
        except (asyncio.IncompleteReadError, ConnectionError):
            self.app.toast("The shell has closed. Your recording is saved. Press Finish, or restart the studio to carry on.")

    def send(self, kind, body):
        if self.proc and self.proc.stdin and not self.proc.stdin.is_closing():
            self.proc.stdin.write(kind + struct.pack(">I", len(body)) + body)

    def resize(self, rows, cols):
        self.send(b"R", struct.pack(">HH", rows, cols))

    def feed(self, data):
        data = self.tail + data
        self.tail = b""
        m = PARTIAL.search(data)
        if m:
            self.tail = data[m.start():]
            data = data[:m.start()]
        pos = 0
        for m in MARK.finditer(data):
            self.output(data[pos:m.start()])
            self.mark(m.group(1).decode("ascii", "replace"))
            pos = m.end()
        self.output(data[pos:])

    def output(self, chunk):
        if not chunk:
            return
        self.app.broadcast_bytes(chunk)
        s = self.app.session
        if s.paused:
            return
        text = chunk.decode("utf-8", "replace")
        s.cast.write(json.dumps([s.now(), "o", text], ensure_ascii=False) + "\n")
        self.app.cast_dirty = True
        if self.current is not None and self.current["size"] < OUTPUT_CAP:
            self.current["out"].append(text)
            self.current["size"] += len(text)

    def mark(self, body):
        parts = body.split(";")
        s = self.app.session
        if parts[0] == "S":
            self.current = {"t": s.now(), "out": [], "size": 0, "paused": s.paused}
            self.app.state(prompt=False)
        elif parts[0] == "P":
            first, self.ready = not self.ready, True
            current, self.current = self.current, None
            self.app.state(prompt=True)
            hist = parts[3] if len(parts) > 3 else ""
            repeat = hist == self.last_hist
            self.last_hist = hist
            if first or not current or repeat or current["paused"] or s.paused:
                return
            cmd = base64.b64decode(parts[4]).decode("utf-8", "replace") if len(parts) > 4 else ""
            cwd = base64.b64decode(parts[2]).decode("utf-8", "replace")
            output, interactive = clean_output("".join(current["out"]))
            asyncio.create_task(self.finish_command(current["t"], cmd, cwd, int(parts[1] or 0), output, interactive))

    async def finish_command(self, started, cmd, cwd, code, output, interactive):
        s = self.app.session
        s.seq += 1
        seq, ended = s.seq, s.now()
        changed, kept, removed = await asyncio.get_running_loop().run_in_executor(None, s.delta, seq)
        event = s.log("cmd", seq=seq, cmd=cmd, cwd=cwd, code=code, out=output, start=started, end=ended, interactive=interactive,
                      changed=changed, files=kept, removed=removed)
        self.app.send_json({"k": "event", "event": {k: event[k] for k in ("k", "t", "seq", "cmd", "code", "changed")}})
        warning = L.scope_warning(cmd)
        if warning:
            self.app.toast(warning)


class App:
    def __init__(self, session, plan, port):
        self.session, self.plan, self.port = session, plan, port
        self.token = secrets.token_urlsafe(24)
        self.clients = set()
        self.terminal = Terminal(self)
        self.video = Video(session)
        self.scroll = bytearray()
        self.cast_dirty = False
        self.prompt = False
        self.plan_pos = 0
        self.mics = None

    def snapshot(self):
        v, s = self.video, self.session
        return {"k": "state", "name": s.name, "title": s.info["title"], "t": s.now(), "paused": s.paused, "prompt": self.prompt, "video": bool(v.proc),
                "videoFile": str(v.file) if v.file else "", "plan": self.plan, "planPos": self.plan_pos, "events": L.summary(s.dir),
                "shell": s.info["shell"], "folder": str(s.work), "mics": self.mics or []}

    def state(self, **extra):
        if "prompt" in extra:
            self.prompt = extra["prompt"]
        self.send_json(dict({"k": "live", "paused": self.session.paused, "prompt": self.prompt, "video": bool(self.video.proc), "t": self.session.now()}, **extra))

    def toast(self, text):
        self.send_json({"k": "toast", "text": text})

    def send_json(self, obj):
        frame = encode_frame(1, json.dumps(obj, ensure_ascii=False).encode("utf-8"))
        for w in list(self.clients):
            self.write(w, frame)

    def broadcast_bytes(self, chunk):
        self.scroll.extend(chunk)
        if len(self.scroll) > 2_000_000:
            del self.scroll[:len(self.scroll) - 1_500_000]
        frame = encode_frame(2, bytes(chunk))
        for w in list(self.clients):
            self.write(w, frame)

    def write(self, w, frame):
        if w.is_closing():
            self.clients.discard(w)
        else:
            w.write(frame)

    async def flusher(self):
        while True:
            await asyncio.sleep(0.25)
            if self.cast_dirty:
                self.session.cast.flush()
                self.cast_dirty = False

    async def message(self, msg):
        kind, s = msg.get("k"), self.session
        loop = asyncio.get_running_loop()
        if kind == "in":
            self.terminal.send(b"D", msg["d"].encode("utf-8"))
        elif kind == "size":
            self.terminal.resize(int(msg["r"]), int(msg["c"]))
            s.log("size", r=int(msg["r"]), c=int(msg["c"]))
        elif kind in ("step", "note", "hint"):
            text = str(msg.get("text", "")).strip()
            if text:
                self.send_json({"k": "event", "event": s.log(kind, text=text)})
        elif kind == "ask":
            q, a = str(msg.get("q", "")).strip(), str(msg.get("a", "")).strip()
            if q:
                self.send_json({"k": "event", "event": s.log("ask", q=q, a=a)})
        elif kind == "tool":
            tool, state = str(msg.get("tool", "")), msg.get("state")
            if re.fullmatch(r"[a-z0-9][a-z0-9-]*", tool) and isinstance(state, dict) and len(json.dumps(state)) <= 20000:
                self.send_json({"k": "event", "event": s.log("tool", tool=tool, state=state, text=str(msg.get("text", tool))[:300])})
        elif kind == "undo":
            self.send_json({"k": "event", "event": s.log("undo")})
        elif kind in ("pause", "resume"):
            s.log(kind)
            s.paused = kind == "pause"
            self.state()
        elif kind == "plan":
            self.use_plan(int(msg.get("i", self.plan_pos)))
        elif kind == "grab":
            self.grab(str(msg.get("path", "")))
        elif kind == "video_start":
            try:
                f = await loop.run_in_executor(None, self.video.start, msg.get("mic") or "")
                self.toast(f"Screen recording to {f}")
            except (RuntimeError, OSError) as e:
                self.toast(str(e))
            self.state()
        elif kind == "video_stop":
            f = await loop.run_in_executor(None, self.video.stop)
            if f:
                self.toast(f"Saved {f}. It stays out of the repo: upload it to YouTube as Unlisted.")
            self.state()
        elif kind == "video_mark":
            s.log("video_start", take=0)
            self.toast("Video start marked. Chapters count from now.")
        elif kind == "finish":
            await self.finish()

    def use_plan(self, i):
        if not 0 <= i < len(self.plan):
            return
        item, s = self.plan[i], self.session
        self.send_json({"k": "event", "event": s.log("step", text=item["title"])})
        if item.get("note"):
            self.send_json({"k": "event", "event": s.log("note", text=item["note"])})
        self.plan_pos = i + 1
        self.state(planPos=self.plan_pos)

    def case_files(self):
        out, total = {}, 0
        for p in sorted(x for x in self.session.work.rglob("*") if x.is_file()):
            size = p.stat().st_size
            if size > FILE_LIMIT or total + size > FILES_LIMIT:
                continue
            try:
                blob = p.read_bytes()
                if p.suffix.lower() in (".pcap", ".pcapng", ".cap") and not blob.startswith(b"#aayat-capture"):
                    text = L.capture_text(blob, p.name)
                    if not text:
                        continue
                    out[p.relative_to(self.session.work).as_posix()] = text
                else:
                    out[p.relative_to(self.session.work).as_posix()] = blob.decode("utf-8")
            except (UnicodeDecodeError, OSError, ValueError, IndexError, struct.error):
                continue
            total += size
        return json.dumps(out, ensure_ascii=False).encode("utf-8")

    def grab(self, path):
        src = Path(path).expanduser()
        if not src.is_file():
            self.toast(f"{path} isn't a file on this computer.")
            return
        dest = self.session.work / src.name
        shutil.copy2(src, dest)
        self.session.listing[src.name] = [dest.stat().st_size, dest.stat().st_mtime_ns]
        self.send_json({"k": "event", "event": self.session.log("file", name=src.name)})

    async def finish(self):
        loop = asyncio.get_running_loop()
        if self.video.proc:
            await loop.run_in_executor(None, self.video.stop)
        self.session.cast.flush()
        self.toast("Building the lesson…")
        try:
            report = await loop.run_in_executor(None, L.finish, self.session.name)
        except Exception as e:
            self.toast(f"The build failed: {e}. Your recording is safe.")
            return
        self.send_json({"k": "report", "report": report})

    async def handle(self, reader, writer):
        try:
            head = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), 30)
            lines = head.decode("latin-1").split("\r\n")
            method, target, _ = lines[0].split(" ", 2)
        except (asyncio.TimeoutError, asyncio.IncompleteReadError, asyncio.LimitOverrunError, ConnectionError, ValueError):
            writer.close()
            return
        headers = {k.strip().lower(): v.strip() for k, v in (l.split(":", 1) for l in lines[1:] if ":" in l)}
        url = urlsplit(target)
        if headers.get("host") not in {f"127.0.0.1:{self.port}", f"localhost:{self.port}"} or method != "GET":
            await self.reply(writer, 403, b"Forbidden", "text/plain")
            return
        if url.path == "/ws":
            await self.websocket(reader, writer, headers, url)
            return
        path = unquote(url.path)
        if path == "/case-files":
            if parse_qs(url.query).get("t", [""])[0] != self.token:
                await self.reply(writer, 403, b"Forbidden", "text/plain")
                return
            body = await asyncio.get_running_loop().run_in_executor(None, self.case_files)
            await self.reply(writer, 200, body, "application/json")
        elif path == "/":
            if parse_qs(url.query).get("t", [""])[0] != self.token:
                await self.reply(writer, 403, b"Open the link the studio printed in your terminal.", "text/plain")
                return
            await self.send_file(writer, UI / "index.html")
        elif path.startswith("/ui/"):
            await self.send_file(writer, UI / path[4:], UI)
        elif path.startswith("/xterm/"):
            await self.send_file(writer, XTERM / path[7:], XTERM)
        elif path.startswith("/site/"):
            await self.send_file(writer, SITE / path[6:], SITE)
        else:
            await self.reply(writer, 404, b"Not found", "text/plain")

    async def send_file(self, writer, path, base=None):
        path = path.resolve()
        if base is not None and base.resolve() not in path.parents:
            await self.reply(writer, 403, b"Forbidden", "text/plain")
            return
        if path.is_dir():
            path = path / "index.html"
        if not path.is_file():
            await self.reply(writer, 404, b"Not found", "text/plain")
            return
        kind = "application/wasm" if path.suffix == ".wasm" else mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        await self.reply(writer, 200, await asyncio.get_running_loop().run_in_executor(None, path.read_bytes), kind)

    async def reply(self, writer, code, body, kind):
        text = {200: "OK", 403: "Forbidden", 404: "Not Found"}[code]
        writer.write(f"HTTP/1.1 {code} {text}\r\nContent-Type: {kind}\r\nContent-Length: {len(body)}\r\nCache-Control: no-store\r\nX-Content-Type-Options: nosniff\r\nConnection: close\r\n\r\n".encode() + body)
        try:
            await writer.drain()
        except ConnectionError:
            pass
        writer.close()

    async def websocket(self, reader, writer, headers, url):
        good = {f"http://127.0.0.1:{self.port}", f"http://localhost:{self.port}"}
        if headers.get("origin") not in good or parse_qs(url.query).get("t", [""])[0] != self.token or "sec-websocket-key" not in headers:
            await self.reply(writer, 403, b"Forbidden", "text/plain")
            return
        if self.mics is None:
            self.mics = await asyncio.get_running_loop().run_in_executor(None, self.video.mics)
        accept = base64.b64encode(hashlib.sha1((headers["sec-websocket-key"] + GUID).encode()).digest()).decode()
        writer.write(f"HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: {accept}\r\n\r\n".encode())
        writer.write(encode_frame(1, json.dumps(self.snapshot(), ensure_ascii=False).encode("utf-8")))
        if self.scroll:
            writer.write(encode_frame(2, bytes(self.scroll)))
        self.clients.add(writer)
        try:
            while True:
                opcode, body = await read_frame(reader)
                if opcode == 8:
                    break
                if opcode == 9:
                    writer.write(encode_frame(10, body))
                elif opcode == 1:
                    await self.message(json.loads(body))
                await writer.drain()
        except (asyncio.IncompleteReadError, ConnectionError, ValueError):
            pass
        self.clients.discard(writer)
        writer.close()


def encode_frame(opcode, body):
    n = len(body)
    if n < 126:
        return bytes([0x80 | opcode, n]) + body
    if n < 65536:
        return bytes([0x80 | opcode, 126]) + struct.pack(">H", n) + body
    return bytes([0x80 | opcode, 127]) + struct.pack(">Q", n) + body


async def read_frame(reader):
    payload, opcode = bytearray(), 0
    while True:
        a, b = await reader.readexactly(2)
        final, op, masked, n = a & 0x80, a & 0x0F, b & 0x80, b & 0x7F
        if n == 126:
            n = struct.unpack(">H", await reader.readexactly(2))[0]
        elif n == 127:
            n = struct.unpack(">Q", await reader.readexactly(8))[0]
        if n > 8_000_000:
            raise ValueError("frame too large")
        mask = await reader.readexactly(4) if masked else b""
        body = await reader.readexactly(n)
        if masked:
            body = bytes(c ^ mask[i & 3] for i, c in enumerate(body))
        if op >= 8:
            return op, body
        opcode = op or opcode
        payload += body
        if final:
            return opcode, bytes(payload)


async def serve(app, open_page):
    server = await asyncio.start_server(app.handle, "127.0.0.1", app.port, limit=1 << 20)
    await app.terminal.start()
    asyncio.create_task(app.flusher())
    link = f"http://127.0.0.1:{app.port}/?t={app.token}"
    print(f"Studio is running for {app.session.name}.\n  Open: {link}\n  Files: {app.session.work}\n  Press Ctrl+C here to stop. Your recording saves as you go.", flush=True)
    if open_page:
        webbrowser.open(link)
    stop = asyncio.Event()
    if os.environ.get("AAYAT_DESK"):
        asyncio.get_running_loop().run_in_executor(None, sys.stdin.buffer.read).add_done_callback(lambda _: stop.set())
    async with server:
        await (stop.wait() if os.environ.get("AAYAT_DESK") else server.serve_forever())


def run(name, title="", source="", shell="auto", port=8765, open_page=True):
    plan = L.prepare(name, title, source)
    session = Session(name, title, default_shell() if shell == "auto" else shell)
    app = App(session, plan, port)
    try:
        asyncio.run(serve(app, open_page))
    except KeyboardInterrupt:
        pass
    finally:
        app.video.stop()
        session.save_info()
        session.cast.close()
        session.events.close()
        print(f"Saved. Carry on with: ./teach studio {name}   Or build it with: ./teach finish {name}")
