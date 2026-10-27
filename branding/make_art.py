"""Store artwork for the textbook, drawn algorithmically: a flow field of data streams over a faint hex dump,
with a small network of nodes, in the book's print colours. Same seed, same pictures.

    python branding/make_art.py
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(__file__).parent
SEED = 1337
SS = 2

MAROON, MAROON_DARK = (128, 0, 0), (58, 0, 0)
CREAM, NAVY, OCHRE, FOREST = (250, 249, 246), (31, 56, 100), (181, 132, 42), (47, 93, 66)

FONTS = Path("C:/Windows/Fonts")
SERIF_B, SERIF_I, SANS, MONO = "georgiab.ttf", "georgiai.ttf", "arial.ttf", "consola.ttf"

TITLE = "Cybersecurity"
SUB1 = "A Foundations Textbook\nfor AP Cybersecurity"
SUB2 = "Units 1\u20135: Introduction to Security\nthrough Securing Applications and Data"
AUTHOR = "Mitali Sharma"


def font(name, px):
    return ImageFont.truetype(str(FONTS / name), int(px))


def field(x, y, w, h, k):
    """Flow direction at (x, y): a few layered sine waves, so streams curl but never cross chaotically."""
    u, v = x / w, y / h
    return (math.sin(u * 3.1 + k[0]) * math.cos(v * 2.3 + k[1]) * 1.6
            + math.sin((u + v) * 5.7 + k[2]) * 0.5
            + math.cos(u * 9.1 - v * 4.3 + k[3]) * 0.2)


def background(w, h):
    """Diagonal maroon gradient, darker toward the lower right."""
    n = 64
    img = Image.new("RGB", (n, n))
    px = img.load()
    for y in range(n):
        for x in range(n):
            t = x / n * 0.55 + y / n * 0.45
            px[x, y] = tuple(int(MAROON[i] + (MAROON_DARK[i] - MAROON[i]) * t) for i in range(3))
    return img.resize((w, h), Image.BILINEAR)


def hexdump(d, w, h, rnd):
    """Faint columns of hex bytes, like a packet capture behind glass."""
    f = font(MONO, 13 * SS)
    step_x, step_y = 30 * SS, 19 * SS
    for y in range(0, h, step_y):
        for x in range(0, w, step_x):
            if rnd.random() < 0.55:
                d.text((x, y), f"{rnd.randrange(256):02X}", font=f, fill=CREAM + (rnd.choice((6, 9, 13)),))


def streams(d, w, h, rnd, n):
    k = [rnd.uniform(0, 6.28) for _ in range(4)]
    inks = [CREAM] * 6 + [OCHRE] * 2 + [(150, 175, 210)]
    for _ in range(n):
        x, y = rnd.uniform(-0.05 * w, 1.05 * w), rnd.uniform(-0.05 * h, 1.05 * h)
        ink, alpha = rnd.choice(inks), rnd.randint(18, 70)
        width = rnd.choice((1, 1, 1, 2)) * SS
        pts = [(x, y)]
        for _ in range(rnd.randint(30, 110)):
            a = field(x, y, w, h, k)
            x += math.cos(a) * 6 * SS
            y += math.sin(a) * 6 * SS
            pts.append((x, y))
        d.line(pts, fill=ink + (alpha,), width=width, joint="curve")
        if rnd.random() < 0.08:
            px, py = pts[-1]
            r = 3 * SS
            d.ellipse((px - r, py - r, px + r, py + r), fill=ink + (min(255, alpha * 3),))


def network(d, w, h, rnd, n, box):
    """Nodes inside box joined to their two nearest neighbours: a small network map."""
    x0, y0, x1, y1 = box
    nodes = [(rnd.uniform(x0, x1), rnd.uniform(y0, y1)) for _ in range(n)]
    for i, (ax, ay) in enumerate(nodes):
        near = sorted(range(n), key=lambda j: (nodes[j][0] - ax) ** 2 + (nodes[j][1] - ay) ** 2)[1:3]
        for j in near:
            d.line((ax, ay, *nodes[j]), fill=CREAM + (90,), width=SS)
    for x, y in nodes:
        r = rnd.choice((4, 5, 7)) * SS
        d.ellipse((x - r, y - r, x + r, y + r), fill=MAROON_DARK + (255,), outline=CREAM + (220,), width=SS)
        if rnd.random() < 0.3:
            d.ellipse((x - r / 2, y - r / 2, x + r / 2, y + r / 2), fill=OCHRE + (255,))


def shade(img, box, strength=200, horizontal=True):
    """Darken behind the text so it reads on any part of the art."""
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    x0, y0, x1, y1 = box
    md.rectangle(box, fill=strength)
    mask = mask.filter(ImageFilter.GaussianBlur(min(w, h) * 0.06))
    return Image.composite(Image.new("RGB", (w, h), (26, 0, 0)), img, mask)


def wrap(d, text, f, max_w):
    lines = []
    for part in text.split("\n"):
        cur = ""
        for wd in part.split():
            t = (cur + " " + wd).strip()
            if d.textlength(t, font=f) <= max_w:
                cur = t
            else:
                lines.append(cur)
                cur = wd
        lines.append(cur)
    return lines


def text_block(d, x, y, max_w, scale, lines, align="left"):
    """lines: (text, font file, size, colour, gap after). Wraps each to max_w; returns the bottom y."""
    for text, ff, size, col, gap in lines:
        f = font(ff, size * scale * SS)
        for ln in wrap(d, text, f, max_w):
            tw = d.textlength(ln, font=f)
            tx = x + (max_w - tw) / 2 if align == "center" else x
            d.text((tx, y), ln, font=f, fill=col)
            y += f.size * 1.22
        y += gap * scale * SS
    return y


def rule(d, x, y, length, scale):
    d.line((x, y, x + length, y), fill=OCHRE + (255,), width=int(3 * scale * SS))


def art(w, h, seed_offset, streams_n, net_box_frac, nodes):
    rnd = random.Random(SEED + seed_offset)
    W, H = w * SS, h * SS
    img = background(W, H).convert("RGBA")
    d = ImageDraw.Draw(img, "RGBA")
    hexdump(d, W, H, rnd)
    streams(d, W, H, rnd, streams_n)
    fx0, fy0, fx1, fy1 = net_box_frac
    network(d, W, H, rnd, nodes, (fx0 * W, fy0 * H, fx1 * W, fy1 * H))
    return img.convert("RGB")


def save(img, name, w, h):
    img.resize((w, h), Image.LANCZOS).save(OUT / name, optimize=True)
    print("wrote", OUT / name)


def landscape(name, w, h, seed_offset=0, label="TEXTBOOK \u00b7 PDF + ONLINE"):
    """Text on the left, network on the right: Gumroad cover, social/share banner."""
    img = art(w, h, seed_offset, int(w * h / 900), (0.6, 0.15, 0.95, 0.85), 16)
    W, H = img.size
    img = shade(img, (0, 0, int(W * 0.56), H), 225)
    d = ImageDraw.Draw(img, "RGBA")
    s = h / 720
    x, mw = int(W * 0.07), int(W * 0.46)
    y = int(H * 0.2)
    y = text_block(d, x, y, mw, s, [(label, SANS, 18, OCHRE, 14)])
    y = text_block(d, x, y, mw, s, [(TITLE, SERIF_B, 84, CREAM, 10)])
    rule(d, x, y, int(120 * s * SS), s)
    y += 26 * s * SS
    y = text_block(d, x, y, mw, s, [(SUB1, SERIF_I, 30, CREAM, 14), (SUB2, SANS, 19, (230, 205, 195), 34),
                                    (AUTHOR, SERIF_B, 30, CREAM, 0)])
    save(img, name, w, h)


def square(name, w, seed_offset=0):
    """Gumroad thumbnail, Razorpay page logo: title only, so it reads when small."""
    img = art(w, w, seed_offset, int(w * w / 700), (0.12, 0.08, 0.88, 0.5), 12)
    W, H = img.size
    img = shade(img, (0, int(H * 0.55), W, H), 225)
    d = ImageDraw.Draw(img, "RGBA")
    s = w / 600
    x, mw = int(W * 0.08), int(W * 0.84)
    y = int(H * 0.6)
    y = text_block(d, x, y, mw, s, [(TITLE, SERIF_B, 70, CREAM, 8)], "center")
    rule(d, W / 2 - 50 * s * SS, y, int(100 * s * SS), s)
    y += 22 * s * SS
    text_block(d, x, y, mw, s, [("for AP Cybersecurity", SERIF_I, 32, CREAM, 10), (AUTHOR, SANS, 24, (230, 205, 195), 0)],
               "center")
    save(img, name, w, w)


def portrait(name, w, h, seed_offset=0):
    """Ebook cover (1:1.6): Google Play Books, Pothi, Payhip, Kindle."""
    img = art(w, h, seed_offset, int(w * h / 2600), (0.1, 0.6, 0.9, 0.8), 18)
    W, H = img.size
    img = shade(img, (0, 0, W, int(H * 0.54)), 225)
    img = shade(img, (0, int(H * 0.85), W, H), 225)
    d = ImageDraw.Draw(img, "RGBA")
    s = w / 1000
    x, mw = int(W * 0.09), int(W * 0.82)
    y = int(H * 0.1)
    y = text_block(d, x, y, mw, s, [("UNITS 1\u20135", SANS, 30, OCHRE, 20), (TITLE, SERIF_B, 128, CREAM, 18)], "center")
    rule(d, W / 2 - 90 * s * SS, y, int(180 * s * SS), s)
    y += 40 * s * SS
    text_block(d, x, y, mw, s, [(SUB1, SERIF_I, 50, CREAM, 24), (SUB2, SANS, 30, (230, 205, 195), 0)], "center")
    text_block(d, x, int(H * 0.88), mw, s, [(AUTHOR, SERIF_B, 56, CREAM, 0)], "center")
    save(img, name, w, h)


if __name__ == "__main__":
    landscape("gumroad-cover-1280x720.png", 1280, 720)
    square("gumroad-thumbnail-600x600.png", 600, 1)
    square("razorpay-logo-512x512.png", 512, 1)
    landscape("share-banner-1200x630.png", 1200, 630, 2)
    portrait("ebook-cover-1600x2560.png", 1600, 2560, 3)
