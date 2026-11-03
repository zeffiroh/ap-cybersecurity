import argparse
import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from .book import PDF as LOCKED_PDF, locked, pdf_password
from .paths import BOOK, ROOT, TEXTBOOK_SRC as TEX

OUT = ROOT / "publication"
BRANDING = ROOT / "branding"
NAME = "Cybersecurity-Textbook-Mitali-Sharma"

TITLE = "Cybersecurity"
SUBTITLE = "A Foundations Textbook for AP Cybersecurity"
AUTHOR = "Mitali Sharma"
EMAIL = "mukumahnoor@gmail.com"
YEAR = "2026"
TRIM_W, TRIM_H, BLEED = 7.0, 9.0, 0.2
SPINE_PER_PAGE = 0.001968
PRINT_GEOMETRY = ("paperwidth=7in, paperheight=9in,\n  inner=0.90in, outer=0.70in,\n"
                  "  top=1.05in,   bottom=1.00in,")

BLURB = ("Units 1–5 of AP Cybersecurity, from social engineering and the CIA triad to network defense, "
         "device hardening, cryptography and secure applications. Every chapter opens with a real incident, "
         "explains how the attack works and how defenders stop it, and closes with review questions and an "
         "answer key. Diagrams, worked examples and short Python and shell listings throughout.")
LONG = f"""From Aayat-AP-Prep: {TITLE}: {SUBTITLE}, by {AUTHOR}.

{BLURB}

Written for students taking College Board's AP Cybersecurity course (one of the AP Career Kickstart
courses) and for teachers running it. The chapters follow the course framework topic by topic:

  Unit 1  Introduction to Security: social engineering, suspicious logins, public Wi-Fi sniffing,
          AI-augmented attacks and AI-powered detection
  Unit 2  Securing Spaces: the CIA triad, physical breaches, access controls and detection systems
  Unit 3  Securing Networks: network exploits, wireless security, segmentation, firewalls, monitoring
  Unit 4  Securing Devices: endpoint vulnerabilities, authentication, hardening, threat auditing
  Unit 5  Securing Applications and Data: code vulnerabilities, Linux permissions, hashing and keys,
          public-key cryptography, secure web design, application auditing

AP is a registered trademark of College Board, which is not affiliated with, and does not endorse, this book. Aayat-AP-Prep is independent."""
KEYWORDS = ["AP Cybersecurity", "cybersecurity textbook", "AP Career Kickstart", "network security for beginners",
            "cryptography basics", "social engineering", "high school computer science"]
BISAC = ["COM053000  COMPUTERS / Security / General", "STU004000  STUDY AIDS / AP Tests",
         "COM043050  COMPUTERS / Networking / Security"]

LICENSE = {
    "digital": ("This digital edition is licensed to the purchaser for personal and classroom use. Please do not "
                "redistribute the file. No part of this edition may be reproduced or transmitted in any form "
                "without the author's written permission, except for brief quotations in reviews and scholarly "
                "work. The online edition of this book is included with the Aayat-AP-Prep course."),
    "print": ("No part of this book may be reproduced, stored or transmitted in any form or by any means without "
              "the author's written permission, except for brief quotations in reviews and scholarly work. The "
              "online edition of this book is included with the Aayat-AP-Prep course."),
}


def compile_edition(kind, dst):
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "textbook"
        shutil.copytree(TEX, src)
        cp = src / "front-matter" / "copyright.tex"
        t = cp.read_text(encoding="utf-8")
        t, n = re.subn(r"This PDF edition is licensed.*?course\.", lambda m: LICENSE[kind], t, flags=re.S)
        if n != 1:
            raise RuntimeError("copyright.tex: licence paragraph not found; update LICENSE in builder/editions.py")
        cp.write_text(t, encoding="utf-8")
        if kind == "print":
            pre = src / "preamble.tex"
            t, n = re.subn(r"paperwidth=.*?bottom=[\d.]+in,", PRINT_GEOMETRY, pre.read_text(encoding="utf-8"),
                           count=1, flags=re.S)
            if n != 1:
                raise RuntimeError("preamble.tex: geometry not found; update PRINT_GEOMETRY in builder/editions.py")
            pre.write_text(t, encoding="utf-8")
        print(f"compiling the {kind} edition (a few minutes)...")
        r = subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
                           cwd=src, capture_output=True, text=True, errors="replace")
        if r.returncode != 0 or not (src / "main.pdf").exists():
            sys.stdout.write(r.stdout[-3000:])
            raise RuntimeError(f"LaTeX build of the {kind} edition failed (log above)")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src / "main.pdf", dst)
    print("made", dst.name)


