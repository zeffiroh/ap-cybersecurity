"""Printable downloads and Anki decks.

topic quiz bank                 -> downloads/unit-N/Topic_<tid>_Quiz.{docx,pdf}
                                   teacher/unit-N/<tid>/Topic_<tid>_Quiz_AnswerKey.{docx,pdf}
practice items + coding problems -> downloads/unit-N/Topic_<tid>_Assignment.{docx,pdf}
                                   teacher/unit-N/<tid>/Topic_<tid>_Assignment_AnswerKey.{docx,pdf}
flashcards.json                 -> downloads/unit-N/Topic_<tid>_Flashcards.apkg

Answer choices print in the order stored in the data, so the printable quizzes use the same balanced A-D
answer positions as the online ones. PDFs are made from the Word files by Microsoft Word (or LibreOffice
if Word is not installed), so the two formats always match.
"""
import hashlib
import io
import json
import re
import shutil
import subprocess
import zipfile
from pathlib import Path

import docx
from docx.shared import Emu, Pt, RGBColor

from . import course as C
from . import util
from .materials import assignment_data, topic_quiz
from .paths import downloads_unit, teacher_topic
from .util import emit_bytes, keep

NO_PDF = False          # set by build.py --no-pdf
FORCE_ANKI = False

ACCENT, DEEP, INK, BODY, MUTED = (RGBColor(0x9C, 0x1C, 0x2C), RGBColor(0x6E, 0x14, 0x1F), RGBColor(0x1A, 0x1A, 0x1A),
                                  RGBColor(0x3A, 0x3A, 0x3A), RGBColor(0x8A, 0x8A, 0x8A))



# ------------------------------------------------------------- docx bits --
def new_doc():
    d = docx.Document()
    s = d.sections[0]
    s.page_width, s.page_height = Emu(7772400), Emu(10058400)                  # US Letter
    s.left_margin = s.right_margin = Emu(731520)
    s.top_margin = s.bottom_margin = Emu(640080)
    d.styles["Normal"].font.name = "Calibri"
    d.styles["Normal"].font.size = Pt(10)
    return d


def para(d, *runs, indent=None, before=None, after=None, keep=False):
    p = d.add_paragraph()
    pf = p.paragraph_format
    if indent is not None:
        pf.left_indent = Emu(indent)
    if before is not None:
        pf.space_before = Emu(before)
    if after is not None:
        pf.space_after = Emu(after)
    pf.keep_with_next = keep
    for text, kw in runs:
        r = p.add_run(text)
        r.font.size = Pt(kw.get("size", 10))
        r.font.color.rgb = kw.get("color", BODY)
        r.bold, r.italic = kw.get("bold"), kw.get("italic")
        if kw.get("mono"):
            r.font.name = "Consolas"
    return p


def R(text, **kw):
    return (text, kw)


INLINE = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`)")


def md_runs(text, size=9.5, color=BODY):
    out = []
    for tok in INLINE.split(text):
        if not tok:
            continue
        if tok.startswith("**"):
            out.append(R(tok[2:-2], size=size, color=color, bold=True))
        elif tok.startswith("`"):
            out.append(R(tok[1:-1], size=size, color=color, mono=True))
        else:
            out.append(R(tok, size=size, color=color))
    return out


def header(d, unit, tid, title, kind):
    para(d, R(f"UNIT {unit} · TOPIC {tid}", size=9, color=ACCENT, bold=True), after=0)
    para(d, R(title, size=18, color=INK, bold=True), after=25400)
    para(d, R(kind, size=11.5, color=BODY), after=127000)


def name_table(d):
    t = d.add_table(rows=1, cols=6)
    for c, label in zip(t.rows[0].cells, ["Name:", "", "Date:", "", "Class:", ""]):
        c.text = label
        for r in c.paragraphs[0].runs:
            r.font.size, r.font.bold = Pt(9.5), True
    para(d, after=50800)


OPT_INDENT = 255905


