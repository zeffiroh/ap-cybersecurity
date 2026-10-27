"""The course's own pages: home, units, topics, progress, calendar, saved results, downloads,
the course map the progress scripts read, and the teacher pages (hub and one page per topic)."""
import json
from pathlib import Path

from . import course as C
from . import nav as N
from .course import BRAND, SUBJECT
from .paths import (ASSETS, DOWNLOADS, LECTURES, SHARED, SITE, TEACHER, TESTS, THEME, downloads_unit,
                    teacher_atom, teacher_topic, unit_dir)
from .util import emit, esc, rel


def seen_attr(item):
    return f' data-aa-seen="{item[3]}"' if len(item) > 3 else ""


def links(page_dir, items):
    """[(label, path, query[, seen key])] -> a row of link buttons, skipping files that do not exist."""
    out = [f'<a href="{rel(page_dir, it[1], it[2])}"{seen_attr(it)}>{esc(it[0])}</a>'
           for it in items if it[1] and Path(it[1]).exists()]
    return f'<div class="aa-links">{"".join(out)}</div>'


def scripts(page_dir):
    r = lambda p: rel(page_dir, p)
    return (f'<script src="{r(ASSETS / "config.js")}"></script>\n<script src="{r(SHARED / "neon.js")}"></script>\n'
            f'<script src="{r(SHARED / "sponsor-metrics.js")}"></script>\n'
            f'<script src="{r(SHARED / "support.js")}"></script>')


def materials(tid):
    return [(lbl, N.target(tid, k), "", f"{k}|{tid}") for k, lbl in N.KINDS[1:] if N.has(tid, k)]


def files(tid):
    d = downloads_unit(tid)
    return [("Quiz (PDF)", d / f"Topic_{tid}_Quiz.pdf", ""),
            ("Assignment (PDF)", d / f"Topic_{tid}_Assignment.pdf", ""),
            ("Flashcards (Anki)", d / f"Topic_{tid}_Flashcards.apkg", ""),
            ("Slides (PowerPoint)", d / f"Topic_{tid}_Slides.pptx", "")]


def atom_row(page_dir, a):
    r = lambda p: rel(page_dir, p)
    ls = [("Lesson", N.lesson_page(a), ""), ("Sim", N.sim_page(a), ""),
          ("Code", N.problem_page(a), ""), ("Quiz", N.quiz_page(a), "")]
    return (f'<li><span class="aa-what"><i class="aa-lvl" data-aa-atom="{a["id"]}"></i><span class="aa-id">{a["id"]}</span>'
            f'<a href="{r(N.lesson_page(a))}">{esc(a["title"])}</a></span>{links(page_dir, ls)}</li>')


# ------------------------------------------------------------------ student --
def home():
    path = SITE / "index.html"
    d = path.parent
    top = links(d, [(label, p, "") for key, label, p in N.GLOBAL if key != "home"])
    cards = []
    for u in C.units():
        t, q = N.unit_test(u["num"])
        rows = "".join(f'<li><span class="aa-id">{tid}</span><a href="{rel(d, N.target(tid, "topic"))}">'
                       f'{esc(C.topic(tid)["title"])}</a> <span class="aa-pct" data-aa-topic="{tid}"></span></li>'
                       for tid in u["topics"])
        cards.append(f'<div class="aa-card"><h3><a href="{rel(d, unit_dir(u["num"]) / "index.html")}">'
                     f'<span class="aa-id">Unit {u["num"]}</span>{esc(u["title"])}</a> '
                     f'<span class="aa-pct" data-aa-unit="{u["num"]}"></span></h3><ol>{rows}</ol>'
                     f'<p style="margin:10px 0 0">{links(d, [("Unit test", t, q), ("Unit quiz", N.unit_quiz(u["num"]), "")])}</p></div>')
    body = (f'<h1>{SUBJECT}</h1>\n<p class="aa-sub">{len(C.order())} topics &middot; {len(C.atom_order())} skills</p>\n'
            f'{top}\n<h2>Units</h2>\n<div class="aa-grid">{"".join(cards)}</div>')
    emit(path, N.shell(path, f"{BRAND} · {SUBJECT}", body))


