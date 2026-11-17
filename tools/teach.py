import argparse
import http.server
import json
import re
import shutil
import socketserver
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from builder import seminars as S

LIVE = "https://zeffiroh.github.io/ap-cybersecurity/"
SOURCE_TYPES = {".md", ".sh", ".py", ".ipynb"}


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def folder_of(name):
    path = S.SEMINARS / slugify(name)
    if not (path / "seminar.json").exists():
        have = ", ".join(p.name for p in S.folders()) or "none yet"
        sys.exit(f"No seminar called {name}. You have: {have}")
    return path


def write_about(path, title):
    about = {"title": title, "summary": "", "units": [], "level": "Beginner", "minutes": 30, "seminar_id": None, "published": False}
    (path / "seminar.json").write_text(json.dumps(about, indent=1) + "\n", encoding="utf-8", newline="\n")


def cmd_new(args):
    path = S.SEMINARS / slugify(args.name)
    if path.exists():
        sys.exit(f"{path} already exists.")
    (path / "files").mkdir(parents=True)
    write_about(path, args.title or args.name)
    (path / "01-look-around.md").write_text(
        "- [ ] List the files\n- [ ] Open the log\n\n> Hint: `ls` lists files.\n\n?> How many files are there? :: 1\n", encoding="utf-8", newline="\n")
    (path / "01-look-around.sh").write_text("ls -l\nhead -n 3 sample.log\n", encoding="utf-8", newline="\n")
    (path / "files" / "sample.log").write_text("2026-11-04 09:00:01 OK user=asha src=10.0.0.5\n2026-11-04 09:00:09 FAIL user=root src=203.0.113.7\n", encoding="utf-8", newline="\n")
    print(f"Made {path.relative_to(ROOT)}")
    print("Replace the example files, set the title in seminar.json, then run: ./teach build " + path.name)


def cmd_from(args):
    src = Path(args.folder).expanduser().resolve()
    if not src.is_dir():
        sys.exit(f"{src} isn't a folder.")
    path = S.SEMINARS / slugify(args.name or src.name)
    if path.exists():
        sys.exit(f"{path} already exists. Choose another name, or copy your files in by hand.")
    (path / "files").mkdir(parents=True)
    write_about(path, args.title or src.name.replace("-", " ").replace("_", " ").title())
    made = 0
    for p in sorted(src.rglob("*")):
        if not p.is_file() or any(part.startswith(".") or part == "__pycache__" for part in p.relative_to(src).parts):
            continue
        if p.parent == src and p.suffix in SOURCE_TYPES:
            made += 1
            stem = p.stem if re.match(r"^\d", p.stem) else f"{made:02d}-{p.stem}"
            shutil.copy2(p, path / (stem + p.suffix))
        else:
            dest = path / "files" / p.relative_to(src)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest)
    print(f"Copied {made} script or note files into {path.relative_to(ROOT)}. Everything else went into files/.")
    check(path)
    print("Set the summary in seminar.json, then run: ./teach build " + path.name)


def check(path):
    bad = S.problems(path)
    for p in sorted(path.glob("*.sh")):
        tested = subprocess.run(["bash", "-n"], input=(S.read(p) + chr(10)).encode("utf-8"), capture_output=True) if shutil.which("bash") else None
        err = tested.stderr.decode("utf-8", "replace") if tested else ""
        if tested and tested.returncode and re.search(r"syntax|unexpected", err):
            bad.append(f"{p.name}: " + err.strip().replace("bash: ", ""))
    for b in bad:
        print(f"  problem: {b}")
    for w in missing_refs(path):
        print(f"  warning: {w}")
    return not bad


def missing_refs(path):
    files = path / "files"
    have = {p.relative_to(files).as_posix() for p in files.rglob("*") if p.is_file()} if files.is_dir() else set()
    names = {h.rsplit("/", 1)[-1] for h in have}
    out = []
    for p in sorted(path.glob("[0-9]*.md")) + sorted(path.glob("[0-9]*.sh")):
        text = re.sub(r"https?://\S+", "", S.read(p))
        text = re.sub(r"```tool[\s\S]*?```", lambda m: " ".join(re.findall(r'"files?": *\[?"([^"\]]+)"', m.group(0))), text)
        if re.search(r"\bREADME\b", text) and "README.txt" not in names:
            out.append(f"{p.name} mentions a README, but files/README.txt is missing")
        for ref in sorted(set(re.findall(r"(?<![\w/.-])((?:[\w-]+/)*[\w.-]+\.(?:log|jsonl|json|csv|eml|txt|pcap|yml|yaml|strings))\b", text))):
            if ref not in have and ref.rsplit("/", 1)[-1] not in names and not re.match(r"(seminar|meta|template|manifest|index)\.json$", ref):
                out.append(f"{p.name} names {ref}, which is not in files/")
    return out