def choices(d, opts, correct, key, multi=False):
    for k, text in enumerate(opts):
        letter = "ABCDEFGH"[k]
        on = k in correct
        mark = ("■" if on else "□") if multi else ("●" if on else "○")
        if key and on:
            para(d, R(f"{mark} {letter}. ", size=10, color=ACCENT, bold=True), R(text, size=10, color=ACCENT, bold=True),
                 indent=OPT_INDENT, after=25400)
        else:
            mark = ("□" if multi else "○")
            para(d, R(f"{mark} {letter}. ", size=10, bold=False), R(text, size=10), indent=OPT_INDENT, after=25400)


def question(d, n, stem, pts=None):
    runs = [R(f"{n}. {stem}", size=10.5, color=INK, bold=True)]
    if pts is not None:
        runs.append(R(f"  ({pts} pt{'s' if pts != 1 else ''})", size=8, color=MUTED, bold=False))
    para(d, *runs, before=101600, after=38100, keep=True)


def why(d, text, label="Why: "):
    if text:
        para(d, R(label + text, size=9.5), indent=OPT_INDENT, after=50800)


# ----------------------------------------------------------------- quiz --
def quiz_doc(q, key):
    d = new_doc()
    unit = q["topic_id"].split(".")[0]
    n = len(q["questions"])
    header(d, unit, q["topic_id"], q["topic_title"], "Quiz, Answer Key" if key else "Quiz")
    if key:
        para(d, R(f"Teacher answer key, {n} questions, 1 point each. The correct answer is highlighted; the explanation "
                  "and distractor notes follow.", size=9.5, italic=True), after=127000)
    else:
        para(d, R(f"Instructions: This quiz has {n} multiple-choice questions, 1 point each. Circle the letter of the "
                  "single best answer for each question.", size=9.5, italic=True), after=127000)
        name_table(d)
    for i, x in enumerate(q["questions"], 1):
        question(d, i, x["stem"])
        keys = [c["key"] for c in x["choices"]]
        choices(d, [c["text"] for c in x["choices"]], [keys.index(x["answer_key"])], key)
        if key:
            para(d, R(f"Correct answer: {x['answer_key']}", size=9.5, bold=True), indent=OPT_INDENT, after=50800)
            why(d, x.get("explanation"))
            dr = x.get("distractor_rationale") or {}
            if dr:
                runs = [R("Why the others are wrong: ", size=8.5, italic=True)]
                for j, (k, v) in enumerate(sorted(dr.items())):
                    runs += [R(("  " if j else "") + k, size=8.5, italic=True, bold=True), R(f", {v}", size=8.5, italic=True)]
                para(d, *runs, indent=OPT_INDENT, after=50800)
    return d


# ----------------------------------------------------------- assignment --
def atom_dir(aid):
    return C.atom(aid)["src"]


def markdown_block(d, md):
    """The small Markdown subset used by problem/prompt.md."""
    lines = md.replace("\r\n", "\n").split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            para(d, R("\n".join(lines[i + 1:j]), size=8, color=INK, mono=True), after=76200)
            i = j + 1
            continue
        if line.startswith("# "):
            para(d, R(line[2:], size=10.5, color=ACCENT, bold=True), keep=True)
        elif line.startswith("## "):
            para(d, R(line[3:], size=10.5, color=ACCENT, bold=True), keep=True)
        elif line.startswith(("- ", "* ")):
            text = line[2:]
            while i + 1 < len(lines) and lines[i + 1].startswith("  ") and lines[i + 1].strip():
                i += 1
                text += " " + lines[i].strip()
            para(d, *md_runs("• " + text), indent=OPT_INDENT // 2)
        elif line.strip():
            text = line
            while i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].startswith(("#", "-", "* ", "```")):
                i += 1
                text += " " + lines[i].strip()
            para(d, *md_runs(text), after=76200)
        i += 1


