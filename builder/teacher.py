import json
from pathlib import Path

from . import course as C
from . import nav as N
from .course import BRAND
from .paths import DOWNLOADS, SITE, TEACHER, THEME, downloads_unit, teacher_atom, teacher_topic
from .util import emit, esc, rel

SIDEBAR = [
    ("dash", "Dashboard", TEACHER / "index.html"),
    ("teach", "Teach a class", TEACHER / "teach.html"),
    ("lectures", "Lectures", TEACHER / "lectures.html"),
    ("live", "Live classes", TEACHER / "classes.html"),
    ("schedule", "Calendar", TEACHER / "schedule.html"),
    ("assign", "Assignments", TEACHER / "assignments.html"),
    ("videos", "Lesson videos", TEACHER / "videos.html"),
    ("seminars", "Seminars", TEACHER / "seminars.html"),
    ("labs", "Labs & notebooks", TEACHER / "labs.html"),
    ("ctf", "Capture the flag", TEACHER / "ctf.html"),
    ("students", "Students, classes & cohorts", TEACHER / "students.html"),
    ("forum", "Classes & forum", SITE / "community.html"),
    ("progress", "Class progress", TEACHER / "progress.html"),
    ("grades", "Gradebook", TEACHER / "class-report.html"),
    ("tests", "Adaptive tests", TEACHER / "tests.html"),
    ("resources", "Resources", TEACHER / "resources.html"),
    ("blog", "Blog", TEACHER / "blog.html"),
    ("accounts", "Accounts", TEACHER / "accounts.html"),
]

PRODUCTS = [
    ("Course · Razorpay (India)", "https://rzp.io/rzp/unlock-aap-cybersecurity"),
    ("Course · Gumroad (international, $299)", "https://mitaliaayatmahnoor.gumroad.com/l/cybersecurity-kickstarter"),
    ("Textbook PDF password · Razorpay (India)", "https://rzp.io/rzp/ap-cyber-security-mitali"),
    ("Textbook PDF + EPUB · Gumroad ($39)", "https://mitaliaayatmahnoor.gumroad.com/l/ap-cybersecurity-textbook"),
    ("Textbook · Payhip", ""),
    ("Textbook · Pothi (paperback and ebook)", ""),
]

DASHBOARDS = [
    ("Razorpay payment pages", "https://dashboard.razorpay.com/app/paymentpages"),
    ("Gumroad products", "https://app.gumroad.com/products"),
    ("Gumroad payouts", "https://app.gumroad.com/settings/payments"),
    ("Payhip dashboard", "https://payhip.com/login"),
    ("Pothi dashboard", "https://pothi.com"),
    ("Neon database", "https://console.neon.tech"),
    ("GitHub repository", "https://github.com/zeffiroh/ap-cybersecurity"),
    ("GitHub Actions (sync robots)", "https://github.com/zeffiroh/ap-cybersecurity/actions"),
    ("cron-job.org (5-minute timer)", "https://console.cron-job.org/jobs"),
]


def site_rel(p):
    return Path(p).relative_to(SITE).as_posix()


def have(p):
    return site_rel(p) if Path(p).exists() else ""


def console(path, title, key, body, scripts=()):
    d = Path(path).parent
    side = "".join(f'<a href="{rel(d, p)}"{" class=on" if k == key else ""}>{esc(label)}</a>' for k, label, p in SIDEBAR)
    html = (f'<link rel="stylesheet" href="{rel(d, THEME / "teacher.css")}">\n'
            f'<link rel="stylesheet" href="{rel(d, THEME / "calendar.css")}">\n'
            f'<div class="tc"><nav class="tc-side" aria-label="Teacher"><div class="tc-brand">Teacher</div>{side}'
            f'<div class="tc-foot"><a href="{rel(d, SITE / "index.html")}">Student view</a></div></nav>\n'
            f'<div class="tc-main" data-tc="{key}">\n{body}\n</div></div>\n'
            + "".join(f'<script src="{rel(d, p)}" defer></script>\n' for p in [TEACHER / "teach-data.js", THEME / "calendar.js", *scripts])
            + f'<script src="{rel(d, THEME / "teacher.js")}" defer></script>')
    emit(path, N.shell(path, f"{title} · Teacher · {BRAND}", html, cls="aa-wide aa-tc"))


