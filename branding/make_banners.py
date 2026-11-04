import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from builder import course as C
from builder.atomtext import parse_atom

FONTS = Path("C:/Windows/Fonts")
W, H, S = 1200, 300, 2
INK, DIM, FAINT, BG = (255, 255, 255), (170, 170, 170), (110, 110, 110), (12, 12, 12)
BRAND = "AAYAT-AP-PREP  \u00b7  BEGINNER'S CYBERSECURITY KICKSTARTER"


def font(name, px):
    return ImageFont.truetype(str(FONTS / name), int(px * S))


def spaced(d, xy, text, f, fill, track):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + track * S
    return x


def wrap(d, text, f, width):
    lines, line = [], ""
    for word in text.split():
        test = (line + " " + word).strip()
        if d.textlength(test, font=f) <= width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def texture(img, seed):
    rnd = random.Random(seed)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = font("consola.ttf", 12)
    for y in range(6 * S, img.size[1], 18 * S):
        for x in range(img.size[0] // 2, img.size[0], 26 * S):
            if rnd.random() < 0.6:
                d.text((x, y), "%02X" % rnd.randrange(256), font=f, fill=(255, 255, 255, rnd.choice((10, 16, 24))))
    fade = Image.linear_gradient("L").rotate(90).resize(img.size)
    layer.putalpha(Image.composite(layer.getchannel("A"), Image.new("L", img.size, 0), fade))
    img.alpha_composite(layer)


def banner(aid, title, unit_n, unit_title, tid, topic_title):
    img = Image.new("RGBA", (W * S, H * S), BG + (255,))
    texture(img, aid)
    d = ImageDraw.Draw(img)
    m = 56
    spaced(d, (m * S, 34 * S), BRAND, font("arialbd.ttf", 12.5), DIM, 2.2)
    d.line([(m * S, 62 * S), ((W - m) * S, 62 * S)], fill=(60, 60, 60), width=S)
    idf = font("consolab.ttf", 54)
    d.text((m * S, 86 * S), aid, font=idf, fill=INK)
    idw = d.textlength(aid, font=idf)
    x0 = m * S + idw + 34 * S
    d.line([(x0 - 17 * S, 92 * S), (x0 - 17 * S, 222 * S)], fill=INK, width=2 * S)
    width = W * S - x0 - m * S
    for size in (40, 36, 32, 28, 25):
        tf = font("georgiab.ttf", size)
        lines = wrap(d, title, tf, width)
        if len(lines) <= 3 and len(lines) * size * 1.22 <= 132:
            break
    lh = size * 1.22 * S
    top = 92 * S + (132 * S - lh * len(lines)) / 2
    for i, line in enumerate(lines):
        d.text((x0, top + i * lh), line, font=tf, fill=INK)
    meta = "Unit %s  \u00b7  %s    %s  %s" % (unit_n, unit_title, tid, topic_title)
    spaced(d, (m * S, 248 * S), meta, font("georgiai.ttf", 16), DIM, 0.2)
    tag = "aligned with AP Cybersecurity"
    tf2 = font("arial.ttf", 11.5)
    d.text(((W - m) * S - d.textlength(tag, font=tf2), 252 * S), tag, font=tf2, fill=FAINT)
    return img.convert("RGB").resize((W, H), Image.LANCZOS)


def main():
    n = 0
    for a in C.atom_order():
        out = a["src"] / "banner.png"
        if not out.exists() and "--all" not in sys.argv:
            continue
        p = parse_atom(a["src"])
        tid = C.tid_of(a["id"])
        t = C.topic(tid)
        u = C.unit(t["unit"])
        banner(a["id"], p["title"], t["unit"], u["title"], tid, t["title"]).save(out, optimize=True)
        n += 1
    print("wrote %d banners" % n)


if __name__ == "__main__":
    main()