def unit_page(u):
    path = unit_dir(u["num"]) / "index.html"
    d = path.parent
    t, q = N.unit_test(u["num"])
    rows = []
    for tid in u["topics"]:
        sq = "".join(f'<i class="aa-lvl" data-aa-atom="{a["id"]}"></i>' for a in C.topic_atoms(tid))
        rows.append(f'<li><span class="aa-what"><span class="aa-id">{tid}</span><a href="{rel(d, N.target(tid, "topic"))}">'
                    f'{esc(C.topic(tid)["title"])}</a> <span class="aa-pct" data-aa-topic="{tid}"></span>'
                    f'<br><span class="aa-squares">{sq}</span></span>{links(d, materials(tid))}</li>')
    body = (f'<h1><span class="aa-id">Unit {u["num"]}</span>{esc(u["title"])} '
            f'<span class="aa-pct" data-aa-unit="{u["num"]}"></span></h1>\n'
            f'{links(d, [("Unit test", t, q), ("Unit quiz", N.unit_quiz(u["num"]), ""), ("CW/HW quizzes", TESTS / "hw" / "index.html", "")])}\n'
            f'<h2>Topics</h2>\n<ul class="aa-list">{"".join(rows)}</ul>\n{scripts(d)}')
    emit(path, N.shell(path, "", body))


def topic_page(tid):
    path = N.target(tid, "topic")
    d = path.parent
    t = C.topic(tid)
    los = "".join(f"<li>{esc(lo)}</li>" for lo in t["los"])
    atoms = "".join(atom_row(d, a) for a in C.topic_atoms(tid))
    body = (f'<h1><span class="aa-id">{tid}</span>{esc(t["title"])} <span class="aa-pct" data-aa-topic="{tid}"></span></h1>\n'
            f'<ul class="aa-los">{los}</ul>\n'
            f'<h2>Study</h2>\n{links(d, materials(tid))}\n'
            f'<h2>Practice</h2>\n<ul class="aa-list">{atoms}</ul>\n'
            f'<h2>Downloads</h2>\n{links(d, files(tid))}\n{scripts(d)}')
    emit(path, N.shell(path, "", body))


def course_map():
    """assets/theme/course-map.js: units, topics, skills and their pages (paths from the site root)."""
    root = lambda p: Path(p).relative_to(SITE).as_posix()
    data = {"units": [{"n": u["num"], "title": u["title"], "href": root(unit_dir(u["num"]) / "index.html"),
                       "topics": u["topics"]} for u in C.units()],
            "topics": {tid: {"u": C.topic(tid)["unit"], "title": C.topic(tid)["title"],
                             "href": root(N.target(tid, "topic")),
                             "atoms": [a["id"] for a in C.topic_atoms(tid)],
                             "mats": {k: root(N.target(tid, k)) for k, _ in N.KINDS[1:] if N.has(tid, k)}}
                       for tid in C.order()},
            "atoms": {a["id"]: {"title": a["title"], "href": root(N.lesson_page(a))} for a in C.atom_order()}}
    emit(THEME / "course-map.js", "window.AAYAT_MAP = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")


def progress_page():
    path = SITE / "progress.html"
    body = (f'<h1>Progress</h1>\n<div id="aa-progress"></div>\n'
            f'<script src="{rel(path.parent, THEME / "progress-page.js")}" defer></script>')
    emit(path, N.shell(path, "", body))


def calendar():
    path = SITE / "calendar.html"
    seq = C.atom_order()
    per_day = 2
    days = [seq[i:i + per_day] for i in range(0, len(seq), per_day)]
    rows = "".join(
        f'<tr><td>{i}</td><td>' + "<br>".join(
            f'<span class="aa-id">{a["id"]}</span><a href="{rel(SITE, N.lesson_page(a))}">{esc(a["title"])}</a>'
            for a in day) + "</td></tr>" for i, day in enumerate(days, start=1))
    body = f'<h1>Calendar</h1>\n<p class="aa-sub">{per_day} skills a day</p>\n<table><tr><th>Day</th><th>Skills</th></tr>{rows}</table>'
    emit(path, N.shell(path, "", body))


