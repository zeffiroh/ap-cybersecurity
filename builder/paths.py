"""Where everything lives. Sources are under source/, the published site under site/."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = Path(__file__).resolve().parent / "templates"

SRC = ROOT / "source"
UNITS_SRC = SRC / "units"            # unit-N/<X.Y-slug>/ (topic) and <X.Y.z-slug>/ (skill)
LECTURES_SRC = SRC / "lectures"      # NN_name.md, images/
TEXTBOOK_SRC = SRC / "textbook"      # LaTeX, book-inserts.json
TESTS_SRC = SRC / "tests"            # adaptive unit tests and CW/HW banks
CAPSTONE_SRC = SRC / "capstone"      # Operation Quiet Harbor: world, stages, toolkit
STATIC_SRC = SRC / "static"          # copied to site/ as they are

SITE = ROOT / "site"
ASSETS = SITE / "assets"
THEME = ASSETS / "theme"
SHARED = ASSETS / "shared"
BOOK = SITE / "book"
LECTURES = SITE / "lectures"
TESTS = SITE / "tests"
CAPSTONE = SITE / "capstone"
DOWNLOADS = SITE / "downloads"
TEACHER = SITE / "teacher"


def unit_dir(n):
    return SITE / f"unit-{int(n)}"


def topic_dir(tid):
    return unit_dir(tid.split(".")[0]) / tid


def atom_dir(aid):
    return topic_dir(aid.rsplit(".", 1)[0]) / aid


def teacher_topic(tid):
    return TEACHER / f"unit-{int(tid.split('.')[0])}" / tid


def teacher_atom(aid):
    return teacher_topic(aid.rsplit(".", 1)[0]) / aid


def downloads_unit(tid):
    return DOWNLOADS / f"unit-{int(tid.split('.')[0])}"
