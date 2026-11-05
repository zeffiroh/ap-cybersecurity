import json
from pathlib import Path

from . import course as C
from . import nav as N
from . import teacher
from .course import BRAND, SUBJECT
from .paths import ASSETS, DOWNLOADS, SHARED, SITE, TESTS, THEME, downloads_unit, unit_dir

VENDOR = ASSETS / "vendor"
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


LAB_PAGES = {"cyberchef": ("CyberChef", SITE / "cyberchef" / "index.html"), "linux": ("Linux lab", SITE / "linux.html"),
             "sqli": ("SQL injection lab", SITE / "sqli.html"), "shop": ("Hack the shop", SITE / "shop.html")}
TOPIC_LABS = {"1.2": ["cyberchef"], "1.3": ["cyberchef"], "3.5": ["linux"], "4.2": ["linux"], "4.3": ["linux"], "4.4": ["linux"],
              "5.1": ["sqli", "shop"], "5.2": ["linux"], "5.3": ["cyberchef", "linux"], "5.4": ["cyberchef"],
              "5.5": ["shop", "sqli"], "5.6": ["shop", "linux"]}


def lab_links(page_dir, tid):
    unit = C.topic(tid)["unit"]
    items = [(LAB_PAGES[k][0], LAB_PAGES[k][1], "") for k in TOPIC_LABS.get(tid, [])]
    items.append((f"Unit {unit} CTF challenges", SITE / "ctf.html", f"#u{unit}"))
    out = [f'<a href="{rel(page_dir, p, q)}">{esc(label)}</a>' for label, p, q in items]
    return f'<div class="aa-links">{"".join(out)}</div>'


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
            f'<h2>Hands-on labs</h2>\n{lab_links(d, tid)}\n'
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
            f'<p><a class="btn" href="{rel(path.parent, SITE / "community.html")}#lectures">Live classes: join, book or request a 1:1</a></p>\n'
            + theme_assets(path.parent, ["calendar.css"], ["calendar.js"]))
    emit(path, N.shell(path, "", body, cls="aa-wide"))


LECTURES = ('<section id="cm-lectures" hidden><p class="aa-sub" id="sx-status">Loading…</p>\n<div id="sx-classes">\n'
            '<h2>Live classes coming up</h2>\n<div id="sx-upcoming" class="sx-classes"></div>\n'
            '<h2>Request a 1:1 class</h2>\n<p class="aa-sub">Pick a free time from your teacher\'s availability, or suggest your own. '
            'When your teacher schedules it, confirm it with tickets.</p>\n'
            '<div id="sx-slots" class="sx-slots"></div>\n<div class="sx-form">'
            '<label>Topic <select id="sx-topic"></select></label>'
            '<label>Chosen time <input id="sx-slot-label" readonly placeholder="Pick a time above"></label>'
            '<label>Or other times that suit you <input id="sx-times" placeholder="e.g. weekends after 4 pm IST"></label>'
            '<label class="sx-wide">What do you want to cover? <textarea id="sx-note" rows="3"></textarea></label>'
            '<button class="btn dark" id="sx-request">Send request</button> <span id="sx-req-msg" class="sx-note"></span></div>\n'
            '<div id="sx-requests"></div>\n'
            '<h2>Recordings</h2>\n<div id="sx-recordings"></div>\n'
            '<p class="sx-note">Live classes run on Jitsi. Its toolbar has a shared whiteboard (Excalidraw) under '
            '<b>More actions &rsaquo; Show whiteboard</b>, so the class can draw diagrams together.</p>\n</div></section>\n')


def classes_page():
    path = SITE / "classes.html"
    target = rel(path.parent, SITE / "community.html") + "#lectures"
    emit(path, N.shell(path, "Live classes", f'<p>Live classes have moved to <a href="{target}">Classes &amp; forum</a>.</p>\n'
                                              f'<script>location.replace("{target}");</script>'))


def community_page():
    path = SITE / "community.html"
    body = ('<h1>Classes &amp; forum</h1>\n<p class="aa-sub" id="cm-msg"></p>\n<div id="cm-app" class="cm-app">'
            '<nav id="cm-side" class="cm-side" aria-label="Spaces"></nav><section id="cm-main" class="cm-main">'
            '<div id="cm-head" class="cm-head"></div>'
            '<div id="cm-compose" class="sx-form" hidden><label class="sx-wide">Title <input id="cm-title" maxlength="200"></label>'
            '<label class="sx-wide">Post <textarea id="cm-body" rows="6" placeholder="Ask, share or explain. Put code between `backticks`."></textarea></label>'
            '<button class="btn dark" id="cm-post">Post</button> <button class="btn" id="cm-cancel">Cancel</button></div>'
            '<div id="cm-list"></div><div id="cm-thread" hidden></div></section>' + LECTURES + '</div>\n'
            + theme_assets(path.parent, [], ["student-extras.js", "community.js"]))
    emit(path, N.shell(path, "", body, cls="aa-wide"))


