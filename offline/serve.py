#!/usr/bin/env python3
"""
Serve the course (site/) on this computer only and open the home page. No internet needed.

Browsers block fetch() on pages opened by double-click (file://), and the quizzes, assignments,
flashcards and capstone load their data that way. A tiny local server fixes that.

Usage:
    python offline/serve.py              # picks a free port from 8000 up, opens the hub
    python offline/serve.py --port 9000 --no-browser
"""
import argparse
import functools
import http.server
import socket
import socketserver
import webbrowser
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".wasm": "application/wasm",   # Pyodide needs this exact type
        ".js": "text/javascript",
        ".mjs": "text/javascript",
        ".json": "application/json",
        ".ipynb": "application/json",
        ".md": "text/markdown; charset=utf-8",
        ".yaml": "text/plain; charset=utf-8",
        ".apkg": "application/octet-stream",
    }

    def log_message(self, *args):
        pass  # keep the console quiet for students


def free_port(start):
    for port in range(start, start + 50):
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    raise SystemExit("No free port found between %d and %d" % (start, start + 49))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args()

    port = free_port(args.port)
    handler = functools.partial(Handler, directory=str(SITE))
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("127.0.0.1", port), handler) as httpd:
        url = "http://localhost:%d/index.html" % port
        print("Aayat-AP-Prep is running offline at " + url)
        print("Keep this window open while you work. Close it (or press Ctrl+C) to stop.")
        if not args.no_browser:
            webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