RESULTS = """<h1>Saved results</h1>
<p class="aa-sub">Skill quizzes taken in this browser</p>
<p><button class="btn" onclick="exportCsv()">Export CSV</button>
<button class="btn" onclick="if(confirm('Clear all saved results?')){localStorage.removeItem('bb_results');render();}">Clear</button></p>
<table id="rtable"></table>
<script>
var HEAD = '<tr><th>Skill</th><th>Score</th><th>Max</th><th>%</th><th>Attempts</th><th>Last attempt</th></tr>';
function results(){ try{return JSON.parse(localStorage.getItem('bb_results')||'{}');}catch(e){return {};} }
function render(){
  var r = results(), t = document.getElementById('rtable');
  t.innerHTML = HEAD;
  Object.keys(r).sort().forEach(function(id){
    var e = r[id], pct = e.max ? Math.round(100*e.score/e.max) : 0;
    t.innerHTML += '<tr><td>'+id+'</td><td>'+e.score+'</td><td>'+e.max+'</td><td>'+pct+'%</td><td>'+e.attempts+'</td><td>'+new Date(e.last).toLocaleString()+'</td></tr>';
  });
}
function exportCsv(){
  var r = results(), rows = ['atom,score,max,pct,attempts,last'];
  Object.keys(r).sort().forEach(function(id){
    var e = r[id], pct = e.max ? Math.round(100*e.score/e.max) : 0;
    rows.push([id,e.score,e.max,pct,e.attempts,new Date(e.last).toISOString()].join(','));
  });
  var link = document.createElement('a');
  link.href = URL.createObjectURL(new Blob([rows.join('\\n')], {type:'text/csv'}));
  link.download = 'quiz_results.csv'; link.click();
}
render();
</script>"""


def results_page():
    path = SITE / "results.html"
    emit(path, N.shell(path, f"Saved results · {BRAND}", RESULTS))


def downloads_page():
    path = DOWNLOADS / "index.html"
    d = path.parent
    from .paths import DOWNLOADS as DL
    from .book import store_html
    book_pdf = DL / "AP_Cybersecurity_Textbook.pdf"
    sections = [f'<h2>Textbook</h2>\n<div class="aa-links">{store_html(rel(d, book_pdf), rel(d, SITE / "buy" / "index.html"))}</div>'
                if book_pdf.exists() else ""]
    for u in C.units():
        rows = "".join(f'<tr><td><span class="aa-id">{tid}</span><a href="{rel(d, N.target(tid, "topic"))}">{esc(C.topic(tid)["title"])}</a></td>'
                       f'<td>{links(d, files(tid) + [("Quiz (Word)", downloads_unit(tid) / f"Topic_{tid}_Quiz.docx", ""), ("Assignment (Word)", downloads_unit(tid) / f"Topic_{tid}_Assignment.docx", "")])}</td></tr>'
                       for tid in u["topics"])
        sections.append(f'<h2>Unit {u["num"]} &middot; {esc(u["title"])}</h2>\n<table>{rows}</table>')
    emit(path, N.shell(path, "", "<h1>Downloads</h1>\n" + "\n".join(sections)))


# ------------------------------------------------------------------ teacher --
TOOLS = [  # (label, path) of the teacher-side tools
    ("Class progress (mastery by student)", TEACHER / "progress.html"),
    ("Class dashboard (quiz and assignment scores)", TEACHER / "class-report.html"),
    ("Adaptive test dashboard", TEACHER / "tests.html"),
    ("Database check", TEACHER / "database-check.html"),
    ("Tutor posts feed (RSS)", TEACHER / "feed.xml"),
    ("Support and sponsorship page", SITE / "support.html"),
    ("Site icon (exports every icon file)", THEME / "icon.html"),
]


def class_progress_page():
    path = TEACHER / "progress.html"
    body = ('<h1>Class progress</h1>\n<p class="aa-sub" id="status"></p>\n'
            '<p class="aa-tools"><select id="unit"></select> <select id="sort"><option value="name">Sort by email</option>'
            '<option value="mastery">Sort by mastery</option><option value="last">Sort by last active</option></select> '
            '<input id="q" type="search" placeholder="Find a student"> <button class="btn" id="reload">Refresh</button> '
            '<button class="btn" id="csv">Export CSV</button></p>\n'
            '<div id="grid" class="aa-scroll"></div>\n<div id="detail"></div>\n'
            f'<script src="{rel(path.parent, THEME / "progress-tutor.js")}" defer></script>')
    emit(path, N.shell(path, f"Class progress · {BRAND}", body, cls="aa-wide"))


