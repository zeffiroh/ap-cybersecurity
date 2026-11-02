import math
import random

from PIL import Image, ImageDraw, ImageFilter

import make_art as A
from make_art import SS, CREAM, OCHRE, SERIF_B, SERIF_I, SANS

NAVY_LIGHT, NAVY_DEEP = (24, 44, 84), (5, 10, 24)
ICE, EMBER = (150, 190, 235), (214, 92, 60)
AUTHOR = "Mitali Aayat Mahnoor Sharma"
SUB = "Beginner's Cybersecurity\nKickstarter · Full Course"
LINE = "Aligned with AP Cybersecurity · simulations · tests · capstone"
FOOT = "Lifetime access · " + AUTHOR


def background(w, h, cx, cy):
    n = 96
    img = Image.new("RGB", (n, n))
    px = img.load()
    for y in range(n):
        for x in range(n):
            t = min(1, math.hypot(x / n - cx / w, (y / n - cy / h) * h / w) * 1.5)
            px[x, y] = tuple(int(NAVY_LIGHT[i] + (NAVY_DEEP[i] - NAVY_LIGHT[i]) * t) for i in range(3))
    return img.resize((w, h), Image.BICUBIC)


def radii(R):
    return [R * f for f in (0.2, 0.36, 0.53, 0.71, 0.9)]


def streams(d, w, h, cx, cy, R, rnd, n):
    rings = radii(R)
    for _ in range(n):
        a0 = rnd.uniform(0, math.tau)
        r0 = rnd.uniform(R * 1.0, max(w, h) * 0.9)
        x, y = cx + math.cos(a0) * r0, cy + math.sin(a0) * r0
        hot = rnd.random() < 0.12
        ink = EMBER if hot else rnd.choice((CREAM, CREAM, ICE, ICE, OCHRE))
        alpha = rnd.randint(22, 75)
        spin = rnd.choice((-1, 1))
        pts = [(x, y)]
        for _ in range(rnd.randint(60, 170)):
            dx, dy = x - cx, y - cy
            r = math.hypot(dx, dy) or 1
            inward = math.atan2(-dy, -dx)
            wall = min(rings, key=lambda q: abs(q - r))
            push = max(0.0, 1 - abs(r - wall) / (R * 0.06)) if r > rings[0] else 1
            a = inward + spin * (0.35 + 1.15 * push) + 0.25 * math.sin(r / (R * 0.11) + a0)
            x += math.cos(a) * 5 * SS
            y += math.sin(a) * 5 * SS
            pts.append((x, y))
            if r < rings[0] * 1.05:
                break
        d.line(pts, fill=ink + (alpha,), width=rnd.choice((1, 1, 2)) * SS, joint="curve")
        if hot:
            ex, ey = pts[-1]
            q = 3 * SS
            d.ellipse((ex - q, ey - q, ex + q, ey + q), fill=EMBER + (200,))


def rings(d, cx, cy, R, rnd):
    nodes = []
    for i, r in enumerate(radii(R)):
        segs = 7 + i * 4
        off = rnd.uniform(0, math.tau)
        for s in range(segs):
            a = off + s * math.tau / segs
            span = math.tau / segs * rnd.uniform(0.55, 0.86)
            col = OCHRE if (s + i) % 5 == 0 else CREAM
            d.arc((cx - r, cy - r, cx + r, cy + r), math.degrees(a), math.degrees(a + span),
                  fill=col + (210 if col == OCHRE else 120,), width=(4 if i % 2 else 2) * SS)
            if rnd.random() < 0.45:
                nodes.append((cx + math.cos(a) * r, cy + math.sin(a) * r, i))
        tick = r + 9 * SS
        for t in range(segs * 3):
            a = off + t * math.tau / (segs * 3)
            d.line((cx + math.cos(a) * (tick - 3 * SS), cy + math.sin(a) * (tick - 3 * SS),
                    cx + math.cos(a) * tick, cy + math.sin(a) * tick), fill=ICE + (60,), width=SS)
    for x, y, i in nodes:
        inner = [n for n in nodes if n[2] == i - 1]
        if inner:
            nx, ny, _ = min(inner, key=lambda n: (n[0] - x) ** 2 + (n[1] - y) ** 2)
            d.line((x, y, nx, ny), fill=ICE + (70,), width=SS)
    for x, y, i in nodes:
        q = (3 + (i % 3)) * SS
        d.ellipse((x - q, y - q, x + q, y + q), fill=NAVY_DEEP + (255,), outline=CREAM + (230,), width=SS)
        if rnd.random() < 0.3:
            d.ellipse((x - q / 2, y - q / 2, x + q / 2, y + q / 2), fill=OCHRE + (255,))