def assignment_doc(a, title, key):
    d = new_doc()
    items, coding = a["practice_items"], a["coding_problems"]
    total = sum(x.get("points", 1) for x in items) + sum(c.get("points", 3) for c in coding)
    header(d, a["unit"], a["topic_id"], title, "Assignment, Answer Key" if key else "Assignment")
    if key:
        para(d, R(f"Teacher answer key, {total} points total.", size=9.5, italic=True), after=127000)
    else:
        para(d, R(f"Instructions: {len(items)} practice questions + {len(coding)} coding assignment(s), {total} points total. "
                  "Show your work for short-answer items. Coding assignments may be completed here or in the interactive "
                  "auto-graded environment on the course site (same problem, same points).", size=9.5, italic=True), after=127000)
        name_table(d)
    para(d, R("Practice Questions", size=13, color=DEEP, bold=True), before=177800, after=76200, keep=True)
    last_atom = None
    for i, x in enumerate(items, 1):
        if x["atom_id"] != last_atom:
            para(d, R(f'{x["atom_id"]} · {x["atom_title"]}', size=11, color=INK, bold=True), before=127000, after=50800, keep=True)
            last_atom = x["atom_id"]
        question(d, i, x["prompt"], x.get("points", 1))
        if x["type"] in ("mcq", "multi"):
            ans = x["answer"] if isinstance(x["answer"], list) else [x["answer"]]
            choices(d, x["options"], ans, key, multi=x["type"] == "multi")
            if x["type"] == "multi" and not key:
                para(d, R("(Select ALL that apply.)", size=8.5, italic=True), indent=OPT_INDENT)
        elif key:
            acc = x.get("accept") or []
            para(d, R("Acceptable answers: ", size=9.5, bold=True), R("; ".join(map(str, acc)), size=9.5), indent=OPT_INDENT)
        else:
            for _ in range(2):
                para(d, R("", size=10), indent=OPT_INDENT)
        if key:
            why(d, x.get("explain"))
    if coding:
        para(d, R("Coding Assignments (Python 3)", size=13, color=DEEP, bold=True), before=177800, after=76200, keep=True)
        for c in coding:
            prob = atom_dir(c["atom_id"]) / "problem"
            para(d, R(f'{c["atom_id"]} · {c["title"]}', size=11, color=INK, bold=True), before=127000, after=50800, keep=True)
            para(d, R(f'{c.get("points", 3)} pts · auto-graded on the site', size=8.5, italic=True), indent=OPT_INDENT, after=50800)
            markdown_block(d, (prob / "prompt.md").read_text(encoding="utf-8"))
            label, code = (("Reference solution:", prob / "solution.py") if key else ("Starter code:", prob / "starter.py"))
            para(d, R(label, size=10, color=ACCENT, bold=True), keep=True)
            para(d, R(code.read_text(encoding="utf-8").replace("\r\n", "\n").rstrip("\n"), size=8, color=INK, mono=True), after=76200)
    return d



# --------------------------------------------------------------- output --
def docx_bytes(d, title):
    d.core_properties.title = title
    d.core_properties.author = "Aayat-AP-Prep"
    buf = io.BytesIO()
    d.save(buf)
    return buf.getvalue()


def docx_signature(blob):
    z = zipfile.ZipFile(io.BytesIO(blob))
    return {n: z.read(n) for n in z.namelist() if n != "docProps/core.xml"}


def emit_docx(path, d, title, to_pdf):
    changed = emit_bytes(path, docx_bytes(d, title), same=lambda a, b: docx_signature(a) == docx_signature(b))
    pdf = path.with_suffix(".pdf")
    keep(pdf)
    if not NO_PDF and (changed or not pdf.exists() or pdf.stat().st_mtime < path.stat().st_mtime):
        to_pdf.append(path)


def make_pdfs(paths):
    if util.CHECK or not paths:
        return
    try:
        import pythoncom
        import win32com.client
        pythoncom.CoInitialize()
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible, word.DisplayAlerts = False, 0
        try:
            for p in paths:
                doc = word.Documents.Open(str(p.resolve()), ReadOnly=True, AddToRecentFiles=False)
                doc.SaveAs2(str(p.with_suffix(".pdf").resolve()), FileFormat=17)       # wdFormatPDF
                doc.Close(False)
                util.changed.append(p.with_suffix(".pdf").relative_to(util.ROOT).as_posix())
        finally:
            word.Quit()
        return
    except ImportError:
        pass
    soffice = shutil.which("soffice") or r"C:\Program Files\LibreOffice\program\soffice.exe"
    for p in paths:
        subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(p.parent), str(p)],
                       check=True, capture_output=True)
        util.changed.append(p.with_suffix(".pdf").relative_to(util.ROOT).as_posix())