def cmd_build(args):
    targets = [folder_of(args.name)] if args.name else S.folders()
    if not targets:
        sys.exit("No seminars yet. Start with: ./teach new my-seminar")
    fail = 0
    for path in targets:
        print(path.name)
        if not check(path):
            fail += 1
            continue
        info = S.about(path)
        cells = S.cells_of(path, info)
        print(f"  {sum(c['t'] == 'md' for c in cells)} notes, {sum(c['t'] == 'sh' for c in cells)} Linux and {sum(c['t'] == 'py' for c in cells)} Python cells, {len(S.evidence(path))} files")
        if info.get("published", True):
            S.publish_one(path)
            print(f"  Notebook link:  {LIVE}notebook.html?ref=rb-{path.name}&runbook=sem-{path.name}")
            print(f"  Download link:  {LIVE}media/seminars/{path.name}/{path.name}.ipynb")
            if info.get("seminar_id"):
                print(f"  Students who unlock seminar {info['seminar_id']} get this lab, and its page shows a button for it. ./publish puts it live.")
            else:
                print('  This lab is part of Labs. To sell it with a seminar, set "seminar_id" in seminar.json (Teacher -> Seminars shows the ID).')
        else:
            print('  Draft. Set "published": true in seminar.json when it is ready.')
    if fail:
        sys.exit(f"{fail} seminar(s) have problems, so they were left out.")


def cmd_list(args):
    for path in S.folders():
        info = S.about(path)
        print(f"{path.name:32} {'live' if info.get('published', True) else 'draft':6} {info.get('title', '')}")
    if not S.folders():
        print("No seminars yet. Start with: ./teach new my-seminar")


def cmd_media(args):
    S.MEDIA.mkdir(parents=True, exist_ok=True)
    for name in args.files:
        src = Path(name).expanduser()
        if not src.is_file():
            sys.exit(f"{src} isn't a file.")
        if src.stat().st_size > 50_000_000:
            sys.exit(f"{src.name} is over 50 MB. Put videos on YouTube as Unlisted and link to them.")
        dest = S.MEDIA / (args.to or "") / src.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        rel = dest.relative_to(S.MEDIA).as_posix()
        print(f"Added {rel}. After ./publish it is at {LIVE}media/{rel}")


def cmd_preview(args):
    site = ROOT / "site"

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=str(site), **k)

        def log_message(self, *a):
            pass

    print(f"Preview: http://127.0.0.1:{args.port}/notebook.html   Press Ctrl+C to stop.")
    with socketserver.TCPServer(("127.0.0.1", args.port), Quiet) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


def cmd_studio(args):
    sys.path.insert(0, str(ROOT / "tools"))
    from studio import server
    server.run(slugify(args.name), args.title or "", args.source or "", args.shell, args.port, not args.no_open)


def cmd_desk(args):
    sys.path.insert(0, str(ROOT / "tools"))
    from studio import desk
    desk.run(args.port, not args.no_open)


def cmd_finish(args):
    from builder import lesson
    report = lesson.finish(slugify(args.name))
    print(f"{report['folder']}: {report['steps']} steps, {report['commands']} commands, {report['notebookCells']} notebook cells, {report['files']} files.")
    print(f"  {report['recordedOnly']} commands can only be replayed in the browser. The replay was {'made' if report['replay'] else 'not made'}.")
    for line in report["review"] + report["problems"]:
        print(f"  check: {line}")
    print('Read the lab, set "published": true in seminar.json when it is ready, then run: ' + report["next"])