def teacher_topic_page(tid):
    """Everything for teaching one topic."""
    path = teacher_topic(tid) / "index.html"
    d = path.parent
    t = C.topic(tid)
    teach = [("Topic deck with speaker notes", d / "slides.html", ""), ("Classroom PowerPoint", downloads_unit(tid) / f"Topic_{tid}_Slides.pptx", ""),
             ("Student view", N.target(tid, "topic"), "")]
    keys = [("Quiz key (PDF)", d / f"Topic_{tid}_Quiz_AnswerKey.pdf", ""),
            ("Quiz key (Word)", d / f"Topic_{tid}_Quiz_AnswerKey.docx", ""),
            ("Assignment key (PDF)", d / f"Topic_{tid}_Assignment_AnswerKey.pdf", ""),
            ("Assignment key (Word)", d / f"Topic_{tid}_Assignment_AnswerKey.docx", ""),
            ("Activity keys", d / "activity-keys.html", "")]
    rows = []
    for a in C.topic_atoms(tid):
        ad = teacher_atom(a["id"])
        ls = [("Solution", ad / "solution.html", ""), ("Solution notebook", ad / f"{a['id']}-solution.ipynb", ""),
              ("Solution preview", ad / "solution-preview.html", ""),
              ("Assignment page", ad / "assign.html", ""), ("Student notebook", ad / f"{a['id']}-student.ipynb", ""),
              ("Pre-lecture post", ad / "pre-lecture-post.html", ""), ("Post-lecture post", ad / "post-lecture-post.html", ""),
              ("Pre-lecture handout", ad / f"{a['id']}-pre-lecture-handout.docx", ""),
              ("Post-lecture handout", ad / f"{a['id']}-post-lecture-handout.docx", "")]
        rows.append(f'<li><span class="aa-what"><span class="aa-id">{a["id"]}</span>{esc(a["title"])}</span>{links(d, ls)}</li>')
    body = (f'<p class="aa-sub"><a href="{rel(d, TEACHER / "index.html")}">Teacher hub</a></p>\n'
            f'<h1><span class="aa-id">{tid}</span>{esc(t["title"])}</h1>\n'
            f'<h2>Teach</h2>\n{links(d, teach)}\n<h2>Answer keys</h2>\n{links(d, keys)}\n'
            f'<h2>Skills</h2>\n<ul class="aa-list">{"".join(rows)}</ul>\n')
    emit(path, N.shell(path, f"{tid} {t['title']} · Teacher · {BRAND}", body))


def teacher_hub():
    path = TEACHER / "index.html"
    d = path.parent
    tools = "".join(f'<li><a href="{rel(d, p)}">{esc(label)}</a></li>' for label, p in TOOLS)
    units = []
    for u in C.units():
        rows = "".join(f'<li><span class="aa-id">{tid}</span><a href="{rel(d, teacher_topic(tid) / "index.html")}">'
                       f'{esc(C.topic(tid)["title"])}</a></li>' for tid in u["topics"])
        units.append(f'<h3>Unit {u["num"]} &middot; {esc(u["title"])}</h3>\n<ul>{rows}</ul>')
    decks = "".join(f'<tr><td>{n:02d}</td><td><a href="{rel(d, p)}">{esc(t)}</a></td>'
                    f'<td>{links(d, [("PowerPoint", TEACHER / "lectures" / (p.stem + ".pptx"), "")])}</td></tr>'
                    for n, p, t in N.decks())
    body = (f'<h1>Teacher hub</h1>\n<p class="aa-sub"><a href="{rel(d, SITE / "index.html")}">Student home</a> &middot; '
            f'<a href="{rel(d, DOWNLOADS / "AP_Cybersecurity_Textbook.pdf")}">Textbook (PDF)</a></p>\n'
            f'<h2>Tools</h2>\n<ul>{tools}</ul>\n<h2>Topics</h2>\n{"".join(units)}\n'
            f'<h2>Lecture decks</h2>\n<table><tr><th>#</th><th>Deck</th><th>Files</th></tr>{decks}</table>')
    emit(path, N.shell(path, f"Teacher hub · {BRAND}", body))


def run():
    course_map()
    progress_page()
    calendar()
    results_page()
    downloads_page()
    for u in C.units():
        unit_page(u)
        for tid in u["topics"]:
            topic_page(tid)
            teacher_topic_page(tid)
    class_progress_page()
    teacher_hub()
    home()                  # last: its link row shows only pages that exist
