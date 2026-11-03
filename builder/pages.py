import json
from pathlib import Path

from . import course as C
from . import nav as N
from . import teacher
from .course import BRAND, SUBJECT
from .paths import ASSETS, DOWNLOADS, SHARED, SITE, TESTS, THEME, downloads_unit, unit_dir
from .util import emit, esc, rel


def seen_attr(item):
    return f' data-aa-seen="{item[3]}"' if len(item) > 3 else ""


def links(page_dir, items):
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


def theme_assets(page_dir, css, js):
    r = lambda p: rel(page_dir, p)
    return ("".join(f'<link rel="stylesheet" href="{r(THEME / c)}">\n' for c in css)
            + "".join(f'<script src="{r(THEME / j)}" defer></script>\n' for j in js))


def calendar():
    path = SITE / "calendar.html"
    body = ('<h1>Calendar</h1>\n<p class="aa-sub" id="cal-who">Your class timetable, what\'s due and new videos.</p>\n'
            '<div id="cal"></div>\n<h2>Due for you</h2>\n<div id="cal-due"></div>\n'
            f'<p><a class="btn" href="{rel(path.parent, SITE / "classes.html")}">Live classes: join, book or request one</a></p>\n'
            + theme_assets(path.parent, ["calendar.css"], ["calendar.js"]))
    emit(path, N.shell(path, "", body, cls="aa-wide"))


def classes_page():
    path = SITE / "classes.html"
    body = ('<h1>Live classes</h1>\n<p class="aa-sub" id="sx-status">Loading…</p>\n<div id="sx-classes">\n'
            '<h2>Coming up</h2>\n<div id="sx-upcoming" class="sx-classes"></div>\n'
            '<h2>Ask for a class</h2>\n<div class="sx-form">'
            '<label>Topic <select id="sx-topic"></select></label>'
            '<label>Times that suit you <input id="sx-times" placeholder="e.g. weekends after 4 pm IST"></label>'
            '<label class="sx-wide">What do you want to cover? <textarea id="sx-note" rows="3"></textarea></label>'
            '<button class="btn dark" id="sx-request">Send request</button> <span id="sx-req-msg" class="sx-note"></span></div>\n'
            '<div id="sx-requests"></div>\n'
            '<h2>Recordings</h2>\n<div id="sx-recordings"></div>\n</div>\n'
            + theme_assets(path.parent, [], ["student-extras.js"]))
    emit(path, N.shell(path, "", body))


def videos_page():
    path = SITE / "videos.html"
    body = ('<h1>Video lessons</h1>\n<p class="aa-sub">A video for each lesson, from your teacher.</p>\n'
            '<div id="sx-videos-page"><div id="sx-pass"></div><div id="sx-videos">Loading…</div></div>\n'
            + theme_assets(path.parent, [], ["student-extras.js"]))
    emit(path, N.shell(path, "", body, cls="aa-wide"))


def notebook_page():
    path = SITE / "notebook.html"
    body = ('<div id="nb-app">\n<section id="nb-index" hidden><h1>Notebook</h1>\n'
            '<p class="aa-sub">Your own notes and Python, saved to your account. Python runs right here in the browser.</p>\n'
            '<h2>My notebooks</h2>\n<div id="nb-mine"></div>\n<h2>Open one</h2>\n'
            '<p class="aa-tools"><select id="nb-lesson"></select> <button class="btn dark" id="nb-open">Open my notes</button> '
            '<button class="btn" id="nb-openbook">Open with the code book</button> <button class="btn" id="nb-new">Blank notebook</button></p>\n'
            '</section>\n<section id="nb-editor" hidden><p class="aa-sub" id="nb-crumb"></p>\n'
            '<input id="nb-title" class="nb-title" aria-label="Notebook title">\n'
            '<div class="nb-tools"><button class="btn" id="nb-addmd">+ Notes</button><button class="btn" id="nb-addpy">+ Python</button>'
            '<button class="btn dark" id="nb-runall">Run all</button><button class="btn" id="nb-book">Load the code book</button>'
            '<button class="btn" id="nb-dl">Download .ipynb</button><span id="nb-status" class="nb-status"></span></div>\n'
            '<div id="nb-cells"></div>\n<p class="nb-tools"><small class="nb-status">Shift+Enter runs a Python cell.</small></p>\n'
            '</section>\n</div>\n'
            + theme_assets(path.parent, [], ["notebook.js"]))
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


def run():
    course_map()
    progress_page()
    calendar()
    classes_page()
    videos_page()
    notebook_page()
    results_page()
    downloads_page()
    for u in C.units():
        unit_page(u)
        for tid in u["topics"]:
            topic_page(tid)
    teacher.run()
    home()
