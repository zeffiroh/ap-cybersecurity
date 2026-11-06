import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist"
WORK = ROOT / ".cache" / "app-build"
ICON = ROOT / "tools" / "studio" / "ui" / "desk.ico"


def build(target_dir, python):
    args = python + ["-m", "PyInstaller", "--noconfirm", "--clean", "--onefile", "--console",
                     "--name", "AayatTeachingDesk", "--distpath", str(target_dir),
                     "--workpath", str(WORK / target_dir.name), "--specpath", str(WORK / target_dir.name),
                     str(ROOT / "tools" / "desk_app.py")]
    if ICON.exists():
        args[4:4] = ["--icon", str(ICON)]
    subprocess.run(args, check=True)


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else ("windows" if sys.platform == "win32" else "linux")
    target = OUT / which
    if target.exists():
        shutil.rmtree(target)
    build(target, [sys.executable])
    print(f"Built {next(target.iterdir())}")


if __name__ == "__main__":
    main()
