"""Writing site files: only when the content changed, everything recorded, nothing written in --check mode."""
import html
import json
import os
from pathlib import Path
from urllib.parse import quote

from .paths import ROOT, SITE

CHECK = False           # set by build.py
changed = []            # site paths that were (or, with --check, would be) written
produced = set()        # every site path this run accounts for, written or unchanged


def rel(page_dir, target, query=""):
    """URL of `target` from a page in `page_dir`."""
    r = os.path.relpath(Path(target), page_dir).replace("\\", "/")
    return quote(r, safe="/#.-_~") + query


def esc(s):
    return html.escape(str(s), quote=True)


def rd(p):
    """Read text with LF line ends."""
    with open(p, encoding="utf-8", newline="") as f:
        return f.read().replace("\r\n", "\n")


def _note(path):
    path = Path(path)
    produced.add(path.resolve())
    return path


def _record(path):
    changed.append(Path(path).relative_to(ROOT).as_posix())


def emit(path, text, json_equal=False):
    """Write text to path unless it already holds exactly that (or the same JSON data)."""
    path = _note(path)
    from .publish import clean
    text = clean(path, text)
    old = rd(path) if path.exists() else None
    if old == text:
        return False
    if old is not None and json_equal:
        try:
            if json.loads(old) == json.loads(text):
                return False
        except ValueError:
            pass
    _record(path)
    if not CHECK:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
    return True


def emit_bytes(path, blob, same=None):
    """Write bytes unless the file is byte-identical (or `same(old_bytes, blob)` says it is)."""
    path = _note(path)
    if path.exists():
        old = path.read_bytes()
        if old == blob or (same is not None and same(old, blob)):
            return False
    _record(path)
    if not CHECK:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(blob)
    return True


def keep(path):
    """Mark a file another tool wrote in place (PDFs, TikZ SVGs) as part of the site."""
    _note(path)


def dump_json(obj, compact=False):
    if compact:
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n"
    return json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


def stale():
    """Site files no step produced this run."""
    out = []
    for d, _, fs in os.walk(SITE):
        for f in fs:
            p = (Path(d) / f).resolve()
            if p not in produced:
                out.append(p)
    return sorted(out)