def linux_page():
    path = SITE / "linux.html"
    r = lambda p: rel(path.parent, p)
    body = ('<h1>Linux lab</h1>\n<p class="aa-sub">A real Linux computer running inside your browser. Nothing to install, '
            'and nothing you do here can harm your own computer.</p>\n<div id="lx-app" class="lx-app">'
            '<section class="lx-term"><div class="lx-bar"><button class="btn dark" id="lx-start">Start Linux</button>'
            '<button class="btn" id="lx-setup" disabled>Create the lab files</button><button class="btn" id="lx-reset">Restart</button>'
            '<span id="lx-status" class="sx-note">Press Start. The first start downloads about 12 MB.</span></div>'
            '<div id="lx-screen" class="lx-screen"><p class="lx-hint">Press <b>Start Linux</b>, then click here and type.</p></div>'
            f'<p class="sx-note">Runs <a href="{r(ASSETS / "linux" / "NOTICE.txt")}">v86 and Buildroot Linux</a>, open source. '
            'There is no internet inside the lab: nmap, curl, wget, tshark, dig, nslookup, whois, ping, traceroute, nc, ssh, openssl, nikto and gobuster reach a recorded '
            'copy of a case network instead.</p></section>'
            '<section id="lx-labs" class="lx-labs"></section></div>\n'
            '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@xterm/xterm@5.5.0/css/xterm.css">\n'
            '<script src="https://cdn.jsdelivr.net/npm/@xterm/xterm@5.5.0/lib/xterm.min.js" defer></script>\n'
            + theme_assets(path.parent, ["runbook.css", "labview.css"], ["linux-vm.js", "labkit.js", "linux-lab.js"]))
    emit(path, N.shell(path, "", body, cls="aa-wide"))


def certificate_page():
    path = SITE / "certificate.html"
    body = ('<div id="ce-app"><div class="ce-tools"><a href="seminars.html">&larr; Seminars</a>'
            '<button class="btn dark" id="ce-print" hidden>Print or save as PDF</button></div>\n'
            '<div id="ce-box"><p class="sx-empty">Loading…</p></div>\n'
            '<form id="ce-verify" class="ce-verify"><label>Check a certificate number <input id="ce-id" placeholder="AAP-XXXX-XXXX" '
            'autocomplete="off"></label><button class="btn">Check</button></form></div>\n'
            + theme_assets(path.parent, [], ["certificate.js"]))
    emit(path, N.shell(path, "", body, cls="aa-wide"))


def ctf_page():
    path = SITE / "ctf.html"
    r = lambda p: rel(path.parent, p)
    body = ('<h1>Capture the flag</h1>\n<p class="aa-sub">Each puzzle hides a flag like <code>aayat{...}</code>. Find it, paste it in, '
            'score points for yourself and your class.</p>\n'
            '<div id="ctf-app" class="ctf-app"><section class="ctf-main"><p class="sx-note" id="ctf-msg">Loading…</p>'
            '<div id="ctf-stats" class="ctf-stats" aria-live="polite"></div>'
            '<div class="ctf-filters" role="search"><label class="ctf-search"><span class="ctf-sr">Search puzzles</span>'
            '<input id="ctf-q" type="search" placeholder="Search puzzles  ( / )" autocomplete="off" spellcheck="false"></label>'
            '<label><span class="ctf-sr">Unit</span><select id="ctf-f-unit"></select></label>'
            '<label><span class="ctf-sr">Type</span><select id="ctf-f-type"></select></label>'
            '<span class="ctf-seg" role="group" aria-label="Show"><button type="button" data-status="all">All</button>'
            '<button type="button" data-status="unsolved">Unsolved</button><button type="button" data-status="solved">Solved</button></span></div>'
            '<nav id="ctf-units" class="ctf-units" aria-label="Units"></nav><div id="ctf-list"></div></section>'
            '<aside class="ctf-side"><h2>Leaderboard</h2><p id="ctf-me" class="sx-note"></p>'
            '<label class="sx-note">Show <select id="ctf-space"><option value="all">Everyone</option></select></label>'
            '<div id="ctf-board"></div><h2>Your tools</h2><div class="aa-links ctf-tools">'
            f'<a href="{r(SITE / "cyberchef" / "index.html")}" target="_blank" rel="noopener">CyberChef</a>'
            f'<a href="{r(SITE / "linux.html")}">Linux lab</a><a href="{r(SITE / "sqli.html")}">SQL injection lab</a>'
            f'<a href="{r(SITE / "shop.html")}">Hack the shop</a></div>'
            '<p class="sx-note">Everything here is a practice target built for this course. Never try these techniques on a real '
            'site or account without written permission.</p></aside></div>\n'
            '<dialog id="ctf-dlg" class="ctf-dlg" aria-labelledby="ctf-dlg-title"></dialog>\n'
            f'<script src="{r(ASSETS / "ctf" / "challenges.js")}" defer></script>\n'
            + theme_assets(path.parent, ["ctf.css"], ["labkit.js", "ctf.js"]))
    emit(path, N.shell(path, "", body, cls="aa-wide"))


