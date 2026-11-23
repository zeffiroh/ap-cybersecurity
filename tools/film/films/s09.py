from kit import ROOT, after, build, chapter, clear, close, cmd, edit, files_window, save_note, say, term, wait, write

JWT = '''import base64
import hashlib
import hmac
import json
import sys

token = open(sys.argv[1]).read().split('DEMO_TOKEN = "')[1].split('"')[0]
head, body, sig = token.split(".")
pad = lambda s: s + "=" * (-len(s) % 4)
print("header: ", base64.urlsafe_b64decode(pad(head)).decode())
print("payload:", base64.urlsafe_b64decode(pad(body)).decode())
for word in open(sys.argv[2]).read().split():
    mac = hmac.new(word.encode(), f"{head}.{body}".encode(), hashlib.sha256).digest()
    if base64.urlsafe_b64encode(mac).rstrip(b"=").decode() == sig:
        print("signature secret found offline:", word)
        break
else:
    print("secret not in the wordlist")
'''

INJECT = '{"email": "admin@nimbu.shop\'--", "password": "x"}\n'
DEMO = '{"email": "demo@nimbu.shop", "password": "demo123"}\n'

ROE = """RULES OF ENGAGEMENT   NimbuMart, 16-20 Nov 2026, 09:00-18:00 IST
Authorised by: Ritu Malhotra, Head of Engineering (signed 12 Nov). Stop contact: +91 98000 11223.
IN:  nimbu.shop web app and /api; 192.0.2.10 shop-staging; 192.0.2.11 api-staging.
OUT: 192.0.2.12 pay.nimbu.shop (payment provider); people, phones, email; DoS; changing data.
MAY: scan in-scope addresses only; manual tests through a proxy; offline token checks.
MAY NOT: guess passwords on live logins; exploits that change data; full-speed scanners.
STOP AND CALL: live card data, real people's data, or signs of someone else inside.
DATA: prove with the minimum; crop screenshots; delete working files after the report.
"""

FINDINGS = """NM-01  Login bypass by SQL injection in /api/login            CVSS 9.8  fix THIS WEEK
  Request: POST /api/login  {"email": "admin@nimbu.shop'--", "password": "x"}
  Result:  200, logged in as admin without the password.
  Why:     the email is pasted into the SQL text; '-- ends the string and comments out the password check.
  Fix:     parameterised query: WHERE email = ? AND password_hash = ?
  Retest:  same request must return 401.
NM-02  Any customer can read any order (/api/orders/{id})         CVSS 6.5
  Request: GET /api/orders/2 with the demo customer's token (own orders: 3, 4).
  Result:  200, order of another customer, including a delivery address (not copied here).
  Fix:     WHERE id = ? AND customer_id = <caller>; return 404 otherwise.
NM-03  Staging tokens signed with a guessable secret; token in a public JS file   CVSS 9.1
  Found offline: HS256 secret is in a 12-word list. Anyone could sign role=admin.
  Fix:     32-byte random secret from a vault; remove the token; staging behind the VPN.
"""