def cmd_capture(args):
    from builder import lesson
    folder = folder_of(args.name)
    cmd = list(args.command)
    if "--" in cmd:
        cut = cmd.index("--")
        pre, cmd = cmd[:cut], cmd[cut + 1:]
        more = argparse.ArgumentParser(prog="teach capture")
        more.add_argument("--files", nargs="*")
        more.add_argument("--shell")
        more.add_argument("--timeout", type=int)
        extra = more.parse_args(pre)
        for k in ("files", "shell", "timeout"):
            if getattr(extra, k) is not None:
                setattr(args, k, getattr(extra, k))
    if not cmd:
        sys.exit("Give the command after --, for example: ./teach capture log-triage -- nmap -sV 10.0.0.5")
    tool = Path(cmd[0]).name
    if not re.fullmatch(r"[A-Za-z0-9_.+-]+", tool):
        sys.exit(f"{tool} isn't a plain tool name.")
    run = cmd
    if args.shell.startswith("wsl"):
        run = ["wsl.exe"] + (["-d", args.shell.split(":", 1)[1]] if ":" in args.shell else []) + ["--"] + cmd
    elif args.shell == "auto" and sys.platform == "win32":
        run = ["wsl.exe", "--"] + cmd
    try:
        r = subprocess.run(run, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=args.timeout)
    except FileNotFoundError:
        sys.exit(f"Couldn't run {cmd[0]}. On Windows this needs WSL; on Linux, install the tool first.")
    except subprocess.TimeoutExpired:
        sys.exit(f"{tool} ran for more than {args.timeout} seconds. Use --timeout to allow longer.")
    scrub = lesson.Scrubber(Path.cwd())
    argstr = scrub(" ".join(cmd[1:]))
    out = scrub((r.stdout or "") + (r.stderr or ""))
    replay = folder / "replay"
    replay.mkdir(exist_ok=True)
    index = replay / "index.txt"
    lines = [l for l in (index.read_text(encoding="utf-8").splitlines() if index.exists() else []) if l.strip()]
    lines = [l for l in lines if l.split("|", 3)[1:2] != [tool] or l.split("|", 3)[3:4] != [argstr]]
    rid = "k" + str(1 + max([int(l.split("|", 1)[0][1:]) for l in lines if re.fullmatch(r"k\d+", l.split("|", 1)[0])] or [0])).zfill(5)
    (replay / f"{rid}.out").write_text(out + ("" if out.endswith("\n") or not out else "\n"), encoding="utf-8", newline="\n")
    for src in args.files or []:
        p = Path(src)
        if not p.is_file():
            sys.exit(f"{src} isn't a file.")
        dst = replay / f"{rid}.files" / p.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(scrub(p.read_text(encoding="utf-8", errors="replace")), encoding="utf-8", newline="\n")
    lines.append(f"{rid}|{tool}|{r.returncode}|{argstr}")
    index.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    about = json.loads((folder / "seminar.json").read_text(encoding="utf-8"))
    tools = about.get("replayTools") or []
    if tool not in tools:
        about["replayTools"] = tools + [tool]
        (folder / "seminar.json").write_text(json.dumps(about, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"Saved {rid}: {tool} {argstr} (exit {r.returncode}, {len(out.splitlines())} lines) in {replay.relative_to(ROOT)}")
    for what, n in sorted(scrub.report.items()):
        print(f"  {n} {what}")
    print(f"Students run it in a Linux cell exactly as: {tool} {argstr}".rstrip())
    print(f"Then: ./teach build {folder.name}")


def cmd_expected(args):
    sys.path.insert(0, str(ROOT / "tools"))
    from studio import expected
    sys.exit(expected.run(args.case))


def cmd_demo(args):
    sys.path.insert(0, str(ROOT / "tools"))
    from studio import demo
    sys.exit(demo.run(args.name, args.speed, args.level))


def cmd_film(args):
    sys.path.insert(0, str(ROOT / "tools"))
    from studio import film
    names = [n.strip() for n in args.name.split(",") if n.strip()]
    bad = sum(film.run(n, args.keep) or 0 for n in names)
    sys.exit(1 if bad else 0)


def cmd_lecture(args):
    sys.path.insert(0, str(ROOT / "tools"))
    from studio import lecture
    sys.exit(lecture.run(args.which))


def cmd_voice(args):
    sys.path.insert(0, str(ROOT / "tools"))
    from studio import voice
    sys.exit(voice.run(args.name, args.port, not args.no_open, args.mix))


def step_titles(path):
    out = []
    for p in sorted(path.glob("[0-9]*.md")):
        first = S.read(p).lstrip().splitlines()[:1]
        out.append(first[0].lstrip("# ").strip() if first and first[0].startswith("#") else S.heading(p.stem).lstrip("# ").strip())
    return out


def script_md(path):
    info = S.about(path)
    sc = info.get("script") or {}
    words = lambda x: len(re.findall(r"\S+", x or ""))
    steps = sc.get("steps") or []
    talk = words(sc.get("intro")) + words(sc.get("outro")) + sum(words(x) if isinstance(x, str) else words(x.get("say") or x.get("before")) + words(x.get("after")) for x in steps)
    kind = info.get("kicker") or ("Free tutorial" if path.name.startswith("t-") else "Seminar")
    title = re.sub(r"^" + re.escape(kind) + r":\s*", "", info.get("title", path.name))
    lines = [f"# Lecture script: {title}", "",
             f"{kind} · about {info.get('minutes', 30)} minutes of lab work · about {max(1, round(talk / 150))} minutes of narration", "",
             "This is what `python tools/teach.py demo " + path.name + "` plays and captions, word for word, and what the voice studio",
             "(`python tools/teach.py voice " + path.name + "`) shows you to read. Edit the words in seminar.json, then run",
             "`python tools/teach.py script " + path.name + "` to refresh this file.", "", "## Opening", "", sc.get("intro") or "", ""]
    files = sorted(path.glob("[0-9]*.md"))
    at = words(sc.get("intro")) / 2.5 + 6
    marks = []
    for i, title in enumerate(step_titles(path)):
        st = steps[i] if i < len(steps) else ""
        before = st if isinstance(st, str) else (st.get("say") or st.get("before") or "")
        after = "" if isinstance(st, str) else (st.get("after") or "")
        body = S.read(files[i]) if i < len(files) else ""
        seen = ["the step text"]
        if files and i < len(files) and files[i].with_suffix(".sh").exists():
            seen.append("the Linux cell")
        if files and i < len(files) and files[i].with_suffix(".py").exists():
            seen.append("the Python cell")
        tools = re.findall(r"```tool (\w+)", body)
        if tools:
            seen.append("the " + ", ".join(dict.fromkeys(tools)) + " tool" + ("s" if len(set(tools)) > 1 else "") + " with the model answer")
        marks.append((at, title))
        at += (words(before) + words(after)) / 2.5 + 3.5 * len(tools) + 4 * (len(seen) > 1)
        lines += [f"## {title}", "", before, ""]
        if after:
            lines += ["*After it runs:*", "", after, ""]
        lines += ["On screen: " + ", ".join(seen) + ".", ""]
    marks.append((at, "Wrap-up"))
    lines += ["## Wrap-up", "", sc.get("outro") or "", "",
              "## YouTube chapters (estimate; `python tools/teach.py demo " + path.name + "` writes the exact ones)", "", "```", "0:00 Opening"]
    lines += [f"{int(t + 5) // 60}:{int(t + 5) % 60:02d} {n}" for t, n in marks] + ["```", ""]
    nl = chr(10)
    (path / "script.md").write_text(nl.join(lines).rstrip() + nl, encoding="utf-8", newline=nl)
    return talk


def cmd_script(args):
    targets = [folder_of(args.name)] if args.name and args.name != "all" else [p for p in S.folders() if S.about(p).get("script")]
    for path in targets:
        talk = script_md(path)
        print(f"{path.name}: script.md written, {talk} words, about {max(1, round(talk / 150))} minutes spoken")


def main():
    ap = argparse.ArgumentParser(prog="teach", description="Turn your seminar scripts into notebooks for the site.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("new", help="start an empty seminar folder")
    p.add_argument("name")
    p.add_argument("title", nargs="?")
    p.set_defaults(fn=cmd_new)
    p = sub.add_parser("from", help="copy a folder of your scripts into a new seminar")
    p.add_argument("folder")
    p.add_argument("--name")
    p.add_argument("--title")
    p.set_defaults(fn=cmd_from)
    p = sub.add_parser("build", help="check a seminar and make its notebook (all seminars if no name)")
    p.add_argument("name", nargs="?")
    p.set_defaults(fn=cmd_build)
    p = sub.add_parser("list", help="list your seminars")
    p.set_defaults(fn=cmd_list)
    p = sub.add_parser("media", help="add files to the website media folder")
    p.add_argument("files", nargs="+")
    p.add_argument("--to", help="a folder inside media, for example slides")
    p.set_defaults(fn=cmd_media)
    p = sub.add_parser("preview", help="open the built site on this computer")
    p.add_argument("--port", type=int, default=8000)
    p.set_defaults(fn=cmd_preview)
    p = sub.add_parser("desk", help="open the Teaching Desk: make, record, edit, check and preview lessons in your browser")
    p.add_argument("--port", type=int, default=8760)
    p.add_argument("--no-open", action="store_true", help="don't open the browser")
    p.set_defaults(fn=cmd_desk)
    p = sub.add_parser("studio", help="teach for real in a live recorded terminal, with optional screen recording")
    p.add_argument("name")
    p.add_argument("--title")
    p.add_argument("--from", dest="source", help="start from a case, seminar or lesson: its files and steps become your plan")
    p.add_argument("--shell", default="auto", help="bash, or wsl:NAME such as wsl:kali-linux (Windows picks Kali, then Ubuntu)")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--no-open", action="store_true", help="don't open the browser")
    p.set_defaults(fn=cmd_studio)
    p = sub.add_parser("finish", help="turn a recording into a lab: codebook, simulated setup, levels, replay, chapters")
    p.add_argument("name")
    p.set_defaults(fn=cmd_finish)
    p = sub.add_parser("capture", help="run a real tool on your Linux and save its output for students to replay")
    p.add_argument("name", help="the seminar folder")
    p.add_argument("--files", nargs="*", help="files the tool wrote, to give students too")
    p.add_argument("--shell", default="auto", help="auto, bash, wsl or wsl:NAME (Windows uses WSL)")
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("command", nargs=argparse.REMAINDER, help="-- then the command, for example: -- nmap -sV 10.0.0.5")
    p.set_defaults(fn=cmd_capture)
    p = sub.add_parser("demo", help="play a seminar lab's walkthrough by itself and save the video, subtitles, chapters and transcript")
    p.add_argument("name", help="a seminar folder such as f-evidence-notes-handoffs, several joined by commas, or tutorials, seminars, network or all")
    p.add_argument("--speed", type=float, default=1.0, help="1 is reading pace; 1.5 is quicker")
    p.add_argument("--level", choices=["", "guided", "solo"], default="", help="leave out for the walkthrough")
    p.set_defaults(fn=cmd_demo)
    p = sub.add_parser("film", help="record a seminar's walkthrough with the real programs in a Linux desktop (needs Docker)")
    p.add_argument("name", help="a seminar folder that has a film.json, or several joined by commas")
    p.add_argument("--keep", action="store_true", help="keep the raw recording, and keep going if a scene fails")
    p.set_defaults(fn=cmd_film)
    p = sub.add_parser("script", help="write a lab's script.md from the narration in its seminar.json")
    p.add_argument("name", nargs="?", default="all")
    p.set_defaults(fn=cmd_script)
    p = sub.add_parser("lecture", help="turn lecture decks into silent videos paced by the speaker notes, with subtitles and a read-along script")
    p.add_argument("which", nargs="?", default="all", help="a lecture number such as 5, several such as 1,2,3, or all")
    p.set_defaults(fn=cmd_lecture)
    p = sub.add_parser("voice", help="record your voice over a silent video with a read-along prompt, then make the final video")
    p.add_argument("name", help="the video folder, for example 24_data_security or t-your-first-sigma-rule")
    p.add_argument("--port", type=int, default=8770)
    p.add_argument("--no-open", action="store_true", help="don't open the browser")
    p.add_argument("--mix", action="store_true", help="only make the final video from what you already recorded")
    p.set_defaults(fn=cmd_voice)
    p = sub.add_parser("expected", help="run labs in the in-browser Linux and save each cell's real output")
    p.add_argument("case", nargs="?", help="one case id; all of them if left out")
    p.set_defaults(fn=cmd_expected)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