def anki(fc):
    import genanki
    tid = fc["topic_id"]
    seed = int(hashlib.sha1(f"ap-cyber-flashcards-{tid}".encode()).hexdigest()[:8], 16)
    model = genanki.Model(
        1607392319, "Aayat-AP-Prep flashcard",
        fields=[{"name": n} for n in ("Front", "Definition", "Example", "Confusion", "Hook")],
        templates=[{"name": "Card", "qfmt": "<div class=front>{{Front}}</div>",
                    "afmt": "{{FrontSide}}<hr id=answer><div>{{Definition}}</div>"
                            "{{#Example}}<p class=ex>{{Example}}</p>{{/Example}}"
                            "{{#Confusion}}<p class=note>{{Confusion}}</p>{{/Confusion}}"
                            "{{#Hook}}<p class=hook>{{Hook}}</p>{{/Hook}}"}],
        css=".card{font-family:Calibri,Arial,sans-serif;font-size:19px;color:#1a1a1a;background:#fff;text-align:left}"
            ".front{font-weight:bold;color:#9c1c2c}.ex{color:#3a3a3a}.note{color:#6e141f;font-size:16px}.hook{font-style:italic;color:#555}")
    deck = genanki.Deck(seed, f'Aayat-AP-Prep::Cybersecurity::{tid} {fc["topic_title"]}')
    for c in fc["flashcards"]:
        deck.add_note(genanki.Note(model=model, guid=genanki.guid_for(c["id"]),
                                   fields=[c.get("front", ""), c.get("back_definition", ""), c.get("back_example", ""),
                                           c.get("back_confusion", ""), c.get("back_hook", "")]))
    return deck


def emit_anki(tid, src):
    """Anki packages carry timestamps, so a deck is rebuilt only when its data is newer (FORCE_ANKI rebuilds all)."""
    import genanki
    import tempfile
    out = downloads_unit(tid) / f"Topic_{tid}_Flashcards.apkg"
    keep(out)
    if out.exists() and out.stat().st_mtime >= src.stat().st_mtime and not FORCE_ANKI:
        return
    util.changed.append(out.relative_to(util.ROOT).as_posix())
    if util.CHECK:
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmpf = Path(tmp) / "deck.apkg"
        genanki.Package(anki(json.loads(src.read_text(encoding="utf-8")))).write_to_file(str(tmpf))
        shutil.copyfile(tmpf, out)


def run():
    to_pdf = []
    for tid in C.order():
        src = C.topic(tid)["src"]
        if (src / "quizbank.xml").exists():
            q = topic_quiz(src / "quizbank.xml")
            name = f"Topic {tid}, {q['topic_title']}"
            emit_docx(downloads_unit(tid) / f"Topic_{tid}_Quiz.docx", quiz_doc(q, False), f"{name} · Quiz", to_pdf)
            emit_docx(teacher_topic(tid) / f"Topic_{tid}_Quiz_AnswerKey.docx", quiz_doc(q, True),
                      f"{name} · Quiz answer key", to_pdf)
            if C.topic_atoms(tid):
                a = assignment_data(tid)
                emit_docx(downloads_unit(tid) / f"Topic_{tid}_Assignment.docx", assignment_doc(a, q["topic_title"], False),
                          f"{name} · Assignment", to_pdf)
                emit_docx(teacher_topic(tid) / f"Topic_{tid}_Assignment_AnswerKey.docx",
                          assignment_doc(a, q["topic_title"], True), f"{name} · Assignment answer key", to_pdf)
        if (src / "flashcards.json").exists():
            emit_anki(tid, src / "flashcards.json")
    make_pdfs(to_pdf)