def teach_data():
    atoms, topics = {}, {}
    for tid in C.order():
        td, dl = teacher_topic(tid), downloads_unit(tid)
        topics[tid] = {"title": C.topic(tid)["title"], "unit": C.topic(tid)["unit"],
                       "page": have(td / "index.html"), "student": have(N.target(tid, "topic")),
                       "slides": have(td / "slides.html"), "ppt": have(dl / f"Topic_{tid}_Slides.pptx"),
                       "quizKey": have(td / f"Topic_{tid}_Quiz_AnswerKey.pdf"),
                       "assignKey": have(td / f"Topic_{tid}_Assignment_AnswerKey.pdf"),
                       "activityKeys": have(td / "activity-keys.html"),
                       "quizPdf": have(dl / f"Topic_{tid}_Quiz.pdf"), "assignPdf": have(dl / f"Topic_{tid}_Assignment.pdf")}
        for a in C.topic_atoms(tid):
            ad, aid = teacher_atom(a["id"]), a["id"]
            atoms[aid] = {"topic": tid, "title": a["title"], "lesson": have(N.lesson_page(a)), "sim": have(N.sim_page(a)),
                          "quiz": have(N.quiz_page(a)), "code": have(N.problem_page(a)),
                          "solution": have(ad / "solution.html"), "assign": have(ad / "assign.html"),
                          "pre": have(ad / "pre-lecture-post.html"), "post": have(ad / "post-lecture-post.html"),
                          "preDoc": have(ad / f"{aid}-pre-lecture-handout.docx"),
                          "postDoc": have(ad / f"{aid}-post-lecture-handout.docx")}
    units = [{"n": u["num"], "title": u["title"], "test": site_rel(N.unit_test(u["num"])[0]) + N.unit_test(u["num"])[1],
              "quiz": have(N.unit_quiz(u["num"]))} for u in C.units()]
    data = {"order": [a["id"] for a in C.atom_order()], "atoms": atoms, "topics": topics, "units": units,
            "decks": [{"n": n, "title": t, "stem": p.stem, "page": have(p), "ppt": have(TEACHER / "lectures" / (p.stem + ".pptx"))}
                      for n, p, t in N.decks()]}
    emit(TEACHER / "teach-data.js", "window.AAYAT_TEACH = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")


def dashboard():
    body = ('<header class="tc-head"><div><h1>Dashboard</h1><p class="aa-sub" id="status">Loading…</p></div>'
            '<button class="btn" id="reload">Refresh</button></header>\n'
            '<section class="tc-kpis" id="kpis"></section>\n'
            '<section class="tc-row">\n'
            '  <div class="tc-card tc-next" id="next"></div>\n'
            '  <div class="tc-card"><h3>Online now</h3><div id="online"></div></div>\n'
            '</section>\n'
            '<section class="tc-row">\n'
            '  <div class="tc-card"><h3>Live classes <a class="tc-more" href="classes.html">All</a></h3><div id="liveclasses"></div></div>\n'
            '  <div class="tc-card"><h3>Due soon <a class="tc-more" href="assignments.html">Assignments</a></h3><div id="due"></div></div>\n'
            '</section>\n'
            '<section class="tc-row">\n'
            '  <div class="tc-card"><h3>Class mastery by unit</h3><div id="units"></div></div>\n'
            '  <div class="tc-card"><h3>Next on the blog</h3><div id="posts"></div></div>\n'
            '</section>\n'
            '<section class="tc-card"><h3>Students <a class="tc-more" href="progress.html">Full progress</a></h3>'
            '<div id="roster" class="aa-scroll"></div></section>')
    console(TEACHER / "index.html", "Dashboard", "dash", body, [TEACHER / "posts.js"])


def teach_page():
    body = ('<header class="tc-head"><div><p class="tc-kicker" id="when"></p><h1 id="title">Teach a class</h1>'
            '<p class="aa-sub" id="skills"></p></div>'
            '<div class="tc-headtools"><select id="grp" aria-label="Group"></select><button class="btn" id="prev">&larr; Previous</button>'
            '<select id="pick"></select><button class="btn" id="next">Next &rarr;</button></div></header>\n'
            '<div class="tc-teach">\n'
            '  <section class="tc-stage"><div class="tc-tabs" id="tabs"></div>'
            '<div class="tc-frame"><iframe id="frame" title="Class material" allowfullscreen></iframe></div>'
            '<div class="tc-under"><a id="open" class="btn" target="_blank" rel="noopener">Open in a new tab (present full screen)</a></div></section>\n'
            '  <aside class="tc-rail">\n'
            '    <div class="tc-card"><h3>Timer</h3><div class="tc-timer" id="timer">00:00</div>'
            '<div class="tc-btns" id="timer-btns"></div></div>\n'
            '    <div class="tc-card"><h3>Share with the class</h3><div id="share"></div><p class="tc-note" id="copied"></p></div>\n'
            '    <div class="tc-card"><h3>Live <span class="tc-dot"></span></h3><div id="live">Loading…</div></div>\n'
            '    <div class="tc-card"><h3>Teacher only</h3><div id="private"></div></div>\n'
            '  </aside>\n</div>')
    console(TEACHER / "teach.html", "Teach a class", "teach", body, [TEACHER / "posts.js"])


def schedule_page():
    body = ('<header class="tc-head"><div><h1>Calendar</h1><p class="aa-sub" id="status">Loading…</p></div>'
            '<div class="tc-headtools"><select id="show"></select></div></header>\n'
            '<section class="tc-card"><div id="tcal"></div></section>\n'
            '<section class="tc-card tc-form"><h3>Timetable for <select id="plan-for"></select></h3>'
            '<label>First class <input type="date" id="start"></label>'
            '<label>Starts at <input type="time" id="time"></label>'
            '<label>Minutes <input type="number" id="minutes" min="15" max="480" step="5" value="60"></label>'
            '<label>Skills per class <input type="number" id="per" min="1" max="6" value="2"></label>'
            '<fieldset id="days"><legend>Class days</legend></fieldset>'
            '<label class="tc-wide">Days off (holidays, exams), comma separated <input id="off" placeholder="2026-12-25, 2027-01-01"></label>'
            '<button class="btn dark" id="save">Save timetable</button> <span id="saved" class="tc-note"></span>'
            '<p class="tc-note tc-wide">Students in a group see that group\'s timetable on their calendar; everyone else sees the Everyone timetable.</p></section>')
    console(TEACHER / "schedule.html", "Calendar", "schedule", body, [])