def page_count(path):
    import fitz
    with fitz.open(path) as doc:
        return doc.page_count


def balanced(s, i, tag="div"):
    depth, pat = 0, re.compile(rf"<(/?){tag}\b[^>]*>")
    for m in pat.finditer(s, i):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return m.end()
    raise ValueError(f"unbalanced <{tag}> at {i}")


def drop(s, start_pat, tag="div"):
    while (m := re.search(start_pat, s)):
        s = s[:m.start()] + s[balanced(s, m.start() + m.group(0).index("<" + tag), tag):]
    return s


def to_mathml(snippets):
    if not snippets:
        return []
    sep = "\n\nMATHSPLIT\n\n"
    md = sep.join((f"$${t}$$" if block else f"${t}$") for t, block in snippets)
    r = subprocess.run(["pandoc", "-f", "markdown", "-t", "html", "--math-method=mathml"], input=md,
                       capture_output=True, text=True, encoding="utf-8", check=True)
    parts = [re.search(r"<math.*</math>", p, re.S) for p in r.stdout.split("<p>MATHSPLIT</p>")]
    if len(parts) != len(snippets) or not all(parts):
        raise RuntimeError("math conversion: pandoc returned a different number of formulas")
    return [p.group(0) for p in parts]


def rasterize(svg, png):
    import fitz
    with fitz.open(svg) as doc:
        doc[0].get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False).save(png)


EPUB_CSS = """body{font-family:serif;line-height:1.45}
h1,h2,h3,h4{font-family:sans-serif;color:#800000;line-height:1.2}
h1{page-break-before:always}
img{max-width:100%;height:auto}
figure{margin:1.2em 0;text-align:center}
figcaption,.code-caption{font-size:.85em;font-style:italic;color:#555}
.box,.review-questions,.answer-key,.ap-alignment{border-left:4px solid #800000;background:#f7f4ef;
  padding:.6em .9em;margin:1em 0}
.box-label{font-family:sans-serif;font-weight:bold;font-size:.8em;text-transform:uppercase;color:#800000}
.box-misconception{border-left-color:#9a9a9a}.box-enrichment{border-left-color:#3a6b52}
pre,code{font-family:monospace;font-size:.85em}
pre{white-space:pre-wrap;background:#f5f3ee;padding:.5em;border:1px solid #ddd;text-align:left}
.code-lang{font-family:sans-serif;font-size:.75em;text-transform:uppercase;color:#666}
.chapter-quote{font-style:italic;margin:1em 2em}
.center{text-align:center}.flushright{text-align:right}
table{border-collapse:collapse;width:100%;font-size:.9em}th,td{border:1px solid #ccc;padding:.3em .5em;
  text-align:left;vertical-align:top}th{background:#f3e6e6}
.answer-code{font-size:.75em;color:#888}
.copyright p{font-size:.85em}
"""


