from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = Path(__file__).resolve().parent / "templates"

SRC = ROOT / "source"
UNITS_SRC = SRC / "units"
LECTURES_SRC = SRC / "lectures"
TEXTBOOK_SRC = SRC / "textbook"
TESTS_SRC = SRC / "tests"
CAPSTONE_SRC = SRC / "capstone"
STATIC_SRC = SRC / "static"

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
