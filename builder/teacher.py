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
    ("videos", "Videos", TEACHER / "videos.html"),
    ("students", "Students & groups", TEACHER / "students.html"),
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
            '<section class="tc-card tc-form" id="form" hidden><h3 id="form-title">New class</h3>'
            '<label class="tc-wide">Title <input id="c-title" placeholder="Firewalls, live walkthrough"></label>'
            '<label>Topic <select id="c-topic"></select></label>'
            '<label>Starts <input type="datetime-local" id="c-starts"></label>'
            '<label>Minutes <input type="number" id="c-minutes" min="15" max="480" step="5" value="60"></label>'
            '<label>Kind <select id="c-mode"><option value="open">Open: anyone signed in joins free</option>'
            '<option value="paid">Paid: students book and pay</option><option value="request">Requested: only invited students</option></select></label>'
            '<label>Price ₹ <input type="number" id="c-inr" min="0" value="0" style="width:7em"></label>'
            '<label>Price $ <input type="number" id="c-usd" min="0" value="0" style="width:7em"></label>'
            '<label>Seats (0 = no limit) <input type="number" id="c-cap" min="0" value="0" style="width:7em"></label>'
            '<label class="tc-wide">Meeting link (Meet, Zoom…), shown only to students with a seat <input id="c-meet" placeholder="https://meet.google.com/…"></label>'
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


def videos_page():
    body = ('<header class="tc-head"><div><h1>Videos</h1><p class="aa-sub" id="status">Loading…</p></div></header>\n'
            '<section class="tc-card tc-form"><h3 id="v-head">Post a video</h3>'
            '<label class="tc-wide">YouTube link (upload it as Unlisted) <input id="v-yt" placeholder="https://youtu.be/…"></label>'
            '<label class="tc-wide">Title <input id="v-title"></label>'
            '<label>Lesson <select id="v-atom"></select></label>'
            '<label>Who sees it <select id="v-group"></select></label>'
            '<label class="tc-check"><input type="checkbox" id="v-free"> Free (no video pass needed)</label>'
            '<label class="tc-check"><input type="checkbox" id="v-email"> Email students about it</label>'
            '<label class="tc-wide">Note <textarea id="v-note" rows="2"></textarea></label>'
            '<button class="btn dark" id="v-save">Post video</button> <button class="btn" id="v-reset">Clear</button> '
            '<span class="tc-note" id="v-msg"></span></section>\n'
            '<section id="list" class="tc-grid"></section>')
    console(TEACHER / "videos.html", "Videos", "videos", body, [])


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
            '<p class="aa-tools"><select id="unit"></select> <select id="kind"><option value="">Pre and post</option>'
            '<option value="pre">Pre-lecture</option><option value="post">Post-lecture</option></select> '
            '<input id="q" type="search" placeholder="Search posts"></p>\n'
            '<div id="blog" class="tc-blog"></div>')
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
            '<select id="f-video"><option value="">Video pass: any</option><option value="yes">Has video pass</option><option value="no">No video pass</option></select>'
            '<select id="f-pw"><option value="">Password: any</option><option value="starter">Still on lock&amp;key</option>'
            '<option value="own">Own password</option><option value="lockedout">Locked out</option></select>'
            '<select id="f-active"><option value="">Activity: any</option><option value="yes">Active this week</option>'
            '<option value="no">Not active this week</option></select></div>\n'
            '<div class="tc-bulk" id="bulk" hidden><b id="bulk-n"></b><select id="bulk-group"></select>'
            '<button class="btn" id="bulk-add">Add to group</button><button class="btn" id="bulk-remove">Remove from group</button>'
            '<button class="btn" id="bulk-video">Give video pass</button><button class="btn" id="bulk-unlock">Give course access</button>'
            '<button class="btn" id="bulk-clear">Clear selection</button></div>\n'
            '<div id="grid" class="aa-scroll"></div>\n<div class="tc-grid">'
            '<section class="tc-card"><h3>Groups</h3><p class="tc-note">A group gets its own timetable, assignments and videos. '
            'Tick students above, then add them to a group.</p>'
            '<p class="aa-tools"><input id="g-name" placeholder="New group, e.g. Period 3"> <button class="btn dark" id="g-add">Create</button></p>'
            '<div id="groups"></div></section>'
            '<section class="tc-card"><h3>Add a student</h3>'
            '<p class="tc-note">They sign in with their email and the starter password <b>lock&amp;key</b>, then choose their own.</p>'
            '<p class="aa-tools"><input id="add-email" type="email" placeholder="student@school.org"> '
            '<label><input id="add-unlock" type="checkbox" checked> Full course access</label> '
            '<button class="btn" id="add">Add</button></p><p class="tc-note" id="add-msg"></p></section>'
            '<section class="tc-card"><h3>Class codes</h3>'
            '<p class="tc-note">Give a class one code. Each student signs in and enters it on the unlock page.</p>'
            '<p class="aa-tools"><input id="code-note" placeholder="Class name, e.g. Period 3"> '
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
    lectures_page()
    present_page()
    blog_page()
    resources_page()
    accounts_page()
    class_progress_page()
    students_page()
