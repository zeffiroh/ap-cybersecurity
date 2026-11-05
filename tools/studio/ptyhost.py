import fcntl
import os
import pty
import select
import signal
import struct
import sys
import termios


def handle(kind, body):
    if kind == b"D":
        os.write(master, body)
    elif kind == b"R":
        rows, cols = struct.unpack(">HH", body)
        fcntl.ioctl(master, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))
        os.kill(pid, signal.SIGWINCH)


def frames(buf):
    while len(buf) >= 5:
        size = struct.unpack(">I", buf[1:5])[0]
        if len(buf) < 5 + size:
            break
        handle(buf[0:1], buf[5:5 + size])
        buf = buf[5 + size:]
    return buf


rc, cwd = sys.argv[1], sys.argv[2]
pid, master = pty.fork()
if pid == 0:
    os.chdir(cwd)
    os.environ["TERM"] = "xterm-256color"
    os.environ["AAYAT_STUDIO"] = "1"
    os.execvp("bash", ["bash", "--rcfile", rc, "-i"])

stdin, stdout = sys.stdin.fileno(), sys.stdout.fileno()
pending = b""
while True:
    try:
        ready, _, _ = select.select([master, stdin], [], [])
    except InterruptedError:
        continue
    if master in ready:
        try:
            data = os.read(master, 65536)
        except OSError:
            data = b""
        if not data:
            break
        packet = b"O" + struct.pack(">I", len(data)) + data
        while packet:
            packet = packet[os.write(stdout, packet):]
    if stdin in ready:
        data = os.read(stdin, 65536)
        if not data:
            os.kill(pid, signal.SIGHUP)
            break
        pending = frames(pending + data)