def classes_page():
    body = ('<header class="tc-head"><div><h1>Live classes</h1><p class="aa-sub" id="status">Loading…</p></div>'
            '<button class="btn dark" id="new">New class</button></header>\n'
            '<section class="tc-card"><h3>Class requests</h3><div id="requests"></div></section>\n'
            '<section class="tc-card"><h3>Availability for custom lectures</h3>'
            '<p class="tc-note">Click the hours you\'re free each week. Students book a free hour on the Live classes page; '
            'booked hours and your live classes are hidden automatically.</p>'
            '<div class="tc-filters"><label>Time zone <input id="av-tz" placeholder="Asia/Kolkata"></label>'
            '<label>Lecture length (min) <input id="av-min" type="number" min="15" max="240" step="15" value="60" style="width:6em"></label>'
            '<label>Weeks ahead <input id="av-weeks" type="number" min="1" max="8" value="2" style="width:5em"></label></div>'
            '<div id="av-grid" class="tc-avgrid aa-scroll"></div>'
            '<p><button class="btn dark" id="av-save">Save availability</button> <span id="av-msg" class="tc-note"></span></p></section>\n'
            '<section class="tc-card tc-form" id="form" hidden><h3 id="form-title">New class</h3>'
            '<label class="tc-wide">Title <input id="c-title" placeholder="Firewalls, live walkthrough"></label>'
            '<label>Topic <select id="c-topic"></select></label>'
            '<label>Starts <input type="datetime-local" id="c-starts"></label>'
            '<label>Minutes <input type="number" id="c-minutes" min="15" max="480" step="5" value="60"></label>'
            '<label>Kind <select id="c-mode"><option value="open">Open: anyone signed in joins free</option>'
            '<option value="paid">Batch / cohort class: students book with tickets</option>'
            '<option value="request">1:1 class: only the student who asked</option></select></label>'
            '<label>Tickets per seat <input type="number" id="c-tickets" min="0" max="50" value="1" style="width:7em"></label>'
            '<label>Seats (0 = no limit) <input type="number" id="c-cap" min="0" value="0" style="width:7em"></label>'
            '<label class="tc-wide">Meeting link, shown only to students with a seat. Leave it blank for a free Jitsi Meet room '
            '<input id="c-meet" placeholder="Blank = a Jitsi room is made for you"></label>'
            '<label class="tc-wide">Recording (unlisted YouTube link), shown only to students with a seat <input id="c-rec" placeholder="https://youtu.be/…"></label>'
            '<label class="tc-wide">Note for students <textarea id="c-note" rows="2"></textarea></label>'
            '<button class="btn dark" id="c-save">Save class</button> <button class="btn" id="c-cancel">Close</button> '
            '<span class="tc-note" id="c-msg"></span></section>\n'
            '<section id="list"></section>')
    console(TEACHER / "classes.html", "Live classes", "live", body, [])


def assignments_page():
    body = ('<header class="tc-head"><div><h1>Assignments</h1><p class="aa-sub" id="status">Loading…</p></div></header>\n'
            '<section class="tc-card tc-form"><h3>Assign something</h3>'
            '<label>To <select id="a-group"></select></label>'
            '<label>What <select id="a-kind"><option value="skill">Skill lesson</option><option value="topic">Whole topic</option>'
            '<option value="quiz">Topic quiz</option><option value="adaptive">Adaptive unit test</option><option value="video">Video</option>'
            '<option value="lecture">Lecture deck</option><option value="link">Any link</option></select></label>'
            '<label class="tc-wide">Item <select id="a-item"></select><input id="a-link" placeholder="https://…" hidden></label>'
            '<label>Due <input type="datetime-local" id="a-due"></label>'
            '<label class="tc-wide">Note <input id="a-note" placeholder="Do the sim before Thursday"></label>'
            '<button class="btn dark" id="a-save">Assign</button> <span class="tc-note" id="a-msg"></span></section>\n'
            '<p class="aa-tools"><select id="a-filter"></select></p>\n<section id="list"></section>')
    console(TEACHER / "assignments.html", "Assignments", "assign", body, [])