def sqli_page():
    path = SITE / "sqli.html"
    r = lambda p: rel(path.parent, p)
    body = ('<h1>SQL injection lab</h1>\n<p class="aa-sub">A pretend staff portal backed by a real SQL database running in your browser. '
            'Break it, then fix it. Nothing outside this page is touched.</p>\n'
            '<div id="sq-app" class="lab-app"><section class="lab-main">'
            '<div class="sq-site"><div class="sq-brand">Northwind Staff Portal</div>'
            '<div class="sq-panel"><h3>Sign in</h3><label>Username <input id="sq-user" autocomplete="off" spellcheck="false"></label>'
            '<label>Password <input id="sq-pass" type="text" autocomplete="off" spellcheck="false"></label>'
            '<button class="btn dark" id="sq-go">Sign in</button><div id="sq-login-out" class="sq-out"></div></div>'
            '<div class="sq-panel"><h3>Product search</h3><label>Search <input id="sq-q" autocomplete="off" spellcheck="false" '
            'placeholder="e.g. cable"></label><button class="btn dark" id="sq-search">Search</button><div id="sq-search-out" class="sq-out"></div></div>'
            '<div class="sq-panel"><h3>Choose a username</h3><label>Username <input id="sq-check" autocomplete="off" spellcheck="false" '
            'placeholder="e.g. alice"></label><button class="btn dark" id="sq-check-go">Is it free?</button><div id="sq-check-out" class="sq-out"></div></div>'
            '<div class="sq-panel"><h3>Admin vault</h3><label>Admin PIN <input id="sq-pin" inputmode="numeric" maxlength="6" autocomplete="off"></label>'
            '<button class="btn dark" id="sq-vault-go">Open</button><div id="sq-vault-out" class="sq-out"></div></div>'
            '</div><h3>What the server ran</h3><pre id="sq-log" class="sq-log">Nothing yet.</pre>'
            '<h3>Fix it</h3><p class="sx-note">Rewrite the login query so user input can never change the SQL. Put <code>?</code> where '
            'each value goes; the lab passes the username, then the password, as separate values.</p>'
            '<textarea id="sq-fix" class="sq-fix" rows="3" spellcheck="false"></textarea>'
            '<p><button class="btn dark" id="sq-test">Test my fix</button> <button class="btn" id="sq-reset">Reset the database</button></p>'
            '<div id="sq-test-out" class="sq-out"></div></section>'
            '<aside class="lab-side"><h2>Missions</h2><div id="sq-missions"></div>'
            '<details class="lab-cheat"><summary>SQL you might need</summary><pre>\'   ends a piece of text\n'
            '--  comment: ignore the rest of the line\nOR 1=1   always true\nUNION SELECT a, b FROM t\n'
            '    add rows from another table\nsqlite_master   lists every table\nsubstr(text, 1, 1)   the first letter</pre></details></aside></div>\n'
            f'<script src="{r(VENDOR / "sqljs-1.13.0" / "sql-wasm.js")}" defer></script>\n'
            f'<script src="{r(ASSETS / "ctf" / "lab-flags.js")}" defer></script>\n'
            + theme_assets(path.parent, [], ["labkit.js", "sqli-lab.js"]))
    emit(path, N.shell(path, "", body, cls="aa-wide"))


