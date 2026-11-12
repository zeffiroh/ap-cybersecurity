import argparse
import io
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = [ROOT / "source" / "lectures" / "images"]
MAX_CHANGE = 3.0
MIN_SAVING = 0.9


def shrink(data):
    im = Image.open(io.BytesIO(data))
    im.load()
    base = im.convert("RGBA") if im.mode in ("RGBA", "LA", "P", "PA") else im.convert("RGB")
    method = Image.Quantize.FASTOCTREE if base.mode == "RGBA" else Image.Quantize.MEDIANCUT
    q = base.quantize(256, method=method, dither=Image.Dither.FLOYDSTEINBERG)
    change = max(ImageStat.Stat(ImageChops.difference(base.convert("RGB"), q.convert("RGB"))).mean)
    if change > MAX_CHANGE:
        return None
    out = io.BytesIO()
    q.save(out, "PNG", optimize=True)
    blob = out.getvalue()
    return blob if len(blob) < len(data) * MIN_SAVING else None


def main():
    ap = argparse.ArgumentParser(description="Make PNG images smaller (256 colours) where it doesn't visibly change them.")
    ap.add_argument("folders", nargs="*", type=Path, default=DEFAULT)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    before = after = changed = 0
    for folder in a.folders:
        for p in sorted(folder.rglob("*.png")):
            data = p.read_bytes()
            before += len(data)
            blob = shrink(data)
            if blob is None:
                after += len(data)
                continue
            after += len(blob)
            changed += 1
            if not a.dry_run:
                p.write_bytes(blob)
    print(f"{changed} images made smaller: {before / 1048576:.1f} MB -> {after / 1048576:.1f} MB" + (" (dry run, nothing written)" if a.dry_run else ""))


if __name__ == "__main__":
    sys.exit(main())