def ctf_page():
    body = ('<header class="tc-head"><div><h1>Capture the flag</h1><p class="aa-sub" id="status">Loading…</p></div>'
            f'<div class="tc-btns"><a class="btn" href="{rel(TEACHER, SITE / "ctf.html")}">Student board</a></div></header>\n'
            '<section class="tc-card tc-form" id="f-card"><h3 id="f-head">New challenge</h3>'
            '<label class="tc-wide">Title <input id="f-title" maxlength="200"></label>'
            '<label>Unit <select id="f-unit"><option value="0">Any</option><option>1</option><option>2</option><option>3</option>'
            '<option>4</option><option>5</option></select></label>'
            '<label>Points <input id="f-points" type="number" min="10" max="1000" step="10" value="100"></label>'
            '<label class="tc-wide">Puzzle (put data between ``` lines, code between `backticks`) <textarea id="f-body" rows="6"></textarea></label>'
            '<label class="tc-wide">Hint <input id="f-hint"></label>'
            '<label class="tc-wide">Link (a site page, e.g. cyberchef/index.html, linux.html, sqli.html) <input id="f-link"></label>'
            '<label class="tc-wide">Flag students must find, e.g. aayat{...} (not case-sensitive) <input id="f-flag" autocomplete="off"></label>'
            '<label class="tc-wide">Walkthrough (teachers only) <textarea id="f-solve" rows="3"></textarea></label>'
            '<div class="tc-btns"><button class="btn dark" id="f-save">Save challenge</button>'
            '<button class="btn" id="f-new" hidden>Cancel edit</button><span class="tc-note" id="f-msg"></span></div></section>\n'
            '<section class="tc-card"><h3>Challenges and answers</h3><p class="tc-note">Flags and walkthroughs show only here, '
            'to teachers. Students see a hash.</p><div id="c-list"></div></section>\n'
            '<section class="tc-card"><h3>Latest solves</h3><div id="c-solves"></div></section>')
    console(TEACHER / "ctf.html", "Capture the flag", "ctf", body)


def seminars_page():
    body = ('<header class="tc-head"><div><h1>Seminars</h1><p class="aa-sub" id="status">Loading…</p></div>'
            f'<div class="tc-btns"><a class="btn" href="{rel(TEACHER, SITE / "seminars.html")}">Student view</a></div></header>\n'
            '<section class="tc-card tc-form" id="s-card"><h3 id="s-head">New seminar</h3>'
            '<label class="tc-wide">Title <input id="s-title" maxlength="200"></label>'
            '<label class="tc-wide">YouTube link (a video or a playlist, uploaded as Unlisted) <input id="s-youtube" placeholder="https://youtube.com/playlist?list=…"></label>'
            '<label class="tc-wide">One-line summary <input id="s-summary" maxlength="500"></label>'
            '<label class="tc-wide">Full description (what it covers, who it is for) <textarea id="s-description" rows="6"></textarea></label>'
            '<label>Level <select id="s-level"><option value="">Any</option><option>Beginner</option><option>Intermediate</option><option>Advanced</option></select></label>'
            '<label>Length (minutes) <input id="s-minutes" type="number" min="0" step="5"></label>'
            '<label>Tickets to unlock (0 = free) <input id="s-tickets" type="number" min="0" max="100" value="1"></label>'
            '<label>Order <input id="s-sort" type="number" value="0"></label>'
            '<label class="tc-wide">Topics (comma separated) <input id="s-topics" placeholder="malware, incident response"></label>'
            '<label class="tc-wide">Cover image link (optional; the YouTube thumbnail is used otherwise) <input id="s-cover"></label>'
            '<label class="tc-wide"><span>Chapters, one per line: <code>0:00 Introduction</code></span><textarea id="s-chapters" rows="6"></textarea></label>'
            '<label class="tc-wide"><span>Resources for buyers, one per line: <code>Slides | https://…</code></span><textarea id="s-resources" rows="3"></textarea></label>'
            '<label class="tc-check"><input type="checkbox" id="s-published"> Published (students can see it)</label>'
            '<div class="tc-btns"><button class="btn dark" id="s-save">Save seminar</button>'
            '<button class="btn" id="s-new" hidden>Cancel edit</button><span class="tc-note" id="s-msg"></span></div></section>\n'
            '<section class="tc-card"><h3>Your seminars</h3><div id="s-list"></div></section>')
    console(TEACHER / "seminars.html", "Seminars", "seminars", body)


def labs_page():
    body = ('<header class="tc-head"><div><h1>Labs &amp; notebooks</h1><p class="aa-sub" id="status">Loading…</p></div>'
            f'<div class="tc-btns"><a class="btn" href="{rel(TEACHER, SITE / "labs.html")}">Student view</a></div></header>\n'
            '<p class="tc-note">Labs and notebooks made here are stored in the database and are only sent to students who have Labs. '
            'They never appear in the public site files.</p>\n'
            '<section class="tc-card tc-form" id="l-card"><h3 id="l-head">New lab</h3>'
            '<label>Kind <select id="l-kind"><option value="lab">Lab (instructions)</option><option value="notebook">Notebook (Python)</option></select></label>'
            '<label class="tc-wide">Title <input id="l-title" maxlength="200"></label>'
            '<label>Unit <select id="l-unit"><option value="0">Any</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option></select></label>'
            '<label>Topic <input id="l-topic" placeholder="e.g. 5.1" maxlength="20"></label>'
            '<label>Tool <select id="l-tool"><option value="">None</option><option value="linux">Linux lab</option><option value="jupyter">JupyterLab</option>'
            '<option value="sqli">SQL injection lab</option><option value="shop">Hack the shop</option><option value="cyberchef">CyberChef</option>'
            '<option value="ctf">CTF board</option></select></label>'
            '<label class="tc-wide">Summary <input id="l-summary" maxlength="1000"></label>'
            '<label class="tc-wide" id="l-body-wrap"><span>Instructions. Blank line = new paragraph, <code># Heading</code>, <code>`code`</code>, '
            'and a block of commands between <code>```</code> lines gets a Copy button.</span><textarea id="l-body" rows="14"></textarea></label>'
            '<div class="tc-wide" id="l-nb-wrap" hidden><p class="tc-note">Write the notebook in the full editor (Python runs there), or import a .ipynb file.</p>'
            '<div class="tc-btns"><a class="btn" id="l-edit-nb" target="_blank" rel="noopener">Open in the notebook editor</a>'
            '<button class="btn" id="l-import">Import .ipynb</button><input type="file" id="l-file" accept=".ipynb,application/json" hidden>'
            '<span class="tc-note" id="l-cells"></span></div></div>'
            '<label class="tc-check"><input type="checkbox" id="l-published"> Published (Labs students can open it)</label>'
            '<div class="tc-btns"><button class="btn dark" id="l-save">Save</button>'
            '<button class="btn" id="l-new" hidden>Cancel edit</button><span class="tc-note" id="l-msg"></span></div></section>\n'
            '<section class="tc-card"><h3>Stored in the database</h3><div id="l-list"></div></section>')
    console(TEACHER / "labs.html", "Labs & notebooks", "labs", body)


