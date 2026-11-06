import random
import sys

from PIL import Image, ImageDraw, ImageFilter

import make_art as A
from make_art import SS, CREAM, OCHRE, SERIF_B, SERIF_I, SANS, MONO
from make_course_art import NAVY_DEEP, ICE, EMBER, AUTHOR, background, shade

GREEN = (120, 210, 150)
SOFT = (200, 215, 235)

PRODUCTS = {
    "labs": dict(
        seed=21,
        kicker="AAYAT-AP-PREP · HANDS-ON LABS",
        title="Cybersecurity Labs",
        sub="Real Linux in your browser.\nReal evidence. Real tools.",
        line="Incident runbooks · analyst console · CTF\nSQL injection lab · Hack the shop",
        tag="Real Linux · real evidence · real tools",
        foot="Lifetime access",
        panel="analyst@lab: ~/case",
        cursor=True,
        square_lines=7,
        lines=[
            ("$ ", "nmap -sV 10.0.2.0/24", CREAM),
            ("", "22/tcp  open  ssh     OpenSSH 8.9", ICE),
            ("", "80/tcp  open  http    nginx 1.24", ICE),
            ("$ ", "grep 'Failed password' auth.log | tk-top-ips", CREAM),
            ("", "  412  198.51.100.23", EMBER),
            ("", "    3  192.0.2.14", ICE),
            ("$ ", "sha256sum evidence.tar", CREAM),
            ("", "9f2c…e41a  evidence.tar", ICE),
            ("$ ", "submit FLAG{night-shift}", CREAM),
            ("", "correct  +150 points", GREEN),
        ],
    ),
    "seminars": dict(
        seed=31,
        kicker="AAYAT-AP-PREP · SEMINARS · ONE YEAR",
        title="Cybersecurity Seminars",
        sub="Every recorded seminar,\neach with its own lab.",
        line="SOC detection · incident response · cloud\nGRC · new seminars added through the year",
        tag="Every seminar and its lab, for a year",
        foot="New seminars included",
        panel="Seminar 06 · Log search: SPL and KQL",
        cursor=False,
        square_lines=6,
        lines=[
            ("00:00  ", "The alert that started the night", CREAM),
            ("06:40  ", "index=auth action=failure", ICE),
            ("       ", "| stats count by src_ip", ICE),
            ("14:15  ", "The same search in KQL", CREAM),
            ("21:30  ", "AuthEvents | summarize count() by SrcIp", ICE),
            ("29:05  ", "Lab: hunt the brute force yourself", CREAM),
            ("38:50  ", "Write the handoff note", CREAM),
            ("", "", ICE),
            ("", "lab unlocked  ·  certificate at 90%", GREEN),
        ],
    ),
    "bundle": dict(
        seed=41,
        kicker="AAYAT-AP-PREP · BEST VALUE",
        title="Course + Cybersecurity Labs",
        sub="The full Kickstarter course,\nplus every hands-on lab.",
        line="Lessons · quizzes · tests · capstone · report card\nReal Linux · runbooks · CTF · Hack the shop",
        tag="Everything together, for less",
        foot="Lifetime access",
        panel="my course",
        cursor=True,
        square_lines=6,
        lines=[
            ("[x] ", "Unit 1  Introduction to Security", CREAM),
            ("[x] ", "Unit 2  Securing Spaces", CREAM),
            ("[x] ", "Unit 3  Securing Networks", CREAM),
            ("[x] ", "Unit 4  Securing Devices", CREAM),
            ("[ ] ", "Unit 5  Securing Applications and Data", ICE),
            ("", "", ICE),
            ("$ ", "open lab --case night-shift", CREAM),
            ("", "evidence loaded  ·  6 hosts  ·  3 logs", ICE),
            ("$ ", "submit FLAG{night-shift}", CREAM),
            ("", "correct  +150 points", GREEN),
        ],
    ),
    "tickets": dict(
        seed=51,
        kicker="AAYAT-AP-PREP · CLASSES & SEMINARS",
        title="Cybersecurity Tickets",
        sub="One balance for live classes\nand single seminars.",
        line="Batch class 1 ticket · 1:1 class from 3\nPacks of 5, 10 and 25 cost less",
        tag="Book live classes and single seminars",
        foot="Use them any time",
        panel="my tickets",
        cursor=False,
        square_lines=6,
        lines=[
            ("", "Balance                       10", CREAM),
            ("- ", "Batch class   Thu 18:00        1", ICE),
            ("- ", "1:1 class     Sat 11:00        3", ICE),
            ("- ", "Seminar 08    Phishing triage  5", ICE),
            ("+ ", "Pack of 10                   +10", GREEN),
            ("", "Balance                       11", CREAM),
            ("", "", ICE),
            ("", "Cancel 2 hours before: refunded", OCHRE),
        ],
    ),
}


def network(d, rnd, box, n):
    x0, y0, x1, y1 = box
    nodes = [(rnd.uniform(x0, x1), rnd.uniform(y0, y1)) for _ in range(n)]
    hot = rnd.randrange(n)
    for i, (ax, ay) in enumerate(nodes):
        near = sorted(range(n), key=lambda j: (nodes[j][0] - ax) ** 2 + (nodes[j][1] - ay) ** 2)[1:3]
        for j in near:
            col = EMBER if hot in (i, j) else ICE
            d.line((ax, ay, *nodes[j]), fill=col + (110 if col == EMBER else 70,), width=SS)
    for i, (x, y) in enumerate(nodes):
        r = rnd.choice((4, 5, 7)) * SS
        if i == hot:
            for k, a in ((3.2, 40), (2.2, 80)):
                d.ellipse((x - r * k, y - r * k, x + r * k, y + r * k), outline=EMBER + (a,), width=SS)
            d.ellipse((x - r, y - r, x + r, y + r), fill=EMBER + (255,))
        else:
            d.ellipse((x - r, y - r, x + r, y + r), fill=NAVY_DEEP + (255,), outline=CREAM + (220,), width=SS)
            if rnd.random() < 0.3:
                d.ellipse((x - r / 2, y - r / 2, x + r / 2, y + r / 2), fill=OCHRE + (255,))