def epub(dst, cover_jpg):
    s = (BOOK / "index.html").read_text(encoding="utf-8")
    i = s.index('<div class="book" id="main-content"')
    s = s[i:s.index('<section class="downloads-section"')]
    s = s[s.index(">") + 1:]
    s = s.replace(' contenteditable="true"', "")
    s = drop(s, r'<div class="titlepage"')
    s = re.sub(r"<h3[^>]*>Check Your Understanding</h3>\s*", "", s)
    s = drop(s, r'<div class="practice-check"')
    s = drop(s, r"<button\b", "button")
    s = s.replace(' loading="lazy"', "")
    s = re.sub(r'<div class="preface"><h2>(.*?)</h2>', r'<h1>\1</h1><div class="preface">', s)
    s = re.sub(r'<header class="\w+-header">(<img[^>]*>)(<h[12][^>]*>.*?</h[12]>)</header>', r"\2\1", s)
    s = re.sub(r"</?section\b[^>]*>", "", s)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "img").mkdir()
        names = {}

        def image(m):
            src = m.group(1)
            if src not in names:
                p = (BOOK / src).resolve()
                stem = re.sub(r"[^\w.-]", "_", p.relative_to(ROOT / "site").with_suffix("").as_posix())
                out = tmp / "img" / (stem + ".png")
                if p.suffix.lower() == ".svg":
                    rasterize(p, out)
                else:
                    out = out.with_suffix(p.suffix.lower())
                    shutil.copyfile(p, out)
                names[src] = "img/" + out.name
            return f'src="{names[src]}"'
        s = re.sub(r'src="([^"]+)"', image, s)

        snippets = []

        def keep_math(t, block):
            snippets.append((html.unescape(t).strip(), block))
            return f"\x00{len(snippets) - 1}\x00"
        s = re.sub(r'<div class="math-block">\\\[(.*?)\\\]</div>', lambda m: "<p>" + keep_math(m.group(1), True) + "</p>",
                   s, flags=re.S)
        parts = re.split(r"(<pre\b.*?</pre>)", s, flags=re.S)
        s = "".join(p if p.startswith("<pre") else
                    re.sub(r"\\\((.*?)\\\)", lambda m: keep_math(m.group(1), False), p, flags=re.S) for p in parts)
        mathml = to_mathml(snippets)
        s = re.sub(r"\x00(\d+)\x00", lambda m: mathml[int(m.group(1))], s)

        notice = (f'<div class="copyright"><h1>Copyright</h1><p><strong>{TITLE}: {SUBTITLE}</strong><br>'
                  f"First edition, {YEAR}</p><p>Copyright &#169; {YEAR} {AUTHOR}. All rights reserved.</p>"
                  f"<p>{html.escape(LICENSE['digital'])}</p>"
                  "<p>AP is a registered trademark of College Board, which is not affiliated with, and does not "
                  "endorse, this book. All other product and company names are trademarks of their respective "
                  "owners and are used only to identify them.</p>"
                  "<p>The attack techniques in this book are described for education and defense. Use them only on "
                  "systems you own or have written permission to test; unauthorized access to computer systems is "
                  "illegal. The information is provided as is, without warranty of any kind, and the author is not "
                  "liable for any damage arising from its use.</p></div>")
        (tmp / "book.html").write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{TITLE}'
                                       f"</title></head><body>{notice}{s}</body></html>", encoding="utf-8")
        (tmp / "epub.css").write_text(EPUB_CSS, encoding="utf-8")
        shutil.copyfile(cover_jpg, tmp / "cover.jpg")
        dst.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["pandoc", "book.html", "-f", "html", "-t", "epub3", "-o", str(dst), "--toc", "--toc-depth=2",
                        "--split-level=2", "--epub-cover-image=cover.jpg", "--css=epub.css",
                        f"--metadata=title:{TITLE}", f"--metadata=subtitle:{SUBTITLE}", f"--metadata=author:{AUTHOR}",
                        "--metadata=lang:en-US", f"--metadata=date:{YEAR}",
                        f"--metadata=rights:Copyright {YEAR} {AUTHOR}. All rights reserved.",
                        "--metadata=subject:Computers / Security / General"],
                       cwd=tmp, check=True, capture_output=True, text=True, encoding="utf-8")
    print("made", dst.name)


def art_module():
    sys.path.insert(0, str(BRANDING))
    import make_art
    return make_art


def front_jpg(dst):
    from PIL import Image
    Image.open(BRANDING / "ebook-cover-1600x2560.png").convert("RGB").save(dst, quality=93, dpi=(300, 300))


