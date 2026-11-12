import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

NAME = "Aayat Teaching Desk"
SAVED = Path.home() / ".aayat-teaching-desk.json"
REPO = "https://github.com/zeffiroh/ap-cybersecurity.git"
WIN = sys.platform == "win32"


def is_course(p):
    return p is not None and (p / "build.py").is_file() and (p / "tools" / "teach.py").is_file()


def here():
    return Path(sys.executable if getattr(sys, "frozen", False) else __file__).resolve().parent


def find_course():
    env = os.environ.get("AAYAT_COURSE")
    if env and is_course(Path(env)):
        return Path(env)
    for start in (here(), Path.cwd()):
        for p in (start, *start.parents):
            if is_course(p):
                return p
    try:
        saved = Path(json.loads(SAVED.read_text(encoding="utf-8"))["course"])
        if is_course(saved):
            return saved
    except (OSError, ValueError, KeyError):
        pass
    print(f"{NAME} needs your course folder, the one with build.py in it.")
    print("Type its path, or type get to download the course into your home folder.")
    while True:
        try:
            typed = input("Course folder: ").strip().strip('"')
        except EOFError:
            return None
        if not typed:
            return None
        if typed.lower() == "get":
            got = download()
            if got:
                SAVED.write_text(json.dumps({"course": str(got)}), encoding="utf-8")
                return got
            continue
        p = Path(typed).expanduser()
        if is_course(p):
            SAVED.write_text(json.dumps({"course": str(p.resolve())}), encoding="utf-8")
            return p.resolve()
        print("That folder has no build.py and tools/teach.py. Try again, or press Enter to stop.")


def download():
    dst = Path.home() / "AayatCourse"
    if is_course(dst):
        return dst
    if not shutil.which("git"):
        print("Downloading needs Git. Install it from https://git-scm.com, then try again.")
        return None
    print(f"Downloading the course into {dst} (a few minutes)...")
    if subprocess.call(["git", "clone", "--depth", "1", REPO, str(dst)]) != 0 or not is_course(dst):
        print("The download didn't finish. Check your internet connection and try again.")
        return None
    py = shutil.which("python3") or shutil.which("python") or (shutil.which("py") and "py")
    if py:
        print("Installing the course's Python packages...")
        subprocess.call([py] + (["-3"] if py == "py" else []) + ["-m", "pip", "install", "--user", "-r", str(dst / "requirements.txt")])
    return dst


def find_python(course):
    names = [course / ".venv" / "Scripts" / "python.exe", course / ".venv" / "bin" / "python"]
    cands = [[str(p)] for p in names if p.exists()]
    if WIN and shutil.which("py"):
        cands.append(["py", "-3"])
    for n in ("python3", "python"):
        w = shutil.which(n)
        if w:
            cands.append([w])
    for c in cands:
        try:
            ok = subprocess.run(c + ["-c", "import yaml, markdown, PIL"], capture_output=True, timeout=60).returncode == 0
        except (OSError, subprocess.SubprocessError):
            ok = False
        if ok:
            return c
    return None


def pause():
    if WIN and getattr(sys, "frozen", False) and sys.stdin and sys.stdin.isatty():
        try:
            input("Press Enter to close.")
        except EOFError:
            pass


def main(argv):
    course = find_course()
    if not course:
        print("No course folder, so nothing was opened.")
        pause()
        return 1
    py = find_python(course)
    if not py:
        print("No Python on this computer has the course's packages.")
        print(f"Install Python 3.10 or newer, then run in {course}:")
        print("    pip install -r requirements.txt")
        pause()
        return 1
    args = argv or ["desk"]
    print(f"{NAME}: {course}")
    print("Close this window, or press Ctrl+C, to stop.")
    try:
        return subprocess.call(py + [str(course / "tools" / "teach.py"), *args], cwd=course)
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