def panel(img, box, s, p, lines):
    x0, y0, x1, y1 = [int(v) for v in box]
    W, H = img.size
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).rounded_rectangle((x0, y0, x1, y1), 14 * SS, fill=(0, 0, 0, 170))
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(18 * SS)))
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle((x0, y0, x1, y1), int(12 * s * SS), fill=(6, 12, 26, 236), outline=ICE + (90,), width=SS)
    bar = int(34 * s * SS)
    d.rounded_rectangle((x0, y0, x1, y0 + bar), int(12 * s * SS), fill=(20, 34, 64, 255))
    d.rectangle((x0, y0 + bar // 2, x1, y0 + bar), fill=(20, 34, 64, 255))
    for k, col in enumerate((EMBER, OCHRE, GREEN)):
        cx, cy, r = x0 + (22 + k * 20) * s * SS, y0 + bar / 2, 6 * s * SS
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col + (230,))
    f = A.font(SANS, 15 * s * SS)
    d.text((x0 + (x1 - x0 - d.textlength(p["panel"], font=f)) / 2, y0 + bar / 2), p["panel"], font=f,
           fill=CREAM + (200,), anchor="lm")
    f = A.font(MONO, 17 * s * SS)
    y = y0 + bar + 18 * s * SS
    left = x0 + 22 * s * SS
    for prompt, text, col in lines:
        x = left
        if prompt:
            d.text((x, y), prompt, font=f, fill=OCHRE)
            x += d.textlength(prompt, font=f)
        d.text((x, y), text, font=f, fill=col)
        y += f.size * 1.5
    if p["cursor"]:
        cw = d.textlength("$ ", font=f)
        d.text((left, y), "$", font=f, fill=OCHRE)
        d.rectangle((left + cw, y + 2 * SS, left + cw + 10 * s * SS, y + f.size), fill=CREAM + (220,))
    return img


def base(w, h, cx_f, cy_f, seed, net_box):
    rnd = random.Random(A.SEED + seed)
    W, H = w * SS, h * SS
    img = background(W, H, W * cx_f, H * cy_f).convert("RGBA")
    d = ImageDraw.Draw(img, "RGBA")
    f = A.font(MONO, 12 * SS)
    for y in range(0, H, 18 * SS):
        for x in range(0, W, 28 * SS):
            if rnd.random() < 0.5:
                d.text((x, y), f"{rnd.randrange(256):02X}", font=f, fill=ICE + (rnd.choice((5, 8, 11)),))
    bx = [v * (W if i % 2 == 0 else H) for i, v in enumerate(net_box)]
    network(d, rnd, bx, 22)
    return img


def landscape(p, name, w, h):
    img = base(w, h, 0.75, 0.5, p["seed"], (0.5, 0.06, 0.98, 0.94))
    W, H = img.size
    s = h / 720
    img = panel(img, (W * 0.53, H * 0.2, W * 0.95, H * 0.8), s, p, p["lines"])
    img = shade(img.convert("RGB"), (0, 0, int(W * 0.46), H), 215)
    d = ImageDraw.Draw(img, "RGBA")
    x, mw = int(W * 0.07), int(W * 0.42)
    size = 72 if len(p["title"]) <= 20 else 58
    y = int(H * (0.15 if size == 72 else 0.13))
    y = A.text_block(d, x, y, mw, s, [(p["kicker"], SANS, 18, OCHRE, 14), (p["title"], SERIF_B, size, CREAM, 10)])
    A.rule(d, x, y, int(120 * s * SS), s)
    y += 26 * s * SS
    A.text_block(d, x, y, mw, s, [(p["sub"], SERIF_I, 30, CREAM, 18), (p["line"], SANS, 18, SOFT, 34),
                                  (AUTHOR, SERIF_B, 28, CREAM, 0)])
    A.save(img, name, w, h)


def square(p, name, w):
    img = base(w, w, 0.5, 0.3, p["seed"] + 1, (0.04, 0.04, 0.96, 0.6))
    W, H = img.size
    s = w / 600
    img = panel(img, (W * 0.1, H * 0.06, W * 0.9, H * 0.47), s * 0.8, p, p["lines"][:p["square_lines"]])
    img = shade(img.convert("RGB"), (0, int(H * 0.5), W, H), 250)
    d = ImageDraw.Draw(img, "RGBA")
    x, mw = int(W * 0.08), int(W * 0.84)
    size = 54 if len(p["title"]) <= 20 else 44
    y = int(H * 0.555)
    y = A.text_block(d, x, y, mw, s, [(p["kicker"], SANS, 17, OCHRE, 6), (p["title"], SERIF_B, size, CREAM, 6)], "center")
    A.rule(d, W / 2 - 50 * s * SS, y, int(100 * s * SS), s)
    y += 18 * s * SS
    A.text_block(d, x, y, mw, s, [(p["tag"], SERIF_I, 24, CREAM, 8),
                                  (p["foot"] + " · " + AUTHOR, SANS, 17, SOFT, 0)], "center")
    A.save(img, name, w, w)


if __name__ == "__main__":
    for key in sys.argv[1:] or PRODUCTS:
        landscape(PRODUCTS[key], f"{key}-cover-1280x720.png", 1280, 720)
        square(PRODUCTS[key], f"{key}-thumbnail-600x600.png", 600)
