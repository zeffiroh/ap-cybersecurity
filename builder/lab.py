import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from . import course as C
from .course import BRAND
from .paths import SITE, teacher_atom
from .util import keep

LAB = SITE / "lab"


def safe(name):
    return "".join(ch for ch in name if ch not in r'<>:"/\|?*').strip()[:60]

START = """# Welcome to the {brand} lab

This is JupyterLab running entirely in your browser. Python runs on your own computer, nothing to install.

* Every skill's **code book** is in the folders on the left, by unit and topic.
* Run a cell with **Shift+Enter**. Missing packages install with `%pip install name` (for example `%pip install cryptography`).
* Your files are saved **in this browser only**. To keep a notebook in your course account, use
  *File > Download*, then open the course **Notebook** page and choose *Import .ipynb*.
"""


def contents(root):
    root.mkdir(parents=True, exist_ok=True)
    (root / "Start here.ipynb").write_text(json.dumps({
        "nbformat": 4, "nbformat_minor": 5,
        "metadata": {"kernelspec": {"name": "python", "display_name": "Python (Pyodide)", "language": "python"}},
        "cells": [{"cell_type": "markdown", "metadata": {}, "source": START.format(brand=BRAND)},
                  {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
                   "source": "import hashlib\nprint(hashlib.sha256(b'hello, lab').hexdigest())"}]}, indent=1), encoding="utf-8")
    n = 0
    for u in C.units():
        for tid in u["topics"]:
            folder = root / safe(f"Unit {u['num']} {u['title']}") / safe(f"{tid} {C.topic(tid)['title']}")
            for a in C.topic_atoms(tid):
                src = teacher_atom(a["id"]) / f"{a['id']}-student.ipynb"
                if src.exists():
                    folder.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(src, folder / (safe(f"{a['id']} {a['title']}") + ".ipynb"))
                    n += 1
    return n


def extensions():
    from jupyter_core.paths import jupyter_path
    found = []
    for base in jupyter_path("labextensions"):
        for pkg in Path(base).glob("@jupyterlite/*"):
            if (pkg / "package.json").exists():
                found.append(str(pkg))
    return found


def run():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        n = contents(tmp / "files")
        (tmp / "jupyter_lite_config.json").write_text(json.dumps({
            "LiteBuildConfig": {"contents": [str(tmp / "files")], "output_dir": str(tmp / "out"), "no_sourcemaps": True,
                                "federated_extensions": extensions()}}),
            encoding="utf-8")
        (tmp / "overrides.json").write_text(json.dumps({
            "@jupyterlab/apputils-extension:themes": {"theme": "JupyterLab Light"}}), encoding="utf-8")
        subprocess.run(["jupyter", "lite", "build", "--lite-dir", str(tmp)], check=True, cwd=tmp)
        if LAB.exists():
            shutil.rmtree(LAB)
        shutil.copytree(tmp / "out", LAB)
    from .ctf import gate_tree
    gate_tree(LAB)
    for f in LAB.rglob("*"):
        if f.is_file():
            keep(f)
    print(f"  lab: {n} code books")