def shop_page():
    path = SITE / "shop.html"
    r = lambda p: rel(path.parent, p)
    body = ('<h1>Hack the shop</h1>\n<p class="aa-sub">NimbuMart is a deliberately insecure online shop. Its web server is simulated '
            'inside this page, so you can attack it freely. Use the address bar and the developer tools under it, as in a real browser.</p>\n'
            '<div id="sh-app" class="lab-app"><section class="lab-main">'
            '<div class="sh-browser"><div class="sh-bar"><button class="btn" id="sh-back" title="Back">&larr;</button>'
            '<button class="btn" id="sh-reload" title="Reload">&#8635;</button><span class="sh-host">https://nimbu.shop</span>'
            '<input id="sh-url" spellcheck="false" autocomplete="off" aria-label="Address"><button class="btn dark" id="sh-goto">Go</button></div>'
            '<div id="sh-page" class="sh-page"></div></div>'
            '<div class="sh-dev"><div class="sh-tabs" role="tablist"><button data-tab="net" class="on">Network</button>'
            '<button data-tab="repeat">Edit and resend</button><button data-tab="store">Storage</button><button data-tab="src">Sources</button>'
            '</div><div id="sh-devbody" class="sh-devbody"></div></div></section>'
            '<aside class="lab-side"><h2>Challenges</h2><p class="sx-note">Each one gives a flag for the CTF board.</p>'
            '<div id="sh-missions"></div><p><button class="btn" id="sh-wipe">Reset the shop</button></p></aside></div>\n'
            f'<script src="{r(VENDOR / "sqljs-1.13.0" / "sql-wasm.js")}" defer></script>\n'
            f'<script src="{r(ASSETS / "ctf" / "lab-flags.js")}" defer></script>\n'
            + theme_assets(path.parent, [], ["labkit.js", "shop-lab.js"]))
    emit(path, N.shell(path, "", body, cls="aa-wide"))


def store_page():
    path = SITE / "store.html"
    body = ('<h1>Store</h1>\n<p class="aa-sub">Each part is sold on its own. In India you pay what you want (some have a minimum); '
            'international prices are on Gumroad. Use the email you sign in with.</p>\n'
            '<div id="st-me" class="st-me"></div>\n<div id="st-products" class="st-grid"></div>\n'
            '<h2 id="redeem">Have a code?</h2>\n<div class="sx-form"><label>Code <input id="st-code" autocomplete="off" spellcheck="false" '
            'placeholder="e.g. LABS-ABCD-EFGH"></label><button class="btn dark" id="st-redeem">Redeem</button> '
            '<span id="st-msg" class="sx-note"></span></div>\n'
            '<h2 id="tickets-history">Your tickets</h2>\n<div id="st-history"><p class="sx-empty">Sign in to see your tickets.</p></div>\n'
            + theme_assets(path.parent, [], ["store.js"]))
    emit(path, N.shell(path, "", body, cls="aa-wide"))