scenes = [
 chapter("Opening"),
 files_window(),
 say("Welcome to Authorised testing: web, APIs and findings that get fixed. The most important word in that title is the first one. A security test and an attack can use the same tools and send the same requests. The difference is a signed letter. In India, getting into a computer system without its owner's permission can be an offence under the Information Technology Act, 2000, whatever your intentions."),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say("So this whole seminar runs on one rule: you test only what the owner has asked you, in writing, to test. Our client is NimbuMart Retail, an online shop. In this recording, the staging shop and API are a lab copy running on this machine, under their real staging names, and we use real tools: nmap, curl, jq and a few lines of Python."),
 close("files"),
 term,

 chapter("1. Authorisation and scope"),
 say("Step one: before you open a single tool, read the letter of authorisation, all of it."),
 cmd("cat engagement.txt", 6),
 after("Who authorised it, and the stop contact. In scope: the shop and two staging hosts. Out of scope: the payment host, which NimbuMart can't authorise because the payment provider runs it. Allowed: scans of in-scope addresses, manual testing, offline token checks. Not allowed: guessing live passwords, changing data, full-speed scanners. We turn that into rules of engagement we can keep beside us all week."),
 edit("rules-of-engagement.txt"),
 write(ROE, cps=42),
 save_note(),
 close("note"),
 clear,

 chapter("2. Recon, inside the lines"),
 say("Step two: recon. Scan only what's in scope, and name each host on the command line. If you scan the whole range out of habit, you hit the payment host, and you've broken the agreement before lunch on day one. nmap checks which ports are open on the two staging hosts, and nothing else."),
 cmd("nmap -Pn --open -p 8000-9000 shop-staging.nimbu.shop api-staging.nimbu.shop | grep -E 'report|open'", 8),
 after("The shop answers on 8443, and the staging API on 8080, which the bundle calls its debug port. pay.nimbu.shop is not on the command line, and it never will be. curl minus capital I asks each one for its headers only: what software says it's running."),
 cmd("curl -sI http://shop-staging.nimbu.shop:8443/ | grep -i server; curl -sI http://api-staging.nimbu.shop:8080/ | grep -i server", 3),
 after("Both say what they are: in this recording, lab copies of NimbuMart's staging servers. On a real test, version headers like these tell you what to look up. The JavaScript file saved from the staging API during recon:"),
 cmd("curl -s http://api-staging.nimbu.shop:8080/static/app.bundle.js", 3),
 after("A to-do that never got done: a login token for the demo account, left in a public file. We'll come back to it."),
 clear,

 chapter("3. Finding one: a login that trusts what you type"),
 say("Step three: the shop's login takes your email and puts it straight into a database query. When a program builds a query by pasting in text from the user, the user can change what the query means. That's SQL injection. We prove it with one request, look at the response, and stop. Here's the request body."),
 cmd("cat inject.json", 2),
 after("The email ends with a quote, which closes the string in the query, and two dashes, which make the rest of the line, the password check, a comment."),
 cmd("curl -s http://shop-staging.nimbu.shop:8443/api/login -H 'Content-Type: application/json' -d @inject.json | jq '{ok, user}'", 3),
 after("200, logged in as admin@nimbu.shop with the password x. That's the proof. We don't look around as admin, and we don't change anything: one request, one response, written down."),
 clear,

 chapter("4. Finding two: someone else's order"),
 say("Step four: log in properly as the demo customer, from the letter, and keep the token."),
 cmd("TOKEN=$(curl -s http://shop-staging.nimbu.shop:8443/api/login -H 'Content-Type: application/json' -d @demo.json | jq -r .token); echo ${TOKEN:0:40}...", 3),
 cmd("curl -s -H \"Authorization: Bearer $TOKEN\" http://shop-staging.nimbu.shop:8443/api/orders/3 | jq '{id, customer_id, items, status}'", 3),
 after("Order 3 is ours, customer 3. The question every tester asks: what if I change the number? And here the rules matter: writing down someone's address in a report is itself a data leak. So jq keeps only what proves the finding."),
 cmd("curl -s -H \"Authorization: Bearer $TOKEN\" http://shop-staging.nimbu.shop:8443/api/orders/2 | jq '{id, customer_id, has_address: (.address != null)}'", 3),
 after("Order 2 belongs to customer 2, and it came back with a delivery address. The API checked that we were logged in, not that the order was ours. That's an insecure direct object reference, an IDOR."),
 clear,

 chapter("5. Finding three: a token anyone can forge"),
 say("Step five: the staging token is a JWT: a header, a payload and a signature, separated by dots. The header and payload are only encoded, so anyone can read them. The signature stops people changing them, and with HS256 it's only as strong as the secret. This short script decodes the token and checks the signature against the twelve-word list, entirely offline. Nothing is sent to NimbuMart."),
 edit("jwt_check.py", "code", (200, 60, 1500, 940)),
 wait(4),
 close("code"),
 cmd("python3 jwt_check.py staging-bundle.js.txt wordlist.txt", 3),
 after("The secret is nimbu2026, word eleven of twelve. With it, anyone could sign a token that says role admin. We don't send one: the letter allows offline checks, and the proof is complete without it."),
 clear,

 chapter("6. Score and rank"),
 say("Step six: CVSS gives each flaw a base score from zero to ten, built from a few questions: over the network? hard to pull off? needs an account? needs a click? and the impact on confidentiality, integrity and availability. The cvss calculator, an open-source library, scores each vector from the register."),
 cmd("for v in $(cut -d, -f4 findings.csv | tail -n +2); do echo \"$v  $(cvss_calculator -n -v $v 2>/dev/null | grep -m1 'Base Score')\"; done", 4),
 after("The login bypass is 9.8: network, easy, no account, no click, full impact. The forged token is 9.1. Reading someone's order needs an account, so 6.5. Then the ranking adds two facts the score doesn't know: is it on the internet, and is anyone exploiting it. All three are internet-facing, so the order holds."),
 clear,

 chapter("7. Findings a developer can fix"),
 say("Step seven: a finding nobody can reproduce doesn't get fixed. Each one gets five parts: the exact request, what came back, why it works, the fix in code terms, and the retest."),
 edit("findings-report.txt"),
 write(FINDINGS, cps=46),
 save_note(),
 close("note"),
 clear,

 chapter("8. Retest, then tell the board"),
 say("Step eight: a fix isn't done until the same test fails. So you repeat each proof exactly, same request, same account, and expect a 401 or a 404. Then you write for the board, who need to know what could have happened to the business, what the fix costs, and what decision you need: here, approval to keep staging off the internet."),
 clear,

 chapter("9. Hand in"),
 say("Step nine: hand in. The notebook carries the rules of engagement, your recon commands, the three proofs, the scores, the findings report and the board note. Then, as the letter says, delete the working files."),
 cmd("ls -l *.txt *.json *.py", 2),
 chapter("Wrap-up"),
 say("That's an authorised test, start to finish. You read the letter first, scanned only what it named, proved three findings with one request each and no more, kept a stranger's address out of your notes, checked a token secret offline, scored and ranked the findings, and wrote them so a developer can fix them and you can prove it. Next, in Design, risk and audit, we stop these bugs before they're built. Thank you for watching."),
 wait(2),
]

LAB = (ROOT / "tools" / "film" / "nimbu_lab.py").name
build("s09-authorised-testing", scenes, host="tester-ws",
      hosts={"shop-staging.nimbu.shop": "127.0.0.10", "api-staging.nimbu.shop": "127.0.0.11"},
      files={"jwt_check.py": JWT, "inject.json": INJECT, "demo.json": DEMO},
      setup=[f"nohup python3 /film-tools/{LAB} /case/staging-bundle.js.txt >/tmp/lab.log 2>&1 &", "sleep 1"])