def videos_page():
    body = ('<header class="tc-head"><div><h1>Lesson videos</h1><p class="aa-sub" id="status">Loading…</p></div>'
            '<a class="btn" href="../videos.html" target="_blank" rel="noopener">Student view</a></header>\n'
            '<section class="tc-card tv-post"><h3 id="v-head">Post a video</h3><div class="tv-cols"><div class="tv-fields">'
            '<label class="tv-f">YouTube link <small>Upload it as Unlisted, then paste the link</small><input id="v-yt" placeholder="https://youtu.be/…"></label>'
            '<label class="tv-f">Title <input id="v-title" placeholder="e.g. Spotting a phishing link"></label>'
            '<div class="tv-row"><label class="tv-f">Lesson <select id="v-atom"></select></label>'
            '<label class="tv-f">Who sees it <select id="v-group"></select></label></div>'
            '<label class="tv-f">Note for students <small>optional</small><textarea id="v-note" rows="2" placeholder="e.g. Watch before Thursday\'s class."></textarea></label>'
            '<div class="tv-checks"><label><input type="checkbox" id="v-free"> <span><b>Free for everyone</b><small>No Labs needed</small></span></label>'
            '<label><input type="checkbox" id="v-email"> <span><b>Email students</b><small>Sent within about 5 minutes</small></span></label></div>'
            '<div class="tc-btns"><button class="btn dark" id="v-save">Post video</button><button class="btn" id="v-reset">Clear</button>'
            '<span class="tc-note" id="v-msg"></span></div></div>'
            '<aside class="tv-preview" aria-live="polite"><div class="tc-kicker">Preview</div><div class="tv-pthumb" id="v-pthumb"><span>Paste a YouTube link to see it here</span></div>'
            '<div class="tv-ptitle" id="v-ptitle">Untitled video</div><div class="tc-note" id="v-pmeta">Not tied to a lesson · Labs</div></aside></div></section>\n'
            '<section class="tc-card"><h3>Posted <span class="tc-note tv-count" id="v-count"></span></h3><div id="list" class="tv-list"></div></section>')
    console(TEACHER / "videos.html", "Lesson videos", "videos", body, [])


def lectures_page():
    path = TEACHER / "lectures.html"
    d = path.parent
    rows = "".join(f'<tr><td>{n:02d}</td><td>{esc(t)}</td><td><span class="tc-links">'
                   f'<a class="btn dark" href="present.html?deck={p.stem}">Present with notes</a>'
                   f'<a href="{rel(d, p)}" target="_blank" rel="noopener">Slides only</a>'
                   + link_list(d, [("PowerPoint", TEACHER / "lectures" / (p.stem + ".pptx"))]) + '</span></td></tr>'
                   for n, p, t in N.decks())
    topics = "".join(f'<tr><td><span class="aa-id">{tid}</span></td><td>{esc(C.topic(tid)["title"])}</td><td><span class="tc-links">'
                     + link_list(d, [("Topic deck with notes", teacher_topic(tid) / "slides.html"),
                                     ("PowerPoint", downloads_unit(tid) / f"Topic_{tid}_Slides.pptx")]) + '</span></td></tr>'
                     for tid in C.order())
    body = ('<header class="tc-head"><div><h1>Lectures</h1><p class="aa-sub">Present any deck with your speaker notes beside it. '
            'Put the slides on the projector and keep the notes on your screen; they stay in step.</p></div></header>\n'
            f'<section class="tc-card"><h3>Lecture decks (30)</h3><table class="tc-table">{rows}</table></section>\n'
            f'<section class="tc-card"><h3>Topic decks</h3><table class="tc-table">{topics}</table></section>')
    console(path, "Lectures", "lectures", body)