def labs_page():
    path = SITE / "labs.html"
    r = lambda p: rel(path.parent, p)
    def card(kick, title, p, d, more="", q=""):
        return (f'<a class="lv-card" href="{r(p) + q}"><span class="lv-ck">{esc(kick)}</span><b>{esc(title)}</b>'
                f'<span class="lv-cs">{esc(d)}</span><span class="lv-cp">{esc(more or "Open")} &rarr;</span></a>')
    attack = (card("Attack the app", "SQL injection lab", SITE / "sqli.html", "Break a staff login with SQL injection, then fix the query so it can't happen again.", "Beginner · 30 min")
              + card("Attack the app", "Hack the shop", SITE / "shop.html", "A deliberately insecure web shop with ten vulnerabilities to find, each worth a CTF flag.", "Intermediate · 1 to 2 hours"))
    ctf = card("Capture the flag", "CTF board", SITE / "ctf.html", "Puzzles for every unit, points and a class leaderboard. Runbooks and attack labs hide flags too.", "All levels")
    tools = (card("Tool", "Linux lab", SITE / "linux.html", "A real Linux computer in your browser, with 13 step-by-step exercises.", "Start with steps 1 to 5")
             + card("Tool", "JupyterLab", SITE / "lab" / "lab" / "index.html", "Every code book, runnable Python, nothing to install.")
             + card("Tool", "CyberChef", SITE / "cyberchef" / "index.html", "Decode, encrypt, hash and analyse data in a recipe of steps."))
    start = ('<section class="lv-start" aria-labelledby="lv-start-h"><div class="lv-sk">Start here</div><h2 id="lv-start-h">New to hands-on labs? Do these three in order</h2>'
             '<ol class="lv-path">'
             f'<li><a href="{r(SITE / "linux.html")}"><b>Learn the commands in the Linux lab</b><span>Steps 1 to 5: look around, permissions, hashing, a log hunt. About 20 minutes.</span></a></li>'
             f'<li><a href="{r(SITE / "sqli.html")}"><b>Your first attack: the SQL injection lab</b><span>Get past a login, then fix it. About 30 minutes.</span></a></li>'
             f'<li><a id="lv-firstcase" href="{r(SITE / "notebook.html")}#nb-cases-h"><b>Your first incident runbook</b><span>A guided case with a briefing, hints and answer checks. About an hour.</span></a></li>'
             '</ol></section>')
    jump = ('<nav class="lv-jump" aria-label="Kinds of lab"><a href="#lv-guided">Guided labs</a><a href="#lv-runbooks">Incident runbooks</a>'
            '<a href="#lv-attack">Attack the app</a><a href="#lv-ctf">CTF</a><a href="#lv-tools">Tools</a></nav>')
    skills = "".join(f'<li><span class="aa-id">{a["id"]}</span><a href="{r(N.lab_page(a))}">{esc(N.window_name(a, "lab"))}</a></li>'
                     for a in C.atom_order() if N.has_lab(a))
    body = ('<div id="lb-app"><section id="lb-index"><h1>Labs</h1>\n<p class="aa-sub">The hands-on side of the course: real tools, '
            'real attacks on practice targets, and incident cases. Sold separately from the course.</p>\n<div id="lb-access"></div>\n'
            f'{start}\n{jump}\n'
            '<h2 id="lv-guided">Guided labs</h2>\n<p class="lv-gd">Step-by-step labs and notebooks from your teacher. Each step has a Done tick, copy buttons and hints.</p>\n'
            '<div id="lb-premium"><p class="sx-empty">Loading…</p></div>\n'
            f'<details class="lv-skills"><summary>Skill labs, one for each lesson</summary><ul class="aa-list lb-skills">{skills}</ul></details>\n'
            '<h2 id="lv-runbooks">Incident runbooks</h2>\n<p class="lv-gd">Work a real case in the Notebook: real Linux, Python and network tools on the case evidence, '
            'with a briefing, a step tracker, hints and answer checks.</p>\n<div id="lv-cases"><p class="sx-empty">Loading cases…</p></div>\n'
            f'<h2 id="lv-attack">Attack-the-app labs</h2>\n<div class="lv-grid">{attack}</div>\n'
            f'<h2 id="lv-ctf">Capture the flag</h2>\n<div class="lv-grid">{ctf}</div>\n'
            f'<h2 id="lv-tools">Tools</h2>\n<div class="lv-grid">{tools}</div>\n'
            f'<p class="sx-note">Lesson videos come with Labs too: <a href="{r(SITE / "videos.html")}">Video lessons</a>.</p></section>\n'
            '<section id="lb-view" hidden></section></div>\n'
            + theme_assets(path.parent, ["runbook.css", "labview.css"], ["linux-vm.js", "labkit.js", "labs.js"]))
    emit(path, N.shell(path, "", body, cls="aa-wide"))


def seminars_page():
    path = SITE / "seminars.html"
    body = ('<div id="sm-app"><section id="sm-index"><h1>Seminars</h1>\n<p class="aa-sub">Complete, intensive recorded seminars. '
            'Unlock one with tickets, or subscribe to all of them.</p>\n<div id="sm-me" class="st-me"></div>\n'
            '<div id="sm-list" class="sm-grid"><p class="sx-empty">Loading…</p></div></section>\n'
            '<section id="sm-view" hidden></section></div>\n'
            + theme_assets(path.parent, [], ["seminars.js"]))
    emit(path, N.shell(path, "", body, cls="aa-wide"))


def videos_page():
    path = SITE / "videos.html"
    body = ('<header class="vl-head"><div><h1>Video lessons</h1>\n<p class="aa-sub">Short videos from your teacher, one for each lesson, '
            'in course order.</p></div><p class="vl-stats" id="vl-stats"></p></header>\n'
            '<div id="sx-videos-page"><div id="sx-pass"></div><div id="sx-videos"><div class="vl-empty"><b>Loading videos…</b></div></div></div>\n'
            + theme_assets(path.parent, [], ["student-extras.js"]))
    emit(path, N.shell(path, "", body, cls="aa-wide"))


