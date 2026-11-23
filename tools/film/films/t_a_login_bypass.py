from kit import after, build, chapter, clear, close, cmd, edit, files_window, save_note, say, term, wait, write

INJECT = '{"email": "admin@nimbu.shop\'--", "password": "x"}\n'

FINDING = """NM-01  Login bypass by SQL injection in /api/login   (authorised test, 16-20 Nov 2026)
Request:   POST /api/login   {"email": "admin@nimbu.shop'--", "password": "x"}
Response:  200 OK, ok: true, role admin. One request, then stopped.
Why:       the server pastes the email into its SQL query inside quotes; the quote ends the
           string and the two dashes comment out the password check.
Fix:       use a parameterised query so the email is sent as data, never as SQL.
Retest:    the same request must now return 401. The finding is not closed until it does.
"""

LAB = "nimbu_lab.py"

scenes = [
 chapter("Opening"),
 files_window(),
 say("Hello, and welcome. Today you'll prove a real web vulnerability, SQL injection, on a shop that was built for practice, with written permission, and then see exactly how developers fix it. The most important word in this video is authorised. Testing someone's system without written permission is a crime, so everything here happens on our own practice shop."),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say("The setting. NimbuMart Retail, an authorised test from the sixteenth to the twentieth of November 2026. Times are Indian Standard Time. The case folder has the letter of authorisation, engagement.txt. A real tester reads it first, all of it, because it says what you may test, when, and what you must not touch."),
 close("files"),
 term,

 chapter("1. The letter of authorisation"),
 cmd("cat engagement.txt", 6),
 after("Who authorised the test, who to call to stop it, what is in scope and what is not. The payment host is out of scope. We stay inside those lines."),
 clear,

 chapter("2. Finding 1: a login that trusts what you type"),
 say("Here's the weakness. When you log in, the shop puts the email you type straight into a SQL query, inside quotes. So the query reads: find the user where email equals what you typed, and password equals what you typed. If the email ends the quote early and starts a SQL comment, with a quote and two dashes, the rest of the line, the password check, is ignored. You become whoever you named. The rule for a tester: prove it with one request, and stop. Here's the request body."),
 cmd("cat inject.json", 2),
 cmd("curl -s http://shop-staging.nimbu.shop:8443/api/login -H 'Content-Type: application/json' -d @inject.json | jq '{ok, user}'", 3),
 after("The request is a POST to /api/login, with the email admin@nimbu.shop followed by a quote and two dashes, and any password at all. The response says we're logged in, with the admin role. That's the proof. We don't browse around as admin or change anything. One request, recorded, and stop. Now write it up the way a developer can use it."),
 edit("finding-NM-01.txt"),
 write(FINDING, cps=44),
 save_note(),
 after("The request, the response, why it works, the one-line fix, and the retest: after the fix, the same request should get 401, not authorised. A finding isn't finished until the retest passes."),
 close("note"),
 clear,

 chapter("Where next"),
 say("That was one step from Seminar 9, Authorised testing: web, APIs and findings that get fixed. The full seminar has a longer video, every step at three levels, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen."),
 chapter("Wrap-up"),
 say("To recap. Get written permission, and read it. Prove a finding with the smallest possible request, then stop. Explain why it works, give the fix in one clear line, and retest. That's how a tester's work gets bugs fixed instead of filed away. Thank you for watching."),
 wait(2),
]

build("t-a-login-bypass", scenes, host="tester-ws",
      hosts={"shop-staging.nimbu.shop": "127.0.0.10", "api-staging.nimbu.shop": "127.0.0.11"},
      files={"inject.json": INJECT},
      setup=[f"nohup python3 /film-tools/{LAB} /case/staging-bundle.js.txt >/tmp/lab.log 2>&1 &", "sleep 1"])
