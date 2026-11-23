import base64
import hashlib
import hmac
import json
import re
import sqlite3
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BUNDLE = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else ""
SHOP_SECRET = b"k7Qz-lab-only-long-random-secret-9fX2pL4mN8vB3cR6"

db = sqlite3.connect(":memory:", check_same_thread=False)
db.executescript("""
CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT, password TEXT, role TEXT, name TEXT);
INSERT INTO users VALUES (1, 'admin@nimbu.shop', 'Adm!n-9f3kQ', 'admin', 'Shop admin');
INSERT INTO users VALUES (2, 'kavya.r@example.in', 'kR-2026-x', 'customer', 'Kavya R');
INSERT INTO users VALUES (3, 'demo@nimbu.shop', 'demo123', 'customer', 'Demo customer');
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, items TEXT, total REAL, address TEXT, status TEXT);
INSERT INTO orders VALUES (1, 2, 'basmati rice 5 kg', 649.0, 'Flat 4B, Lake View Apts, Indiranagar, Bengaluru 560038', 'delivered');
INSERT INTO orders VALUES (2, 2, 'ghee 1 L; jaggery 1 kg', 812.0, 'Flat 4B, Lake View Apts, Indiranagar, Bengaluru 560038', 'out for delivery');
INSERT INTO orders VALUES (3, 3, 'tea 500 g', 310.0, 'Demo address, Lab Street, Pune 411001', 'delivered');
INSERT INTO orders VALUES (4, 3, 'masala oats 1 kg', 275.0, 'Demo address, Lab Street, Pune 411001', 'packed');
""")


def b64(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def sign(payload, secret):
    head = b64(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode())
    body = b64(json.dumps(payload, separators=(",", ":")).encode())
    sig = b64(hmac.new(secret, f"{head}.{body}".encode(), hashlib.sha256).digest())
    return f"{head}.{body}.{sig}"


def verify(token, secret):
    try:
        head, body, sig = token.split(".")
        good = b64(hmac.new(secret, f"{head}.{body}".encode(), hashlib.sha256).digest())
        if not hmac.compare_digest(good, sig):
            return None
        return json.loads(base64.urlsafe_b64decode(body + "=="))
    except Exception:
        return None


class Shop(BaseHTTPRequestHandler):
    server_version = "NimbuMart-shop-staging (lab copy)"
    sys_version = ""

    def log_message(self, *a):
        pass

    def send(self, code, obj, ctype="application/json"):
        data = obj if isinstance(obj, bytes) else (json.dumps(obj, indent=1) + "\n").encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/":
            return self.send(200, b"<html><title>NimbuMart (staging)</title><body>NimbuMart staging shop</body></html>\n", "text/html")
        m = re.fullmatch(r"/api/orders/(\d+)", self.path)
        if m:
            user = verify(self.headers.get("Authorization", "").replace("Bearer ", ""), SHOP_SECRET)
            if not user:
                return self.send(401, {"error": "log in first"})
            row = db.execute("SELECT id, customer_id, items, total, address, status FROM orders WHERE id = ?", (int(m.group(1)),)).fetchone()
            if not row:
                return self.send(404, {"error": "no such order"})
            return self.send(200, dict(zip(["id", "customer_id", "items", "total", "address", "status"], row)))
        return self.send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/api/login":
            return self.send(404, {"error": "not found"})
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        query = f"SELECT id, email, role FROM users WHERE email = '{body.get('email', '')}' AND password = '{body.get('password', '')}'"
        try:
            row = db.execute(query).fetchone()
        except sqlite3.Error as e:
            return self.send(500, {"error": "database error", "detail": str(e)})
        if not row:
            return self.send(401, {"error": "wrong email or password"})
        user = {"sub": row[0], "email": row[1], "role": row[2]}
        return self.send(200, {"ok": True, "user": user, "token": sign(user, SHOP_SECRET)})


class Staging(Shop):
    server_version = "NimbuMart-api-staging (lab copy)"

    def do_GET(self):
        if self.path == "/static/app.bundle.js":
            return self.send(200, BUNDLE.encode(), "application/javascript")
        if self.path == "/":
            return self.send(200, {"name": "NimbuMart API (staging, debug)"})
        return self.send(404, {"error": "not found"})

    def do_POST(self):
        return self.send(404, {"error": "not found"})


def serve(handler, host, port):
    ThreadingHTTPServer((host, port), handler).serve_forever()


threading.Thread(target=serve, args=(Shop, "127.0.0.10", 8443), daemon=True).start()
threading.Thread(target=serve, args=(Staging, "127.0.0.11", 8080), daemon=True).start()
threading.Event().wait()
