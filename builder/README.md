# Building the site

Everything you edit is in `source/`; `python build.py` turns it into `site/`, which is what gets published.
Never edit `site/` by hand.

```
python build.py                    # build what changed
python build.py --check            # list what would change, write nothing
python build.py --only pages,book  # some steps (python build.py --list)
python build.py --audit            # broken links, duplicate sources
python build.py --verify           # coding problems: solutions pass, starters fail
```

Needs Python 3.10+ (`pip install -r requirements.txt`, then `python -m playwright install chromium`),
MiKTeX or TeX Live for the textbook PDF, and Word or LibreOffice for the PDF downloads (`--no-pdf` skips them).

## Where things are

A topic folder, `source/units/unit-N/X.Y-<name>/`:

| File | What it is |
|---|---|
| `notes.html` | the topic's Notes page |
| `slides.json` | the topic slide deck (and, under `classroom`, the PowerPoint-only slides) |
| `images/` | the slides' and notes' diagrams; Mermaid diagrams keep their code beside the PNG as `.mmd` |
| `quizbank.xml` | the topic quiz (also the book's "Check Your Understanding" and the printable quiz) |
| `flashcards.json` | the flashcard deck (also the Anki download) |
| `X.Y.z-<name>/` | one skill: `atom.md` (lesson), `quiz.yaml`, `sim.html`, `activity.md`, `tutor.md`, `problem/`, `banner.png`, `lab.html` |

| To change | Edit |
|---|---|
| Unit or topic titles, learning objectives | `source/course.json` |
| Skill titles, objectives, coding-problem points | `source/atoms.json` |
| A unit's classwork quiz (Units 2–5) | `source/units/unit-N/classwork-quiz.json` |
| Unit-test, Unit 1 classwork and CW/HW questions | `source/tests/` |
| A lecture deck or its images (```mermaid blocks are drawn at build time) | `source/lectures/` |
| The textbook; online-only book diagrams and boxes | `source/textbook/`; `source/textbook/book-inserts.json` |
| The buy page (store links: Razorpay, Gumroad, ebook stores; blank shows "coming soon") | `source/static/buy/index.html` |
| Capstone world, stages, toolkit, rubric | `source/capstone/` |
| Glossary, report card, capstone page, test pages, styles, scripts | `source/static/` (same path as in `site/`) |
| Database connection (Neon URLs) | `source/static/assets/config.js`; schema in `db/` |
| The bar, page titles, which materials a topic shows | `builder/nav.py` |
| Home, unit, topic, downloads and teacher pages | `builder/pages.py` |

New skill: copy a skill folder, add it to `source/atoms.json`, rebuild. Published scripts, styles and pages
are written without comments (`builder/publish.py`).

## Publishing

Build, then push to GitHub. In *Settings → Pages* choose *Source: GitHub Actions*;
`.github/workflows/pages.yml` publishes `site/` on every push to `main`. Add the site's address to Neon
Auth's trusted origins (`db/README.md`). The database connection string with the password lives only in
`.env`, which is never published.

The textbook PDF is published locked (AES-256) with `BOOK_PDF_PASSWORD` from `.env`; buyers get that password
after paying. The build refuses to publish the PDF if the password is missing. Changing the password: edit
`.env`, then `python build.py --only book --force-pdf`.