def cover_wrap(dst, spine_in, dpi=300):
    from PIL import Image, ImageDraw
    A = art_module()
    ss = A.SS
    px = lambda inches: int(round(inches * dpi))
    w, h = px(2 * TRIM_W + spine_in + 2 * BLEED), px(TRIM_H + 2 * BLEED)
    img = A.art(w, h, 7, int(w * h / 2400), (0.62, 0.56, 0.95, 0.78), 22)
    back_x0, spine_x0 = px(BLEED) * ss, px(BLEED + TRIM_W) * ss
    front_x0, front_w = px(BLEED + TRIM_W + spine_in) * ss, px(TRIM_W) * ss
    top, trim_h = px(BLEED) * ss, px(TRIM_H) * ss
    safe = px(0.375) * ss

    img = A.shade(img, (front_x0, 0, front_x0 + front_w + px(BLEED) * ss, top + int(trim_h * 0.54)), 225)
    img = A.shade(img, (front_x0, top + int(trim_h * 0.85), front_x0 + front_w + px(BLEED) * ss, h * ss), 225)
    img = A.shade(img, (0, 0, spine_x0, h * ss), 215)
    d = ImageDraw.Draw(img, "RGBA")
    s = front_w / ss / 1000
    x, mw = front_x0 + safe, front_w - 2 * safe
    y = top + int(trim_h * 0.1)
    y = A.text_block(d, x, y, mw, s, [("UNITS 1–5", A.SANS, 30, A.OCHRE, 20),
                                      (TITLE, A.SERIF_B, 128, A.CREAM, 18)], "center")
    A.rule(d, x + mw / 2 - 90 * s * ss, y, int(180 * s * ss), s)
    y += 40 * s * ss
    A.text_block(d, x, y, mw, s, [(A.SUB1, A.SERIF_I, 50, A.CREAM, 24), (A.SUB2, A.SANS, 30, (230, 205, 195), 0)],
                 "center")
    A.text_block(d, x, top + int(trim_h * 0.88), mw, s, [(AUTHOR, A.SERIF_B, 56, A.CREAM, 0)], "center")

    bx, bw = back_x0 + safe, spine_x0 - back_x0 - 2 * safe
    y = top + safe + int(trim_h * 0.04)
    y = A.text_block(d, bx, y, bw, s, [("AP CYBERSECURITY · UNITS 1–5", A.SANS, 30, A.OCHRE, 26),
                                       (TITLE, A.SERIF_B, 84, A.CREAM, 10)])
    A.rule(d, bx, y, int(140 * s * ss), s)
    y += 36 * s * ss
    y = A.text_block(d, bx, y, bw, s, [(BLURB, A.SERIF_I, 40, A.CREAM, 34),
                                       ("Read it with the course: lectures, practice, quizzes and a capstone "
                                        "investigation at zeffiroh.github.io/ap-cybersecurity", A.SANS, 30,
                                        (230, 205, 195), 0)])
    A.text_block(d, bx, top + trim_h - safe - int(1.6 * dpi * ss), bw - int(2.3 * dpi * ss), s * 0.8,
                 [("AP is a registered trademark of College Board, which is not affiliated with, and does not "
                   "endorse, this book.", A.SANS, 24, (200, 180, 170), 0)])

    spine_w = int(spine_in * dpi) * ss
    if spine_in >= 0.5:
        strip = Image.new("RGBA", (trim_h, spine_w), (0, 0, 0, 0))
        sd = ImageDraw.Draw(strip)
        f = A.font(A.SERIF_B, spine_w * 0.42)
        fa = A.font(A.SANS, spine_w * 0.3)
        ty = (spine_w - f.size) / 2 - f.size * 0.1
        sd.text((safe, ty), TITLE, font=f, fill=A.CREAM)
        tw = sd.textlength(AUTHOR, font=fa)
        sd.text((trim_h - safe - tw, (spine_w - fa.size) / 2), AUTHOR, font=fa, fill=(230, 205, 195))
        strip = strip.rotate(-90, expand=True)
        img.paste(strip, (spine_x0, top), strip)

    import io
    import fitz
    out = img.resize((w, h), Image.LANCZOS)
    jpg = io.BytesIO()
    out.save(jpg, "JPEG", quality=95, dpi=(dpi, dpi))
    page_w, page_h = (2 * TRIM_W + spine_in + 2 * BLEED) * 72, (TRIM_H + 2 * BLEED) * 72
    dst.parent.mkdir(parents=True, exist_ok=True)
    with fitz.open() as doc:
        doc.new_page(width=page_w, height=page_h).insert_image(fitz.Rect(0, 0, page_w, page_h), stream=jpg.getvalue())
        doc.save(dst, garbage=3, deflate=True)
    out.resize((w // 4, h // 4), Image.LANCZOS).save(dst.with_name(dst.stem + "-preview.jpg"), "JPEG", quality=85)
    print(f"made {dst.name}  ({page_w / 72:.3f} x {page_h / 72:.3f} in, spine {spine_in:.3f} in)")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def readmes(pw, pages, pothi_spine):
    kw = "\n".join("  " + k for k in KEYWORDS)
    bisac = "\n".join("  " + b for b in BISAC)
    write(OUT / "README.txt", f"""
TEXTBOOK STORE COPIES
=====================

Every place the book is sold has a folder here with the exact files to upload and a README.txt with the
steps. This folder is gitignored: it holds the unlocked book and the PDF password, so never commit it or
put it on the course site.

  Folder               Sells                                   Files
  razorpay/            the PDF password (India)                 thank-you text, book logo, course logo
  gumroad/             the PDF + EPUB (everywhere else)          digital PDF, EPUB, thank-you text, cover, thumbnail
  gumroad/course/      the course (everywhere else)             course cover, course thumbnail
  payhip/              the PDF + EPUB, delivered by Payhip      digital PDF, EPUB, cover
  pothi/               paperback + ebook (India)                interior PDF, cover PDF / PDF, EPUB

  store-listing.txt    title, description, keywords and categories to paste into every store

The three editions
  locked PDF    the course site's download, opens with the password ({pw})
  digital       unlocked PDF + EPUB; copyright page says "digital edition ... do not redistribute the file"
  print         unlocked PDF for printing ({pages} pages, {TRIM_W:g} x {TRIM_H:g} in); copyright page without "file"

After paying on Razorpay, buyers of the locked PDF see the password on the thank-you page. Every other store
delivers its own unlocked file, so no password is involved there.

When a store link is live, paste it into source/static/buy/index.html (the LINKS list at the bottom), then
    python build.py --only static ; git add . ; git commit -m "Store links" ; git push

Rebuild this folder after changing the book
    python build.py --only book
    python -m builder.editions                     (add --pothi-spine N if Pothi's cover page says otherwise)
The paperback covers are sized for {pages} pages; if the page count changes, rebuild and upload both again.

Before you publish anywhere
  [ ] Open the EPUB in Calibre (installed) and page through one chapter.
  [ ] Open each interior PDF and check the copyright page wording.
  [ ] Pothi gives a paperback ISBN free; the ebooks don't need one.
""")
    write(OUT / "store-listing.txt", f"""
STORE LISTING (paste into every store)
======================================

Title       {TITLE}
Subtitle    {SUBTITLE}
Author      {AUTHOR}
Edition     First edition, {YEAR}
Language    English
Pages       {pages} (print)
Audience    Grades 10-12 and first-year college; teachers of AP Cybersecurity
Contact     {EMAIL}

SHORT DESCRIPTION (one paragraph)
{BLURB}

LONG DESCRIPTION
{LONG}

KEYWORDS
{kw}

CATEGORIES (BISAC codes, for Pothi's category picker)
{bisac}

The word "AP" belongs to College Board. Keep "for AP Cybersecurity" as the subtitle (not the title) and keep
the trademark line in the description; some stores flag titles that look official.
""")
    write(OUT / "razorpay" / "README.txt", f"""
RAZORPAY - sell the PDF password (India)
========================================

Buyers download the locked PDF from the course site and pay here for the password.

The page is live: https://rzp.io/rzp/ap-cyber-security-mitali  (already on the buy page)
Edit it at https://dashboard.razorpay.com/app/paymentpages

Check once on that page:
  [ ] Customer details ask for Email (required), so you can resend the password.
  [ ] Settings -> "After payment": Custom message = thank-you-message.txt (it contains the password).
      No redirect: the password must stay on Razorpay's page, not on the public course site.
  [ ] Description: the SHORT DESCRIPTION from ../store-listing.txt. Image: razorpay-logo-512x512.png.

The course page (https://rzp.io/rzp/unlock-aap-cybersecurity) uses course-logo-512x512.png.
  [ ] A Rs 1 test shows the password after paying.
""")
    thanks = f"""
Thank you for buying {TITLE}: {SUBTITLE}.

Your PDF password:   {pw}

1. Download the PDF: https://zeffiroh.github.io/ap-cybersecurity/downloads/AP_Cybersecurity_Textbook.pdf
2. Open it and type the password above. Save a copy of this message.

The licence is for you and your classroom; please don't share the file or the password.
Questions or a lost password: {EMAIL}
"""
    write(OUT / "razorpay" / "thank-you-message.txt", thanks)
    write(OUT / "gumroad" / "thank-you-message.txt", f"""
Thank you for buying {TITLE}: {SUBTITLE}.

Download the PDF or the EPUB above (the EPUB reflows to fit phones and e-readers). Both are yours to keep.

The licence is for you and your classroom; please don't share the files.
Questions: {EMAIL}
""")
    write(OUT / "gumroad" / "README.txt", f"""
GUMROAD - unlocked PDF + EPUB (everywhere outside India)
========================================================

1. https://app.gumroad.com/products/new -> E-book. Name: "{TITLE}: {SUBTITLE} (Aayat-AP-Prep)". Price in USD.
2. Description: the LONG DESCRIPTION from ../store-listing.txt.
   Cover: gumroad-cover-1280x720.png. Thumbnail: gumroad-thumbnail-600x600.png.
3. Content tab: upload {NAME}.pdf and {NAME}.epub, and a text block with thank-you-message.txt.
   Buyers get both files on the receipt page and by email.
4. Publish, copy the product link, and paste it as the second "pdf" entry in source/static/buy/index.html.

THE COURSE (folder course/): "Beginner's Cybersecurity Kickstarter: Full Course (Aayat-AP-Prep)", link
ending /l/cybersecurity-kickstarter. db/sync_gumroad.py (every 5 minutes, secret GUMROAD_ACCESS_TOKEN)
puts every Gumroad sale in the ledger and unlocks the course for each course buyer's email.
""")
    write(OUT / "payhip" / "README.txt", f"""
PAYHIP - unlocked PDF + EPUB, delivered by Payhip
=================================================

1. https://payhip.com -> Products -> Add new product -> Digital product.
2. Upload both files: {NAME}.pdf and {NAME}.epub (buyers pick the one their reader likes).
3. Title, description: from ../store-listing.txt. Cover: cover-1600x2560.jpg.
4. Turn on "PDF stamping" (writes the buyer's email in the PDF's margins; discourages sharing).
   Download limit: 5.
5. Publish, copy the link, and paste it into the Payhip entry in source/static/buy/index.html.
""")
    write(OUT / "pothi" / "README.txt", f"""
POTHI.COM - paperback and ebook (India)
=======================================

https://pothi.com -> Publish -> sign up.

PAPERBACK (folder paperback/)
1. Publish a print book. Size: {TRIM_W:g}" x {TRIM_H:g}" (a Pothi standard size). Paperback (perfect binding).
2. Interior: Black & white, {pages} pages, plain white paper. Upload {NAME}-interior.pdf
   ({TRIM_W:g} x {TRIM_H:g} in pages, no bleed, at least 0.6 in clear on every side, as Pothi asks).
3. Cover: upload {NAME}-cover.pdf. It uses Pothi's softcover formula: spine = 0.001968 x {pages} =
   {pothi_spine:.3f} in, 0.2 in bleed on every side. If Pothi's cover page gives a different spine, rebuild:
       python -m builder.editions --pothi-spine <Pothi's number in inches>
4. ISBN: take Pothi's free ISBN (or none). Description, keywords: ../store-listing.txt.
5. Price and approve; order one copy to check.

EBOOK (folder ebook/)
Publish an eBook -> upload {NAME}.pdf (Pothi sells PDF ebooks; also upload the EPUB if offered).
Cover: cover-1600x2560.jpg.

Copy the Pothi book link into the Pothi entry in source/static/buy/index.html.
""")


def main():
    ap = argparse.ArgumentParser(description="Store copies of the textbook in publication/")
    ap.add_argument("--pothi-spine", type=float, help="Pothi spine width in inches (default: from --paper)")
    a = ap.parse_args()

    if not LOCKED_PDF.exists() or not locked(LOCKED_PDF):
        raise SystemExit("site/downloads/AP_Cybersecurity_Textbook.pdf is missing or unlocked: "
                         "run python build.py --only book first")
    pw = pdf_password()
    OUT.mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        digital, printed, cover = tmp / "digital.pdf", tmp / "print.pdf", tmp / "cover.jpg"
        compile_edition("digital", digital)
        compile_edition("print", printed)
        front_jpg(cover)
        epub(tmp / "book.epub", cover)
        pages = page_count(printed)
        pothi_spine = a.pothi_spine or pages * SPINE_PER_PAGE

        def put(src, *rel):
            dst = OUT.joinpath(*rel)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)

        put(BRANDING / "razorpay-logo-512x512.png", "razorpay", "razorpay-logo-512x512.png")
        put(BRANDING / "course-logo-512x512.png", "razorpay", "course-logo-512x512.png")
        for f in ("gumroad-cover-1280x720.png", "gumroad-thumbnail-600x600.png"):
            put(BRANDING / f, "gumroad", f)
        for f in ("course-cover-1280x720.png", "course-thumbnail-600x600.png"):
            put(BRANDING / f, "gumroad", "course", f)
        for d in ("gumroad", "payhip", "pothi/ebook"):
            put(cover, *d.split("/"), "cover-1600x2560.jpg")
            put(tmp / "book.epub", *d.split("/"), f"{NAME}.epub")
            put(digital, *d.split("/"), f"{NAME}.pdf")
        put(printed, "pothi", "paperback", f"{NAME}-interior.pdf")
        cover_wrap(OUT / "pothi" / "paperback" / f"{NAME}-cover.pdf", pothi_spine)
        readmes(pw, pages, pothi_spine)
    print(f"done: {OUT.relative_to(ROOT)}/  ({pages} print pages)")


if __name__ == "__main__":
    main()