def present_page():
    body = ('<header class="tc-head"><div><p class="tc-kicker"><a href="lectures.html">Lectures</a></p><h1 id="p-title">Present</h1></div>'
            '<div class="tc-headtools"><span class="tc-clock" id="p-clock">00:00</span>'
            '<button class="btn" id="p-reset">Reset timer</button>'
            '<a class="btn dark" id="p-pop" target="deck-projector">Open slides for the projector</a></div></header>\n'
            '<div class="tc-present"><div class="tc-frame"><iframe id="p-frame" title="Slides" allowfullscreen></iframe></div>'
            '<aside class="tc-card tc-notes"><h3><span id="p-count">Slide 1</span><span id="p-unit" class="tc-note"></span></h3>'
            '<div class="tc-kicker" id="p-slide"></div><div id="p-notes" class="tc-notesbody">Loading notes…</div>'
            '<p class="tc-note">Arrow keys move the slides. The notes follow along here and on the projector window.</p></aside></div>')
    console(TEACHER / "present.html", "Present", "lectures", body, [])


def blog_page():
    body = ('<header class="tc-head"><div><h1>Blog</h1><p class="aa-sub">Pre- and post-lecture posts for every skill, '
            'in course order. Copy one into your class stream, or share the link.</p></div>'
            f'<a class="btn" href="feed.xml">RSS feed</a></header>\n'
            '<div class="bl-bar"><select id="unit" aria-label="Unit"></select> <select id="kind" aria-label="Which posts"><option value="">Before and after class</option>'
            '<option value="pre">Before class only</option><option value="post">After class only</option></select> '
            '<input id="q" type="search" placeholder="Search posts" aria-label="Search posts"><span class="tc-note" id="bl-count"></span></div>\n'
            '<div id="blog" class="bl-list"></div>')
    console(TEACHER / "blog.html", "Blog", "blog", body, [TEACHER / "posts.js"])


def link_list(d, items):
    return "".join(f'<a href="{rel(d, p)}">{esc(label)}</a>' for label, p in items if p and Path(p).exists())


def resources_page():
    path = TEACHER / "resources.html"
    d = path.parent
    units = []
    for u in C.units():
        cards = []
        for tid in u["topics"]:
            td, dl = teacher_topic(tid), downloads_unit(tid)
            teach = link_list(d, [("Topic deck", td / "slides.html"), ("PowerPoint", dl / f"Topic_{tid}_Slides.pptx"),
                                  ("Student view", N.target(tid, "topic")), ("Quiz (PDF)", dl / f"Topic_{tid}_Quiz.pdf"),
                                  ("Assignment (PDF)", dl / f"Topic_{tid}_Assignment.pdf")])
            keys = link_list(d, [("Quiz key", td / f"Topic_{tid}_Quiz_AnswerKey.pdf"),
                                 ("Quiz key (Word)", td / f"Topic_{tid}_Quiz_AnswerKey.docx"),
                                 ("Assignment key", td / f"Topic_{tid}_Assignment_AnswerKey.pdf"),
                                 ("Assignment key (Word)", td / f"Topic_{tid}_Assignment_AnswerKey.docx"),
                                 ("Activity keys", td / "activity-keys.html")])
            skills = "".join(
                f'<li><span class="aa-id">{a["id"]}</span>{esc(a["title"])}<span class="tc-links">'
                + link_list(d, [("Solution", teacher_atom(a["id"]) / "solution.html"),
                                ("Assignment", teacher_atom(a["id"]) / "assign.html"),
                                ("Pre post", teacher_atom(a["id"]) / "pre-lecture-post.html"),
                                ("Post post", teacher_atom(a["id"]) / "post-lecture-post.html"),
                                ("Pre handout", teacher_atom(a["id"]) / f"{a['id']}-pre-lecture-handout.docx"),
                                ("Post handout", teacher_atom(a["id"]) / f"{a['id']}-post-lecture-handout.docx"),
                                ("Notebook", teacher_atom(a["id"]) / f"{a['id']}-solution.ipynb")])
                + "</span></li>" for a in C.topic_atoms(tid))
            cards.append(f'<article class="tc-card tc-topic"><h3><span class="aa-id">{tid}</span>'
                         f'<a href="{rel(d, td / "index.html")}">{esc(C.topic(tid)["title"])}</a></h3>'
                         f'<a class="btn tc-go" href="teach.html?topic={tid}">Teach this topic</a>'
                         f'<div class="tc-group"><b>Teach</b><span class="tc-links">{teach}</span></div>'
                         f'<div class="tc-group"><b>Answer keys</b><span class="tc-links">{keys}</span></div>'
                         f'<details><summary>Skills ({len(C.topic_atoms(tid))})</summary><ul class="tc-skills">{skills}</ul></details>'
                         f'</article>')
        units.append(f'<details class="tc-unit" open><summary><span class="aa-id">Unit {u["num"]}</span>{esc(u["title"])}</summary>'
                     f'<div class="tc-grid">{"".join(cards)}</div></details>')
    decks = "".join(f'<tr><td>{n:02d}</td><td><a href="{rel(d, p)}">{esc(t)}</a></td>'
                    f'<td><span class="tc-links">{link_list(d, [("PowerPoint", TEACHER / "lectures" / (p.stem + ".pptx"))])}</span></td></tr>'
                    for n, p, t in N.decks())
    book = link_list(d, [("Textbook (PDF)", DOWNLOADS / "AP_Cybersecurity_Textbook.pdf"), ("Online book", SITE / "book" / "index.html"),
                         ("All downloads", DOWNLOADS / "index.html"), ("Glossary", SITE / "glossary.html"),
                         ("Student calendar", SITE / "calendar.html")])
    body = ('<header class="tc-head"><div><h1>Resources</h1><p class="aa-sub">Everything for teaching, by unit and topic. '
            'Keys and solutions are for you only.</p></div>'
            '<input id="q" type="search" placeholder="Find a topic or skill"></header>\n'
            f'<section class="tc-card"><h3>Course books</h3><span class="tc-links">{book}</span></section>\n'
            f'{"".join(units)}\n'
            f'<details class="tc-unit"><summary>Lecture decks (30)</summary><table class="tc-table">'
            f'<tr><th>#</th><th>Deck</th><th>Files</th></tr>{decks}</table></details>')
    console(path, "Resources", "resources", body)