def notebook_page():
    path = SITE / "notebook.html"
    body = ('<div id="nb-app">\n<section id="nb-index" hidden>'
            '<header class="nb-hero"><h1>Notebook</h1>\n'
            '<p class="aa-sub">Runbooks and notes: step-by-step instructions, Linux commands and Python in one document, with every output saved. '
            'Everything runs here in your browser. Linux cells come with Labs.</p></header>\n'
            '<div class="nb-starts">'
            '<article class="nb-start nb-feature"><div class="nb-sk">Incident response</div><h3>Work a real case</h3>'
            '<p>Incident runbooks for every unit: a hacked web shop, a phishing email that ends in ransomware, an insider '
            'stealing designs, a leaked cloud key. You use real Linux, Python, '
            '<code>nmap</code>, <code>curl</code>, <code>tshark</code> and <code>dig</code> on a recorded copy of each case network.</p>'
            '<button class="btn" id="nb-runbook">Choose a case &darr;</button></article>'
            '<article class="nb-start"><div class="nb-sk">Lesson</div><h3>Lesson notebook</h3>'
            '<p>Your notes for one lesson, or start from its code book.</p>'
            '<select id="nb-lesson" aria-label="Lesson"></select>'
            '<div class="nb-sbtns"><button class="btn dark" id="nb-open">Open my notes</button>'
            '<button class="btn" id="nb-openbook">With the code book</button></div></article>'
            '<article class="nb-start"><div class="nb-sk">Your own</div><h3>Blank notebook</h3>'
            '<p>Notes, Linux and Python cells, in any order you like.</p>'
            '<div class="nb-sbtns"><button class="btn dark" id="nb-new">Create</button>'
            '<a class="btn" href="lab/lab/index.html" target="_blank" rel="noopener">Full JupyterLab</a></div></article></div>\n'
            '<h2>My notebooks</h2>\n<div id="nb-mine"></div>\n'
            '<h2 id="nb-cases-h">Incident runbooks</h2>\n<div id="nb-cases" class="nb-cases"><p class="nb-empty">Loading cases…</p></div>\n'
            '</section>\n<section id="nb-editor" hidden><p class="nb-crumb" id="nb-crumb"></p>\n'
            '<input id="nb-title" class="nb-title" aria-label="Notebook title">\n'
            '<div class="nb-tools"><div class="nb-grp" role="group" aria-label="Add a cell"><span class="nb-gl">Add</span>'
            '<button class="btn" id="nb-addmd">Notes</button><button class="btn" id="nb-addsh">Linux</button>'
            '<button class="btn" id="nb-addpy">Python</button></div>'
            '<button class="btn dark" id="nb-runall">&#9654; Run all</button>'
            '<div class="nb-grp"><button class="btn" id="nb-book">Load the code book</button>'
            '<button class="btn" id="nb-dl">Download .ipynb</button><button class="btn" id="nb-import">Import .ipynb</button>'
            '<input type="file" id="nb-file" accept=".ipynb,application/json" hidden>'
            '<a class="btn" id="nb-lab" target="_blank" rel="noopener">JupyterLab</a></div>'
            '<span id="nb-status" class="nb-status"></span></div>\n'
            '<div id="nb-cells"></div>\n'
            '<div class="nb-addrow"><span>Add a cell</span><button class="btn" data-add="md">+ Notes</button>'
            '<button class="btn" data-add="sh">+ Linux</button><button class="btn" data-add="py">+ Python</button></div>\n'
            '<p class="nb-help"><b>Keys:</b> Shift+Enter or Ctrl+Enter runs a cell, Tab indents, Ctrl+/ comments a line. '
            'Linux cells share one shell, so <code>cd</code> and variables carry on to the next cell. '
            'Network tools in Linux cells: <code>nmap curl wget tshark dig nslookup host whois ping traceroute nc ssh openssl nikto gobuster</code>. '
            'Write <code>- [ ] step</code> in notes for a checklist, <code>&gt; Hint: text</code> for a hidden hint, and '
            '<code>?&gt; Question :: sha256:&lt;hash&gt;</code> for a question with a checked answer. Double-click a note to edit it.</p>\n'
            '</section>\n</div>\n'
            + theme_assets(path.parent, ["runbook.css", "playbook.css", "tools.css"], ["linux-vm.js", "labkit.js", "tools.js", "tool-logsearch.js", "playbook.js", "notebook.js"]))
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
    community_page()
    linux_page()
    store_page()
    labs_page()
    seminars_page()
    certificate_page()
    ctf_page()
    sqli_page()
    shop_page()
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
