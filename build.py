#!/usr/bin/env python3
"""Build the course site: everything in source/ -> site/.

    python build.py                    build what changed
    python build.py --check            report what would change, write nothing
    python build.py --only pages,book  run some steps (see --list)
    python build.py --skip lectures
    python build.py --no-pdf           Word files only, no PDF conversion (no Word/LibreOffice needed)
    python build.py --estimate         lecture decks: split long slides by estimate, without a browser
    python build.py --prune            also delete site/ files that no source produces any more
    python build.py --audit            check the built site for broken links and duplicate sources
    python build.py --verify           run every coding problem: solutions must pass, starters must fail

Steps run in this order; a failing step is reported and the rest still run.
"""
import argparse
import sys
import time
import traceback

from builder import util

STEPS = [  # name, what it builds
    ("static", "hand-made files, notes, images, sims, flashcard data, capstone world"),
    ("tests", "adaptive unit tests and CW/HW quizzes"),
    ("materials", "topic quizzes, flashcards, assignments, coding problems, activities, SimLab, skill pages"),
    ("teacher", "solutions, notebooks, tutor posts, handouts, activity keys"),
    ("slides", "topic slide decks and classroom PowerPoints"),
    ("lectures", "the 30 lecture decks and their PowerPoints"),
    ("downloads", "printable quizzes and assignments, answer keys, Anki decks"),
    ("book", "the online book and the textbook PDF"),
    ("pages", "home, unit, topic, progress, calendar, downloads and teacher pages"),
]


def step(name, args):
    from builder import (adaptive, book, downloads, lectures, materials, pages, slides, static, tutor)
    if name == "static":
        static.run()
    elif name == "tests":
        adaptive.run()
    elif name == "materials":
        materials.run()
    elif name == "teacher":
        tutor.run()
    elif name == "slides":
        slides.run()
    elif name == "lectures":
        lectures.ESTIMATE, lectures.NO_PPTX = args.estimate, args.no_pptx
        lectures.SHOW_UNFINISHED = args.show_unfinished_images
        lectures.run()
    elif name == "downloads":
        downloads.NO_PDF, downloads.FORCE_ANKI = args.no_pdf, args.anki
        downloads.run()
    elif name == "book":
        book.run()
        book.pdf(force=args.force_pdf)
    elif name == "pages":
        pages.run()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--skip", default="")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--no-pdf", action="store_true")
    ap.add_argument("--no-pptx", action="store_true")
    ap.add_argument("--estimate", action="store_true")
    ap.add_argument("--anki", action="store_true", help="rebuild every Anki deck")
    ap.add_argument("--force-pdf", action="store_true", help="recompile the textbook PDF")
    ap.add_argument("--show-unfinished-images", action="store_true")
    ap.add_argument("--prune", action="store_true")
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()
    names = [n for n, _ in STEPS]

    if args.list:
        for n, what in STEPS:
            print(f"{n:10} {what}")
        return 0
    if args.verify:
        from builder import course
        from builder.atomtext import verify_problems
        bad = verify_problems(course.atom_order())
        print("coding problems:", "every solution passes and every starter fails" if not bad else f"{len(bad)} problem(s)")
        for b in bad:
            print("  ", b)
        return 1 if bad else 0
    if args.audit:
        from builder import audit
        return 0 if audit.run(args.verbose) else 1

    def parse(s):
        got = [x for x in s.split(",") if x]
        bad = set(got) - set(names)
        if bad:
            sys.exit(f"unknown step(s): {', '.join(sorted(bad))} (see --list)")
        return got
    only, skip = parse(args.only) if args.only else names, parse(args.skip)
    util.CHECK = args.check
    results = []
    for name in names:
        if name not in only or name in skip:
            continue
        print(f"=== {name}", flush=True)
        t, before = time.time(), len(util.changed)
        try:
            step(name, args)
            status = "ok"
        except Exception:
            traceback.print_exc()
            status = "FAILED"
        n = len(util.changed) - before
        results.append((name, status, n, time.time() - t))
        if args.verbose or args.check:
            for c in util.changed[before:before + 40]:
                print("  ", c)
            if n > 40:
                print(f"   ... and {n - 40} more")
    verb = "would change" if args.check else "changed"
    print("\n=== summary")
    for name, status, n, secs in results:
        print(f"{name:10} {status:7} {n:5} file(s) {verb}   {secs:6.1f}s")
    if only == names and not skip and all(s == "ok" for _, s, _, _ in results):
        old = util.stale()
        if old:
            print(f"\n{len(old)} file(s) in site/ that no source produces" + (" (deleted)" if args.prune and not args.check else
                                                                              " (python build.py --prune deletes them)"))
            for p in old[:20]:
                print("  ", p.relative_to(util.ROOT).as_posix())
            if args.prune and not args.check:
                for p in old:
                    p.unlink()
    return 1 if any(s != "ok" for _, s, _, _ in results) else 0


if __name__ == "__main__":
    sys.exit(main())