def accounts_page():
    path = TEACHER / "accounts.html"
    d = path.parent
    out = lambda items: "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(label)}</a></li>' if u
                                else f'<li>{esc(label)} <i class="tc-note">not set up yet</i></li>' for label, u in items)
    own = [("Buy page (textbook)", SITE / "buy" / "index.html"), ("Pay page (course)", SITE / "pay" / "index.html"),
           ("Unlock page (codes)", SITE / "unlock" / "index.html"), ("Support and sponsorship", SITE / "support.html"),
           ("Ledger (open with your private link)", SITE / "ledger" / "index.html")]
    tools = [("Database check", TEACHER / "database-check.html"), ("Tutor posts feed (RSS)", TEACHER / "feed.xml"),
             ("Site icon (exports every icon file)", THEME / "icon.html")]
    li = lambda items: "".join(f'<li><a href="{rel(d, p)}">{esc(label)}</a></li>' for label, p in items)
    body = ('<header class="tc-head"><div><h1>Accounts</h1><p class="aa-sub">Store links, site pages and the dashboards '
            'behind the course. Dashboards ask you to sign in.</p></div></header>\n<div class="tc-grid">'
            f'<section class="tc-card"><h3>Products</h3><ul class="tc-ul">{out(PRODUCTS)}</ul></section>'
            f'<section class="tc-card"><h3>Site pages</h3><ul class="tc-ul">{li(own)}</ul></section>'
            f'<section class="tc-card"><h3>Dashboards</h3><ul class="tc-ul">{out(DASHBOARDS)}</ul></section>'
            f'<section class="tc-card"><h3>Tools</h3><ul class="tc-ul">{li(tools)}</ul></section></div>')
    console(path, "Accounts", "accounts", body)


def class_progress_page():
    path = TEACHER / "progress.html"
    body = ('<header class="tc-head"><div><h1>Class progress</h1><p class="aa-sub" id="status"></p></div></header>\n'
            '<p class="aa-tools"><select id="unit"></select> <select id="sort"><option value="name">Sort by email</option>'
            '<option value="mastery">Sort by mastery</option><option value="last">Sort by last active</option></select> '
            '<input id="q" type="search" placeholder="Find a student"> <button class="btn" id="reload">Refresh</button> '
            '<button class="btn" id="csv">Export CSV</button></p>\n'
            '<div id="grid" class="aa-scroll"></div>\n<div id="detail"></div>')
    console(path, "Class progress", "progress", body, [THEME / "progress-tutor.js"])