def core(img, cx, cy, R):
    W, H = img.size
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    for f, a in ((0.2, 70), (0.13, 120), (0.07, 200)):
        r = R * f
        g.ellipse((cx - r, cy - r, cx + r, cy + r), fill=OCHRE + (a,))
    glow = glow.filter(ImageFilter.GaussianBlur(R * 0.06))
    img = Image.alpha_composite(img, glow)
    d = ImageDraw.Draw(img, "RGBA")
    r = R * 0.05
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 236, 190, 255))
    r = R * 0.1
    d.regular_polygon((cx, cy, r), 6, rotation=30, outline=CREAM + (230,), width=2 * SS)
    return img


def art(w, h, cx_f, cy_f, R_f, seed, n):
    rnd = random.Random(A.SEED + seed)
    W, H = w * SS, h * SS
    cx, cy, R = W * cx_f, H * cy_f, min(W, H) * R_f
    img = background(W, H, cx, cy).convert("RGBA")
    d = ImageDraw.Draw(img, "RGBA")
    f = A.font(A.MONO, 12 * SS)
    for y in range(0, H, 18 * SS):
        for x in range(0, W, 28 * SS):
            if rnd.random() < 0.5:
                d.text((x, y), f"{rnd.randrange(256):02X}", font=f, fill=ICE + (rnd.choice((5, 8, 11)),))
    streams(d, W, H, cx, cy, R, rnd, n)
    rings(d, cx, cy, R, rnd)
    return core(img, cx, cy, R).convert("RGB")


def shade(img, box, strength):
    W, H = img.size
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rectangle(box, fill=strength)
    mask = mask.filter(ImageFilter.GaussianBlur(min(W, H) * 0.07))
    return Image.composite(Image.new("RGB", (W, H), NAVY_DEEP), img, mask)


def landscape(name, w, h):
    img = art(w, h, 0.8, 0.5, 0.54, 11, int(w * h / 700))
    W, H = img.size
    img = shade(img, (0, 0, int(W * 0.5), H), 215)
    d = ImageDraw.Draw(img, "RGBA")
    s = h / 720
    x, mw = int(W * 0.07), int(W * 0.47)
    y = int(H * 0.17)
    y = A.text_block(d, x, y, mw, s, [("AAYAT-AP-PREP · FULL COURSE · LIFETIME ACCESS", SANS, 18, OCHRE, 14),
                                      (A.TITLE, SERIF_B, 84, CREAM, 10)])
    A.rule(d, x, y, int(120 * s * SS), s)
    y += 26 * s * SS
    A.text_block(d, x, y, mw, s, [(SUB, SERIF_I, 32, CREAM, 18), (LINE, SANS, 18, (200, 215, 235), 34),
                                  (AUTHOR, SERIF_B, 30, CREAM, 0)])
    A.save(img, name, w, h)


def square(name, w):
    img = art(w, w, 0.5, 0.36, 0.42, 12, int(w * w / 750))
    W, H = img.size
    img = shade(img, (0, int(H * 0.6), W, H), 235)
    d = ImageDraw.Draw(img, "RGBA")
    s = w / 600
    x, mw = int(W * 0.08), int(W * 0.84)
    y = int(H * 0.655)
    y = A.text_block(d, x, y, mw, s, [("AAYAT-AP-PREP", SANS, 18, OCHRE, 6), (A.TITLE, SERIF_B, 64, CREAM, 6)],
                     "center")
    A.rule(d, W / 2 - 50 * s * SS, y, int(100 * s * SS), s)
    y += 18 * s * SS
    A.text_block(d, x, y, mw, s, [("Beginner's Kickstarter · Full Course", SERIF_I, 28, CREAM, 8),
                                  (FOOT, SANS, 18, (200, 215, 235), 0)], "center")
    A.save(img, name, w, w)


if __name__ == "__main__":
    landscape("course-cover-1280x720.png", 1280, 720)
    square("course-thumbnail-600x600.png", 600)
    square("course-logo-512x512.png", 512)