def students_page():
    path = TEACHER / "students.html"
    body = ('<header class="tc-head"><div><h1>Students &amp; groups</h1><p class="aa-sub" id="status"></p></div>'
            '<button class="btn" id="reload">Refresh</button></header>\n'
            '<div class="tc-filters"><input id="q" type="search" placeholder="Find a student">'
            '<select id="f-group"></select>'
            '<select id="f-access"><option value="">Any access</option><option value="unlocked">Course unlocked</option>'
            '<option value="locked">Locked</option><option value="paid">Paid</option></select>'
            '<select id="f-video"><option value="">Labs: any</option><option value="yes">Has Labs</option><option value="no">No Labs</option></select>'
            '<select id="f-pw"><option value="">Password: any</option><option value="starter">Still on lock&amp;key</option>'
            '<option value="own">Own password</option><option value="lockedout">Locked out</option></select>'
            '<select id="f-active"><option value="">Activity: any</option><option value="yes">Active this week</option>'
            '<option value="no">Not active this week</option></select></div>\n'
            '<div class="tc-bulk" id="bulk" hidden><b id="bulk-n"></b><select id="bulk-group"></select>'
            '<button class="btn" id="bulk-add">Add to group</button><button class="btn" id="bulk-remove">Remove from group</button>'
            '<button class="btn" id="bulk-video">Give Labs</button><button class="btn" id="bulk-unlock">Give course access</button>'
            '<input id="bulk-tix" type="number" min="1" max="500" value="5" style="width:4.5em" aria-label="Tickets">'
            '<button class="btn" id="bulk-tickets">Give tickets</button><button class="btn" id="bulk-seminars">Give a year of seminars</button>'
            '<button class="btn" id="bulk-clear">Clear selection</button></div>\n'
            '<div id="grid" class="aa-scroll"></div>\n<div class="tc-grid">'
            '<section class="tc-card"><h3>Classes &amp; cohorts</h3><p class="tc-note">A student can be in any number of classes and cohorts. '
            'Each one gets its own timetable, assignments, videos, forum and shared notebook. Tick students above, then add them.</p>'
            '<p class="aa-tools"><input id="g-name" placeholder="Name, e.g. Period 3 or 2026 batch"> '
            '<select id="g-kind"><option value="class">Class</option><option value="cohort">Cohort</option></select> '
            '<label><input type="checkbox" id="g-open"> Students can join and leave themselves</label> '
            '<button class="btn dark" id="g-add">Create</button></p>'
            '<div id="groups"></div></section>'
            '<section class="tc-card"><h3>Add a student</h3>'
            '<p class="tc-note">They sign in with their email and the starter password <b>lock&amp;key</b>, then choose their own.</p>'
            '<p class="aa-tools"><input id="add-email" type="email" placeholder="student@school.org"> '
            '<label><input id="add-unlock" type="checkbox" checked> Full course access</label> '
            '<button class="btn" id="add">Add</button></p><p class="tc-note" id="add-msg"></p></section>'
            '<section class="tc-card"><h3>Codes</h3>'
            '<p class="tc-note">One code can be shared by a whole class. Students sign in and enter it in the Store '
            '(course codes also work on the unlock page). Tickets: how many each student gets. Seminars: how many days.</p>'
            '<p class="aa-tools"><select id="code-product"><option value="course">Course</option><option value="labs">Labs</option>'
            '<option value="tickets">Tickets</option><option value="seminars">Seminars subscription</option></select> '
            '<input id="code-amount" type="number" min="1" max="3650" value="5" style="width:5em" aria-label="Tickets or days" hidden> '
            '<input id="code-note" placeholder="Class name, e.g. Period 3"> '
            '<input id="code-uses" type="number" min="1" max="500" value="30" style="width:5em"> uses '
            '<button class="btn" id="make">Make code</button></p><p class="tc-note" id="code-msg"></p>'
            '<div id="codes" class="aa-scroll"></div></section></div>')
    console(path, "Students & groups", "students", body, [THEME / "students-tutor.js"])


def topic_page(tid):
    path = teacher_topic(tid) / "index.html"
    d = path.parent
    t = C.topic(tid)
    teach = link_list(d, [("Topic deck with speaker notes", d / "slides.html"),
                          ("Classroom PowerPoint", downloads_unit(tid) / f"Topic_{tid}_Slides.pptx"),
                          ("Student view", N.target(tid, "topic"))])
    keys = link_list(d, [("Quiz key (PDF)", d / f"Topic_{tid}_Quiz_AnswerKey.pdf"),
                         ("Quiz key (Word)", d / f"Topic_{tid}_Quiz_AnswerKey.docx"),
                         ("Assignment key (PDF)", d / f"Topic_{tid}_Assignment_AnswerKey.pdf"),
                         ("Assignment key (Word)", d / f"Topic_{tid}_Assignment_AnswerKey.docx"),
                         ("Activity keys", d / "activity-keys.html")])
    rows = []
    for a in C.topic_atoms(tid):
        ad = teacher_atom(a["id"])
        ls = link_list(d, [("Solution", ad / "solution.html"), ("Solution notebook", ad / f"{a['id']}-solution.ipynb"),
                           ("Solution preview", ad / "solution-preview.html"), ("Assignment page", ad / "assign.html"),
                           ("Student notebook", ad / f"{a['id']}-student.ipynb"),
                           ("Pre-lecture post", ad / "pre-lecture-post.html"), ("Post-lecture post", ad / "post-lecture-post.html"),
                           ("Pre-lecture handout", ad / f"{a['id']}-pre-lecture-handout.docx"),
                           ("Post-lecture handout", ad / f"{a['id']}-post-lecture-handout.docx")])
        rows.append(f'<li><span class="aa-id">{a["id"]}</span>{esc(a["title"])}<span class="tc-links">{ls}</span></li>')
    body = (f'<header class="tc-head"><div><p class="tc-kicker"><a href="{rel(d, TEACHER / "resources.html")}">Resources</a></p>'
            f'<h1><span class="aa-id">{tid}</span>{esc(t["title"])}</h1></div>'
            f'<a class="btn" href="{rel(d, TEACHER / "teach.html")}?topic={tid}">Teach this topic</a></header>\n'
            f'<div class="tc-grid"><section class="tc-card"><h3>Teach</h3><span class="tc-links">{teach}</span></section>'
            f'<section class="tc-card"><h3>Answer keys</h3><span class="tc-links">{keys}</span></section></div>\n'
            f'<section class="tc-card"><h3>Skills</h3><ul class="tc-skills">{"".join(rows)}</ul></section>')
    console(path, f"{tid} {t['title']}", "resources", body)


def run():
    teach_data()
    for tid in C.order():
        topic_page(tid)
    dashboard()
    teach_page()
    schedule_page()
    classes_page()
    assignments_page()
    videos_page()
    ctf_page()
    seminars_page()
    labs_page()
    lectures_page()
    present_page()
    blog_page()
    resources_page()
    accounts_page()
    class_progress_page()
    students_page()
