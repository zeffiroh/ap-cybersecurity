import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEM = ROOT / "source" / "seminars"


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip("\n") + "\n", encoding="utf-8", newline="\n")


def copy(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def hosts(rows):
    return "\n".join("|".join(str(x) for x in r) for r in rows)


def folder(name, about, files, steps, net=None):
    d = SEM / name
    if d.exists():
        for p in d.iterdir():
            if p.is_file():
                p.unlink()
            elif p.name in ("files", "net"):
                shutil.rmtree(p)
    d.mkdir(parents=True, exist_ok=True)
    for rel, val in files.items():
        if isinstance(val, Path):
            copy(val, d / "files" / rel)
        else:
            write(d / "files" / rel, val)
    for rel, text in (net or {}).items():
        write(d / "net" / rel, text)
    for fname, text in steps.items():
        write(d / fname, text)
    (d / "seminar.json").write_text(json.dumps(about, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return d


def sim_phish():
    F = SEM / "f-evidence-notes-handoffs" / "files"
    alerts = json.loads((F / "alerts.json").read_text(encoding="utf-8"))
    rows = alerts if isinstance(alerts, list) else alerts.get("alerts", [])
    early = [a for a in rows if a["time"] < "2026-11-02T09:41"]
    late = [a for a in rows if a["time"] >= "2026-11-02T09:41"]
    files = {
        "README.txt": """
Kestrel Logistics, a freight company. Monday 2 November 2026. All times are UTC (India is UTC+5:30).
Proxy times are Unix epoch seconds; turn them into UTC before you write them down.

hr-pc07      10.20.0.14   HR laptop (priya.nair)
fin-pc02     10.20.0.15   Finance laptop (dev.kapoor)
acct-pc03    10.20.0.16   Accounts laptop
fs01         10.20.1.10   file server with the HR, Finance and Ops shares
mail         10.20.1.5    the company mail server
proxy        10.20.1.3    the web proxy every laptop uses

It is 09:16. Dev Kapoor in Finance has just pressed Report phishing on an email about an overdue invoice.
Helpdesk ticket 88213 opened by itself. Nobody has looked at it yet.

What you have:
  invoice.eml           the reported message (it's in Mail too)
  mail.log              the mail server's delivery log
  proxy.log             the web proxy log (epoch times)
  process.csv           the EDR process list from hr-pc07 and fin-pc02
  eventlogs/Security.jsonl  the Windows Security log from hr-pc07
  alerts.json           the SIEM alerts so far (they're in Tickets too)
  ticket-88213.txt      the helpdesk ticket
""",
        "invoice.eml": F / "invoice.eml",
        "mail.log": F / "mail.log",
        "proxy.log": F / "proxy.log",
        "process.csv": F / "process.csv",
        "ticket-88213.txt": F / "ticket-88213.txt",
        "share_listing.txt": F / "share_listing.txt",
        "eventlogs/Security.jsonl": (SEM / "x01-phish-to-containment" / "files" / "eventlogs" / "Security.jsonl").read_text(encoding="utf-8"),
        "alerts.json": json.dumps(early, indent=1),
        "alerts-fs01.json": json.dumps(late, indent=1),
    }
    net = {
        "hosts.txt": hosts([
            ["10.20.0.1", "gw.kestrel.lan", 53, "tcp", "domain", "dnsmasq 2.89", 0, ""],
            ["10.20.0.2", "sw1-core.kestrel.lan", 22, "tcp", "ssh", "OpenSSH 8.9", 0, ""],
            ["10.20.1.3", "proxy.kestrel.lan", 3128, "tcp", "http-proxy", "Squid http proxy 5.7", 0, ""],
            ["10.20.1.5", "mail.kestrel.lan", 25, "tcp", "smtp", "Postfix smtpd", 0, ""],
            ["10.20.1.5", "mail.kestrel.lan", 993, "tcp", "ssl/imap", "Dovecot imapd", 0, ""],
            ["10.20.1.10", "fs01.kestrel.lan", 445, "tcp", "microsoft-ds", "Windows Server 2022 SMB", 0, ""],
            ["10.20.0.14", "hr-pc07.kestrel.lan", 445, "tcp", "microsoft-ds?", "", 0, ""],
            ["10.20.0.14", "hr-pc07.kestrel.lan", 3389, "tcp", "ms-wbt-server", "Microsoft Terminal Services", 0, ""],
            ["10.20.0.15", "fin-pc02.kestrel.lan", 445, "tcp", "microsoft-ds?", "", 0, ""],
            ["10.20.0.16", "acct-pc03.kestrel.lan", 445, "tcp", "microsoft-ds?", "", 0, ""],
            ["203.0.113.45", "kestrel-logistlcs.com", 80, "tcp", "http", "nginx 1.18.0", 0, "Invoices"],
            ["os", "10.20.1.10", "Windows", "Windows Server 2022"],
            ["os", "10.20.0.14", "Windows", "Windows 11"],
        ]),
        "dns.txt": """
SERVER 10.20.0.1
A gw.kestrel.lan 10.20.0.1
A proxy.kestrel.lan 10.20.1.3
A mail.kestrel.lan 10.20.1.5
A fs01.kestrel.lan 10.20.1.10
A hr-pc07.kestrel.lan 10.20.0.14
A fin-pc02.kestrel.lan 10.20.0.15
A acct-pc03.kestrel.lan 10.20.0.16
A kestrel-logistlcs.com 203.0.113.45
A cdn-update-check.net 198.51.100.61
""",
    }
    steps = {
        "01-the-report.md": """
## 1. The report

It's Monday 2 November 2026 at **Kestrel Logistics**, 09:16 UTC. Dev Kapoor in Finance has just reported an email as phishing: message **4A1F21C02**, an overdue invoice. Read it, then the mail server's log, to find out who else got it.

- [ ] Who really sent it? Read the From and Return-Path, and the domain, letter by letter
- [ ] How many people received message 4A1F21C02, and who?

> Hint: In mail.log, `nrcpt=` is the number of recipients, and each `to=<...>` line is one mailbox.

?> Which domain sent the invoice? :: kestrel-logistlcs.com

?> How many people received message 4A1F21C02? :: 3
""",
        "01-the-report.sh": """
cd ~/case
grep -E '^(From|Return-Path|Subject):' invoice.eml
echo ---
grep 4A1F21C02 mail.log
""",
        "02-who-opened-it.md": """
## 2. Who opened it

Receiving a phishing email is not an incident. **Opening** it is. The web proxy logs every download. Search it for the look-alike domain, and turn the epoch times into UTC.

- [ ] Which internal address downloaded INV-30412.docm, and when?
- [ ] Did anyone else try? Did it work?

> Hint: `TCP_MISS/200` means the file was fetched. `TCP_DENIED/403` means the proxy blocked it: the domain was added to the blocklist at 09:18.

?> Which internal address downloaded INV-30412.docm? :: 10.20.0.14

?> Did fin-pc02 get the document? (yes or no) :: no
""",
        "02-who-opened-it.sh": """
cd ~/case
grep logistlcs proxy.log
echo ---
grep logistlcs proxy.log | while read t ms ip code size method url rest; do echo "$(date -u -d @${t%.*} '+%F %T') $ip $code $url"; done
""",
        "03-what-ran.md": """
## 3. What ran on hr-pc07

10.20.0.14 is hr-pc07, Priya Nair's HR laptop. The EDR process list shows every program that started and which program started it. Follow the chain from Word.

- [ ] What did Word start?
- [ ] What did that start, and what was left running?

> Hint: Follow the `ppid` column: each process's parent is the row whose `pid` matches it.

?> Which program did Word start? :: cmd.exe

?> Which program was left running from C:\\Users\\Public? :: svchost-upd.exe
""",
        "03-what-ran.sh": """
cd ~/case
grep hr-pc07 process.csv
""",
        "04-contain-and-escalate.md": """
## 4. Contain, then escalate

You know enough: hr-pc07 opened a macro document, and malware is running on it. **Contain first, investigate second.** In the Hacker Room, isolate hr-pc07 from the network (Remote desktop, or shut its switch port in the Server room), end the malware's process, and escalate alert AL-2203 with a note that says what you found and what you did.

If nobody contains it, at 09:41 the malware walks the file server and renames the HR share's files to `.kestrel-locked`. `share_listing.txt` shows what that looks like.

- [ ] Isolate hr-pc07 before 09:41
- [ ] End svchost-upd.exe
- [ ] Escalate AL-2203: what fired, what you found, what you did, what you don't know yet

> Hint: Don't switch the laptop off: memory holds evidence. Isolating keeps it running but cut off.

?> Which alert should you escalate? (its ID) :: AL-2203
""",
    }
    sim = {
        "title": "Phish to containment",
        "role": "SOC analyst, Monday morning",
        "start": "2026-11-02T09:16:00Z",
        "speed": 1,
        "pins": ["mail", "files", "terminal", "chat", "tickets", "tool-siem", "rdp", "rack", "notes"],
        "first": True,
        "cast": {"lead": {"name": "Meera Iyer", "role": "SOC lead"}, "it": {"name": "Arjun", "role": "IT helpdesk"}, "dev": {"name": "Dev Kapoor", "role": "Finance"}},
        "story": "It's 09:16 on Monday 2 November 2026 at Kestrel Logistics, a freight company. You're the SOC analyst on the morning shift.\n\nDev Kapoor in Finance has just pressed Report phishing on an email about an overdue invoice. It went to three people. Your job: find out who opened it, stop it spreading, and hand the incident on with a note the next person can act on.\n\nThe clock on the taskbar is the story clock. It runs at real speed. Something bad happens at 09:41 if nobody acts.",
        "hold": ["alerts-fs01.json", "share_listing.txt"],
        "events": [
            {"at": 1, "chat": "lead", "text": "Morning. Dev Kapoor just reported a suspicious invoice email, message 4A1F21C02. Ticket 88213 opened itself but it says nothing useful. It's yours."},
            {"at": 6, "chat": "lead", "text": "The message is in Mail, the evidence in Files, the alerts in Tickets. Find who got it, who opened it, and stop it spreading. Ask me if you're stuck."},
            {"at": 120, "chat": "it", "text": "Hi, Priya in HR says her laptop has been slow since she opened an invoice this morning. Shall I just restart it for her?"},
            {"after": "who", "chat": "lead", "text": "Good. So it was hr-pc07. What ran after Word opened the document? The Remote desktop has the EDR process list."},
            {"after": "contain", "chat": "it", "text": "hr-pc07 just dropped off the network. I'll tell Priya not to touch it."},
            {"after": "contain", "wait": 5, "chat": "lead", "text": "Nice. Now end the malware's process and escalate AL-2203 in Tickets with what you know."},
            {"at": 1500, "unless": "contain", "release": ["alerts-fs01.json", "share_listing.txt"], "chat": "lead", "text": "CRITICAL: fs01's HR share is being renamed to .kestrel-locked by priya.nair's account. Contain hr-pc07 right now!"},
            {"after": "escalate", "chat": "lead", "text": "Got your escalation. The incident lead takes it from here. Send me a one-line summary in chat when you're ready."},
        ],
        "replies": [
            {"match": "restart|reboot|turn (it )?off|shut ?down", "who": "it", "text": "OK. Should I? You tell me. Restarting would wipe what's in memory."},
            {"match": "don.?t|do not|leave it|isolat|unplug|cable|disconnect", "who": "it", "text": "Got it. I'll leave it switched on and won't touch it. Isolate it from your side when you're ready."},
        ],
        "objectives": [
            {"id": "sender", "text": "Read the reported email. Which domain really sent it?", "ask": "Sender domain", "answer": ["kestrel-logistlcs.com"], "points": 10, "hint": "Open Mail. Read the From address letter by letter: logistlcs, with an L where the i should be."},
            {"id": "count", "text": "How many people received message 4A1F21C02?", "ask": "Number of recipients", "answer": ["3", "three"], "points": 10, "hint": "Open mail.log in Files and look for nrcpt= on the 4A1F21C02 lines, or run: grep 4A1F21C02 ~/case/mail.log"},
            {"id": "who", "text": "Which internal address downloaded the invoice document?", "ask": "IP address", "answer": ["10.20.0.14"], "points": 15, "hint": "Search proxy.log for logistlcs: grep logistlcs ~/case/proxy.log. TCP_MISS/200 means the file came through."},
            {"id": "denied", "text": "Did fin-pc02 (10.20.0.15) get the document too?", "ask": "yes or no", "answer": ["no"], "points": 10, "after": "who", "hint": "Its line in proxy.log says TCP_DENIED/403: the proxy blocked it after the domain was added to the blocklist at 09:18."},
            {"id": "chain", "text": "On hr-pc07, which program did Word start?", "ask": "Program name", "answer": ["cmd.exe", "cmd"], "points": 10, "after": "who", "hint": "Remote desktop, hr-pc07, Task Manager. Find WINWORD.EXE's PID, then the row whose Parent is that PID."},
            {"id": "contain", "text": "Contain hr-pc07: isolate it, or shut its switch port", "points": 20, "after": "who",
             "on": {"any": [{"event": "rdp.isolate", "host": "hr-pc07", "isolated": True}, {"event": "rack.port", "ip": "10.20.0.14", "shut": True}]},
             "hint": "Remote desktop, open hr-pc07, press Isolate from the network. Or Server room, hr-pc07, Shut its ports. Don't switch it off: memory holds evidence."},
            {"id": "intime", "text": "Bonus: contain it before the malware reaches the file server at 09:41", "with": "contain", "within": 1500, "points": 15},
            {"id": "kill", "text": "End the malware's process on hr-pc07", "points": 10, "after": "chain", "on": {"event": "rdp.endtask", "host": "hr-pc07", "image": "svchost-upd"}, "hint": "Task Manager on hr-pc07: svchost-upd.exe running from C:\\Users\\Public. A real svchost.exe lives in System32."},
            {"id": "escalate", "text": "Escalate alert AL-2203 in Tickets with a note", "points": 15, "after": "contain", "on": {"event": "ticket.escalate", "id": "~AL-220[34]"}, "hint": "Tickets, AL-2203, write what fired, what you found, what you did and what you don't know yet, then press Escalate."},
            {"id": "summary", "text": "Send the SOC lead a one-line summary in chat that names the host", "points": 5, "after": "escalate", "on": {"event": "chat.send", "text": "~hr-pc07|10\\.20\\.0\\.14"}, "hint": "For example: hr-pc07 opened INV-30412.docm at 09:02, isolated at 09:30, malware ended, AL-2203 escalated."},
        ],
        "debrief": "A strong run takes about twenty minutes. Read the email and spot the look-alike domain. Use mail.log to see it went to three people. Search proxy.log to see that only hr-pc07 (10.20.0.14) downloaded the document at 09:02, and that fin-pc02's try at 09:20 was blocked. Follow the process chain: Word, cmd.exe, a hidden PowerShell, then svchost-upd.exe running from C:\\Users\\Public, which is not where Windows keeps svchost.\n\nThen contain before you dig further. Isolating hr-pc07, without switching it off, stops the 09:41 encryption of the HR share and keeps the memory for the incident team. End the malware's process, escalate AL-2203 with a note that says what fired, what you found, what you did and what you don't know yet (did anyone else open it, was anything copied out), and tell your lead in one line.\n\nThe usual mistakes: restarting the laptop (evidence gone), spending twenty minutes on the low alerts, or escalating with \"probably malware ???\".",
        "pass": 70,
    }
    about = {
        "title": "Simulation: Phish to containment",
        "kicker": "Simulation",
        "summary": "A reported phishing email, a ticking clock and a laptop running malware. Find who opened it, contain it before 09:41, and hand it on.",
        "units": [1, 4],
        "level": "Beginner",
        "minutes": 35,
        "order": 300,
        "tools": ["Mail", "Tickets", "Remote desktop", "Server room", "Terminal"],
        "seminar_id": None,
        "published": True,
        "sim": sim,
        "script": {
            "intro": "Hello, and welcome to a simulation. For the next half hour you're the SOC analyst on the Monday morning shift at Kestrel Logistics. A phishing email has been reported, and somewhere on the network, malware is already running. Watch how I work it from the first message to containment.",
            "steps": [
                {"say": "It's 09:16. The SOC lead hands me the case in chat. First, the email itself. In Mail, the From line says Kestrel Logistics Accounts, but read the domain letter by letter: kestrel-logistlcs, with an L instead of an i. Then mail.log in a terminal: message 4A1F21C02 went to three mailboxes.",
                 "after": "Three people received it. That's three possible victims, and receiving an email isn't the incident. Opening it is. So the next question is who downloaded the document."},
                {"say": "The web proxy logs every download. I search proxy.log for the look-alike domain. The times are Unix epoch seconds, so I convert them to UTC.",
                 "after": "One success: 10.20.0.14, hr-pc07, Priya Nair's HR laptop, downloaded INV-30412.docm at 09:02. fin-pc02 tried at 09:20 and was denied, because the domain went on the blocklist at 09:18. So we have one infected machine, not three."},
                {"say": "Now what ran on hr-pc07. The EDR process list shows each program and its parent. I follow the chain from Word.",
                 "after": "Word started cmd.exe, which started a hidden PowerShell running a script from C:\\Users\\Public, which started svchost-upd.exe from the same folder. The real svchost lives in System32, so this is the malware, and it's still running. Meanwhile IT asks in chat whether to restart the laptop. The answer is no: restarting wipes memory, which is evidence."},
                {"say": "Contain first, investigate second. In the Remote desktop I open hr-pc07 and press Isolate from the network. The laptop stays on, but it can't reach the file server any more. Then Task Manager, End task on svchost-upd.exe. Then Tickets: alert AL-2203, a note with what fired, what I found, what I did and what I don't know yet, and Escalate.",
                 "after": "Contained before 09:41, so the HR share is safe, which is the bonus objective. The debrief shows the score, every action with its story time, and what a strong run looks like. Download it: it's part of your hand-in."},
            ],
            "outro": "That's a real morning in a SOC, compressed: read carefully, find who actually opened it, follow the process chain, contain without destroying evidence, and hand on a note someone can act on. Now it's your turn. Open the simulation in the Hacker Room and try to beat 09:41.",
        },
    }
    return folder("x01-phish-to-containment", about, files, steps, net)


def tree(src, prefix=""):
    out = {}
    for p in sorted(src.rglob("*")):
        if p.is_file():
            out[prefix + p.relative_to(src).as_posix()] = p
    return out


def sim_pentest():
    S9 = SEM / "s09-authorised-testing" / "files"
    files = tree(S9)
    files["README.txt"] = """
NimbuMart Retail, an authorised test, Monday 16 to Friday 20 November 2026. Times IST (UTC+5:30); the taskbar clock shows UTC.

You are the tester. It is Monday morning, the first hour of the test window.

engagement.txt          the letter of authorisation: read it first, all of it
staging-bundle.js.txt   a JavaScript file saved from the staging API during recon
wordlist.txt            a short list of common and company-themed passwords
findings.csv            your findings register

The shop runs in your browser: the Web proxy talks to it. nmap reaches a recorded copy of the staging network.
"""
    net = {"hosts.txt": (S9 / "net" / "hosts.txt").read_text(encoding="utf-8"), "dns.txt": (S9 / "net" / "dns.txt").read_text(encoding="utf-8")}
    steps = {
        "01-the-letter-first.md": """
## 1. The letter first

A test without written permission is an attack. Read **engagement.txt** to the end before you touch anything: what's in scope, what's out, the window, and when to stop.

- [ ] When does the window close?
- [ ] Which address must you never touch, and why?

?> Which address is out of scope? :: 192.0.2.12
""",
        "01-the-letter-first.sh": "cd ~/case\ncat engagement.txt",
        "02-recon-inside-the-lines.md": """
## 2. Recon inside the lines

Scan only the two staging hosts, by address, never the whole range: 192.0.2.12 sits in the same range and belongs to the payment provider.

- [ ] Which services and versions run on each host?
- [ ] Which one looks like it shouldn't be reachable?

> Hint: `nmap -sV 192.0.2.10 192.0.2.11` names each address. `192.0.2.0/24` would include the out-of-scope payment host.

?> Which port does the staging debug API listen on? :: 8080
""",
        "02-recon-inside-the-lines.sh": "nmap -sV 192.0.2.10 192.0.2.11",
        "03-one-request-then-stop.md": """
## 3. One request, then stop

The login puts the email straight into a SQL query. Prove it with **one** POST to /api/login in the Web proxy, with the email `admin@nimbu.shop'--` and any password. Record the status and the role, and stop.

- [ ] The request, the status and the role you got
- [ ] Why it works, and the one-line fix
- [ ] The retest you'll ask for

> Hint: `'--` closes the quote and comments out the password check. The fix is a parameterised query.

?> Which HTTP status does the injected login get? :: 200
""",
        "04-report-and-tell.md": """
## 4. Report it the same day

A critical finding doesn't wait for the final report. Write it up in the report builder (what, where, why it works, the fix, the retest) and tell the client's contact the same day, as the letter asks.

- [ ] Finding 1 written, with a fix a developer can follow
- [ ] The client contact told

?> Who is the client's stop contact? :: Ritu Malhotra
""",
    }
    sim = {
        "title": "Authorised pen test",
        "role": "Penetration tester, day one",
        "start": "2026-11-16T03:30:00Z",
        "speed": 1,
        "pins": ["files", "terminal", "tool-proxy", "tool-report", "chat", "notes", "rack"],
        "first": True,
        "cast": {"lead": {"name": "Kiran Rao", "role": "Test lead"}, "client": {"name": "Ritu Malhotra", "role": "NimbuMart, Head of Engineering"}},
        "story": "It's 09:00 IST on Monday 16 November 2026, the first hour of an authorised test of NimbuMart Retail's online shop. The taskbar clock shows UTC (03:30).\n\nYour test lead has set you up. The letter of authorisation is in the case folder. Read it before you do anything: it says what you may test, what you must not touch, and when to stop.\n\nYour goal today: map the two staging hosts, prove the login bypass the developers are worried about with as little as possible, and report it the same day. One mistake ends a career here: touching a system you weren't allowed to.",
        "events": [
            {"at": 1, "chat": "lead", "text": "Morning. Window's open until Friday 18:00 IST. Letter's in ~/case/engagement.txt. Read all of it before you run anything, then map the staging hosts."},
            {"at": 8, "chat": "client", "text": "Hi, Ritu from NimbuMart. I'm your stop contact this week. Call me first if anything looks like a real break-in."},
            {"on": {"event": "terminal.command", "cmd": "~192\\.0\\.2\\.(12|0/)|pay\\.nimbu"}, "chat": "client", "text": "Our payment provider just called. Someone from your address scanned pay.nimbu.shop. That host is out of scope. Please stop and explain."},
            {"after": "scan", "chat": "lead", "text": "Good. Port 8080 on the API host is a debug service that shouldn't face anyone. Note it. Now the login: one request in the Web proxy, then stop."},
            {"after": "bypass", "chat": "lead", "text": "That's a critical. Write it up in the report builder now, and tell Ritu today. Don't wait for Friday."},
            {"after": "tell", "chat": "client", "text": "Thank you for telling us straight away. The developers will switch to a parameterised query today. Please retest tomorrow morning."},
        ],
        "replies": [
            {"match": "sorry|mistake|out of scope|explain", "who": "client", "text": "Thank you for owning it. Write it in your notes with the time, and stick to the two staging hosts from now on."},
        ],
        "objectives": [
            {"id": "window", "text": "Read the letter. When does the test window close?", "ask": "Day and time", "answer": ["~fri|20"], "points": 10, "hint": "engagement.txt, the Window line: Friday 20 November 2026, 18:00 IST."},
            {"id": "scope", "text": "Which address is out of scope?", "ask": "IP address", "answer": ["192.0.2.12"], "points": 10, "hint": "OUT OF SCOPE: 192.0.2.12, pay.nimbu.shop, run by the payment provider."},
            {"id": "clean", "text": "Stay in scope all day: never touch pay.nimbu.shop or scan the whole range", "keep": True, "points": 20, "fail": {"event": "terminal.command", "cmd": "~192\\.0\\.2\\.(12|0/)|pay\\.nimbu"}},
            {"id": "scan", "text": "Scan the two staging hosts with nmap, by address", "after": "scope", "points": 10, "on": {"event": "terminal.command", "cmd": "~nmap.*192\\.0\\.2\\.1[01]"}, "hint": "In a terminal: nmap -sV 192.0.2.10 192.0.2.11"},
            {"id": "debug", "text": "Which port is the staging debug API on?", "ask": "Port", "answer": ["8080"], "after": "scan", "points": 10, "hint": "The nmap output for 192.0.2.11: Node.js Express on 8080, labelled debug."},
            {"id": "bypass", "text": "Prove the login bypass with one request in the Web proxy", "after": "scope", "points": 20, "on": {"event": "tool.result", "tool": "proxy", "data.s": 200, "data.b": "~'\\s*--"}, "hint": "Web proxy: POST /api/login with the body {\"email\": \"admin@nimbu.shop'--\", \"password\": \"x\"} and Content-Type: application/json."},
            {"id": "role", "text": "Which role did the injected login give you?", "ask": "Role", "answer": ["admin", "administrator"], "after": "bypass", "points": 10, "hint": "Read the response body in the Web proxy."},
            {"id": "write", "text": "Write finding 1 in the report builder", "after": "bypass", "points": 10, "on": {"event": "tool.result", "tool": "report"}, "hint": "Start, Report builder. Say what, where, why it works, the fix (a parameterised query) and the retest (expect 401)."},
            {"id": "tell", "text": "Tell the client contact about the critical finding today", "after": "bypass", "points": 10, "on": {"event": "chat.send", "text": "~sql|inject|login|bypass|critical"}, "hint": "In Team chat, one or two lines for Ritu: what you found, how bad it is, the fix, and that you'll retest."},
        ],
        "debrief": "A strong first day starts with reading the whole letter: the window closes Friday 20 November at 18:00 IST, and 192.0.2.12 (pay.nimbu.shop) is out of scope because NimbuMart can't authorise testing its payment provider. That's why you scan the two staging hosts by address, not the /24 range.\n\nThe scan shows a debug API on 192.0.2.11:8080 that shouldn't be reachable: note it. Then one request proves the login bypass: status 200 and the admin role. Stop there. Write it up with the cause (the email goes into the SQL text), a fix a developer can follow (a parameterised query) and the retest (the same request should get 401), and tell the client contact the same day.\n\nThe mistake that ends careers is the one this simulation watches for all day: touching what you weren't allowed to.",
        "pass": 70,
    }
    about = {
        "title": "Simulation: Authorised pen test",
        "kicker": "Simulation",
        "summary": "Day one of an authorised web test: read the letter, scan only what you may, prove a login bypass with one request, and report it the same day.",
        "units": [6], "level": "Intermediate", "minutes": 40, "order": 302,
        "tools": ["Terminal (nmap)", "Web proxy", "Report builder"], "seminar_id": None, "published": True, "sim": sim,
        "script": {
            "intro": "Hello, and welcome to a simulation. Today you're a penetration tester on the first morning of an authorised test. The skill that matters most isn't hacking. It's staying inside the lines you were given. Let's see how a professional does day one.",
            "steps": [
                {"say": "Before anything, the letter of authorisation. I read all of it. The window runs to Friday at 18:00 IST. Two staging hosts are in scope, and 192.0.2.12, the payment page, is out, because NimbuMart can't give permission for a system its payment provider runs.",
                 "after": "Notice the stop conditions too: real card data, real people's data, or signs someone else is already inside. If I see any of those, I stop and call Ritu."},
                {"say": "Recon. I scan the two staging hosts by address, not the whole range, because the range includes the payment host.",
                 "after": "SSH and the shop on .10, and on .11 the API on 443 and a debug service on 8080 that shouldn't face anyone. That goes in my notes as a finding to check."},
                {"say": "Now the login. One request in the Web proxy: a POST to /api/login with the email admin@nimbu.shop, a quote, and two dashes.",
                 "after": "Status 200, and the role is admin. That's the proof. I stop here: I don't browse as admin or change anything."},
                {"say": "A critical finding doesn't wait for Friday. I write it in the report builder: what, where, why it works, the fix, a parameterised query, and the retest, which should get 401. Then I tell Ritu in chat.",
                 "after": "The debrief shows every action with its time, and it checks one thing all day: did I ever touch the payment host? That's the habit this simulation is really teaching."},
            ],
            "outro": "Read the letter, scan by address, prove with one request, stop, report the same day. Now open the simulation and try your own first morning.",
        },
    }
    return folder("x02-authorised-pen-test", about, files, steps, net)


def sim_office():
    files = {
        "README.txt": """
Saffron Dental Care, Kochi. Saturday 14 November 2026. The clinic is closed today. All times UTC (India is UTC+5:30).

You are the IT contractor on the monthly security visit. The practice manager, Anita Thomas, asked for three things:
  1. Find anything on the network that shouldn't be there.
  2. Close the doors that don't need to be open.
  3. Keep the waiting-room Wi-Fi away from patient records.

gw.saffron.lan      10.40.0.1    the internet router and firewall
sw1.saffron.lan     10.40.0.2    the switch in the comms cupboard
nas01.saffron.lan   10.40.0.10   file server: patient records, X-ray images
recep-pc            10.40.0.21   reception PC
dr-pc               10.40.0.22   dentist's PC
xray-pc             10.40.0.23   X-ray workstation
printer             10.40.0.30   reception printer
cam-nvr             10.40.0.40   CCTV recorder
Guest Wi-Fi         10.40.1.0/24 the waiting room network

What you have:
  inventory.csv        the clinic's own list of its devices
  switch-ports.txt     which wall socket each switch port goes to, and whether it is live
  dhcp-leases.txt      the router's list of addresses it has handed out
  conn.csv             a week of connection counts from the router
  firewall-rules.txt   the router's rules today
""",
        "inventory.csv": """
ip,name,type,owner,location,notes
10.40.0.1,gw.saffron.lan,router,IT contractor,comms cupboard,
10.40.0.2,sw1.saffron.lan,switch,IT contractor,comms cupboard,
10.40.0.10,nas01.saffron.lan,file server,Dr Menon,comms cupboard,patient records and X-rays
10.40.0.21,recep-pc,PC,reception,front desk,
10.40.0.22,dr-pc,PC,Dr Menon,surgery 1,
10.40.0.23,xray-pc,PC,Dr Menon,X-ray room,
10.40.0.30,printer,printer,reception,front desk,
10.40.0.40,cam-nvr,CCTV recorder,practice manager,comms cupboard,installer set it up in 2023
""",
        "switch-ports.txt": """
sw1.saffron.lan port map, checked 14 Nov 2026 08:40 UTC

port  wall socket  room                     device               link
1     -            comms cupboard           gw.saffron.lan       up
2     -            comms cupboard           nas01.saffron.lan    up
3     -            comms cupboard           cam-nvr              up
4     R1           reception                recep-pc             up
5     R2           reception                printer              up
6     S1           surgery 1                dr-pc                up
7     C3           consult room 3           (nothing)            up     room closed for building work since October
8     X1           X-ray room               xray-pc              up
9     W1           waiting room             10.40.0.99           up
10    S2           surgery 2                (nothing)            down
11    ST1          store room               (nothing)            up     nobody works in the store room
12    -            comms cupboard           uplink to Wi-Fi AP   up
""",
        "dhcp-leases.txt": """
gw.saffron.lan DHCP leases, 14 Nov 2026 08:41 UTC

address      mac                vendor             hostname        first seen
10.40.0.21   3c:52:82:11:20:01  HP                 recep-pc        2024-03-02
10.40.0.22   3c:52:82:11:20:02  HP                 dr-pc           2024-03-02
10.40.0.23   3c:52:82:11:20:03  HP                 xray-pc         2024-03-02
10.40.0.30   00:1e:0b:44:10:30  HP                 printer         2024-03-02
10.40.0.40   bc:ad:28:90:00:40  Hikvision          cam-nvr         2023-06-10
10.40.0.99   98:da:c4:7e:12:99  TP-Link            TL-WR840N       2026-11-09
10.40.1.17   f2:11:0a:9c:41:17  (random)           Galaxy-A14      2026-11-13
10.40.1.23   6a:3e:11:02:9b:23  (random)           iPhone          2026-11-13
""",
        "conn.csv": """
src,dst,dport,proto,count
10.40.0.21,10.40.0.10,445,tcp,1820
10.40.0.22,10.40.0.10,445,tcp,2211
10.40.0.23,10.40.0.10,445,tcp,904
10.40.0.23,203.0.113.80,443,tcp,96
10.40.0.21,198.51.100.25,443,tcp,410
10.40.0.40,203.0.113.200,80,tcp,288
10.40.1.17,198.51.100.25,443,tcp,77
10.40.1.23,198.51.100.25,443,tcp,140
10.40.1.17,10.40.0.10,445,tcp,6
10.40.1.23,10.40.0.30,9100,tcp,2
10.40.1.17,10.40.0.1,53,udp,51
10.40.0.99,10.40.0.10,445,tcp,31
""",
        "firewall-rules.txt": """
zone clinic 10.40.0.0/24
zone guest 10.40.1.0/24
zone internet any

allow any clinic -> any
allow any guest -> any
default deny
""",
    }
    net = {
        "hosts.txt": hosts([
            ["10.40.0.1", "gw.saffron.lan", 53, "udp", "domain", "dnsmasq 2.86", 0, ""],
            ["10.40.0.1", "gw.saffron.lan", 443, "tcp", "ssl/http", "router admin", 0, "Saffron router"],
            ["10.40.0.2", "sw1.saffron.lan", 22, "tcp", "ssh", "OpenSSH 7.4", 0, ""],
            ["10.40.0.2", "sw1.saffron.lan", 23, "tcp", "telnet", "switch telnet", 0, ""],
            ["10.40.0.10", "nas01.saffron.lan", 445, "tcp", "microsoft-ds", "Samba smbd 4.17", 0, ""],
            ["10.40.0.10", "nas01.saffron.lan", 5000, "tcp", "http", "NAS admin page", 0, "NAS login"],
            ["10.40.0.21", "recep-pc", 445, "tcp", "microsoft-ds?", "", 0, ""],
            ["10.40.0.22", "dr-pc", 445, "tcp", "microsoft-ds?", "", 0, ""],
            ["10.40.0.23", "xray-pc", 104, "tcp", "dicom", "DICOM", 0, ""],
            ["10.40.0.30", "printer.saffron.lan", 23, "tcp", "telnet", "printer telnet", 0, ""],
            ["10.40.0.30", "printer.saffron.lan", 9100, "tcp", "jetdirect", "", 0, ""],
            ["10.40.0.40", "cam-nvr.saffron.lan", 80, "tcp", "http", "NVR web", 0, "Recorder login (admin/12345)"],
            ["10.40.0.40", "cam-nvr.saffron.lan", 554, "tcp", "rtsp", "", 0, ""],
            ["10.40.0.99", "TL-WR840N", 53, "tcp", "domain", "dnsmasq", 0, ""],
            ["10.40.0.99", "TL-WR840N", 80, "tcp", "http", "TP-Link router web", 0, "TL-WR840N Wireless N Router"],
            ["os", "10.40.0.99", "Linux", "embedded Linux (TP-Link router)"],
        ]),
        "dns.txt": "SERVER 10.40.0.1\nA gw.saffron.lan 10.40.0.1\nA sw1.saffron.lan 10.40.0.2\nA nas01.saffron.lan 10.40.0.10\nA printer.saffron.lan 10.40.0.30\nA cam-nvr.saffron.lan 10.40.0.40",
    }
    steps = {
        "01-what-is-on-the-network.md": """
## 1. What is on the network

Start by finding out what's really there, then compare it with the clinic's own list. Anything on the network and not on the list is the first thing to explain.

- [ ] Scan 10.40.0.0/24
- [ ] Which address isn't in inventory.csv? What is it, and since when?

> Hint: dhcp-leases.txt shows the vendor and the day each device first appeared. switch-ports.txt shows which wall socket it's plugged into.

?> Which address is on the network but not in the inventory? :: 10.40.0.99
""",
        "01-what-is-on-the-network.sh": "nmap -sV 10.40.0.0/24\necho ---\ncd ~/case\ngrep 10.40.0.99 dhcp-leases.txt switch-ports.txt",
        "02-close-the-doors.md": """
## 2. Close the doors

Telnet sends passwords in plain text: nothing should still offer it. Live wall sockets in empty rooms are an open invitation. A recorder with its installer's password is a camera anyone can watch.

- [ ] Which devices offer Telnet (port 23)?
- [ ] Which switch ports are live in rooms nobody uses?
- [ ] Which device still has a default password?

?> How many switch ports are live in rooms nobody uses? :: 2
""",
        "02-close-the-doors.sh": "cd ~/case\ngrep -i 'up' switch-ports.txt | grep -i 'nothing'",
        "03-keep-guests-away-from-patients.md": """
## 3. Keep the guests away from the patient records

Today the router lets the waiting-room Wi-Fi reach everything. conn.csv shows a guest phone talking to the NAS on 445. Rewrite the rules so guests reach the internet (web and DNS) and nothing inside.

- [ ] Guests: DNS to the router, web to the internet, nothing else
- [ ] The clinic keeps working: PCs to the NAS, the X-ray PC to its cloud
- [ ] Run your rules in the Firewall program and check the guest-to-NAS flow is denied

> Hint: Rules are read top to bottom. Put the guest rules first, and end with `default deny`.

?> How many guest connections to the NAS are in conn.csv? :: 6
""",
    }
    sim = {
        "title": "Secure a small office",
        "role": "IT contractor, monthly security visit",
        "start": "2026-11-14T08:45:00Z",
        "speed": 1,
        "pins": ["files", "terminal", "rack", "tool-firewall", "chat", "notes"],
        "first": True,
        "cast": {"lead": {"name": "Anita Thomas", "role": "Practice manager"}, "dr": {"name": "Dr Menon", "role": "Dentist and owner"}},
        "story": "It's Saturday 14 November 2026 at Saffron Dental Care in Kochi. The clinic is closed, and you're the IT contractor on the monthly security visit.\n\nThe practice manager wants three things: find anything on the network that shouldn't be there, close the doors that don't need to be open, and keep the waiting-room Wi-Fi away from patient records.\n\nYou have a terminal with nmap, the Server room (the clinic's rack: shut a port, tag a device, export the inventory) and the Firewall program with the router's rules.",
        "events": [
            {"at": 1, "chat": "lead", "text": "Morning! The clinic's all yours till lunch. The device list and the switch map are in the case folder. Shout if you find anything odd."},
            {"after": "rogue", "chat": "lead", "text": "A TP-Link in the waiting room? Oh. One of the receptionists said the Wi-Fi was weak by the chairs. I think her husband brought a router in last Monday."},
            {"after": "cut", "chat": "dr", "text": "Anita told me. Thank you for catching it. Please make sure the waiting-room Wi-Fi can't see our records either."},
            {"after": "fw", "chat": "lead", "text": "Brilliant. Can you send me the updated asset list for our files before you go?"},
        ],
        "replies": [
            {"match": "telnet|password|camera|cctv|recorder", "who": "lead", "text": "The camera man set it up in 2023 and nobody's touched it since. Please fix whatever needs fixing and tell me what to ask him."},
        ],
        "objectives": [
            {"id": "scan", "text": "Scan the clinic network with nmap", "points": 10, "on": {"event": "terminal.command", "cmd": "~nmap.*10\\.40\\.0\\."}, "hint": "In a terminal: nmap -sV 10.40.0.0/24"},
            {"id": "rogue", "text": "Which address is on the network but not in the clinic's inventory?", "ask": "IP address", "answer": ["10.40.0.99"], "points": 15, "hint": "Compare the scan (or dhcp-leases.txt) with inventory.csv. One device appeared on 9 November."},
            {"id": "what", "text": "What kind of device is it?", "ask": "Device", "answer": ["~access ?point|router|wi-?fi|tp-?link|wr840"], "after": "rogue", "points": 10, "hint": "dhcp-leases.txt says TP-Link TL-WR840N; its web page title says Wireless N Router. It's plugged into wall socket W1 in the waiting room."},
            {"id": "cut", "text": "Cut the rogue device off at the switch", "after": "rogue", "points": 15, "on": {"event": "rack.port", "ip": "10.40.0.99", "shut": True}, "hint": "Server room, click 10.40.0.99, Shut its ports."},
            {"id": "telnet1", "text": "Turn off Telnet on the switch", "points": 10, "on": {"event": "rack.port", "ip": "10.40.0.2", "port": "23", "shut": True}, "hint": "Server room, sw1, port 23: Shut."},
            {"id": "telnet2", "text": "Turn off Telnet on the printer", "points": 10, "on": {"event": "rack.port", "ip": "10.40.0.30", "port": "23", "shut": True}, "hint": "Server room, the printer, port 23: Shut."},
            {"id": "rooms", "text": "How many switch ports are live in rooms nobody uses?", "ask": "Number", "answer": ["2", "two"], "points": 10, "hint": "switch-ports.txt: consult room 3 (port 7) and the store room (port 11) are up with nothing plugged in."},
            {"id": "cam", "text": "Tag the CCTV recorder for hardening: it still has its installer's password", "points": 10, "on": {"event": "rack.tag", "ip": "10.40.0.40", "tag": "patch"}, "hint": "Server room, cam-nvr, Review: Needs patching or hardening. Its login page title gives away admin/12345."},
            {"id": "fw", "text": "Rewrite the router rules: guests reach the internet only, and run them in the Firewall program", "points": 20, "on": {"event": "tool.result", "tool": "firewall", "data.rules": "~^(?![\\s\\S]*allow\\s+any\\s+guest\\s*->\\s*any\\b)[\\s\\S]*guest\\s*->\\s*internet"}, "hint": "Replace 'allow any guest -> any' with: allow udp guest -> 10.40.0.1:53, allow tcp guest -> internet:80,443, deny any guest -> clinic. Keep 'allow any clinic -> any' and 'default deny'."},
            {"id": "export", "text": "Export the asset inventory for the practice manager", "after": "fw", "points": 5, "on": {"event": "rack.export"}, "hint": "Server room, Export CSV."},
        ],
        "debrief": "A strong visit starts with a scan of 10.40.0.0/24 compared against the clinic's own list. 10.40.0.99 isn't on it: dhcp-leases.txt says a TP-Link TL-WR840N appeared on 9 November, and switch-ports.txt puts it on wall socket W1 in the waiting room. A home router plugged into a clinic network is a back door anyone in the waiting room can use, and conn.csv shows it already talking to the NAS. Cut it off at the switch first, then explain kindly to the person who brought it.\n\nThen close the doors: Telnet on the switch and the printer, the two live sockets in empty rooms (consult room 3 and the store room), and the CCTV recorder still using its installer's password. Finally, the rule that matters most for a clinic: guests get DNS and the web, never the patient records. Run the rules in the Firewall program and check the guest-to-NAS flow is now denied, then hand the manager the updated inventory.",
        "pass": 70,
    }
    about = {
        "title": "Simulation: Secure a small office",
        "kicker": "Simulation",
        "summary": "A dental clinic's monthly security visit: find the rogue access point, close the open doors, and keep the waiting-room Wi-Fi away from patient records.",
        "units": [2, 3], "level": "Beginner", "minutes": 35, "order": 303,
        "tools": ["Terminal (nmap)", "Server room", "Firewall and segmentation"], "seminar_id": None, "published": True, "sim": sim,
        "script": {
            "intro": "Hello, and welcome to a simulation. Today you're the IT contractor for a small dental clinic. No attacker, no alarm, just a Saturday visit. And that's exactly when most real problems are found: the ones nobody noticed.",
            "steps": [
                {"say": "First, what's really on the network. I scan 10.40.0.0/24 and compare it with the clinic's own inventory.",
                 "after": "Everything matches except 10.40.0.99. The DHCP leases say it's a TP-Link router that first appeared on Monday, and the switch map puts it on the wall socket in the waiting room. Somebody plugged in a home router to boost the Wi-Fi."},
                {"say": "I cut it off at the switch from the Server room, then close the other doors: Telnet on the switch and on the printer, and I tag the CCTV recorder, which still has its installer's password.",
                 "after": "Two live sockets in empty rooms go on the list for the manager too: consult room 3 and the store room."},
                {"say": "The big one: the waiting-room Wi-Fi can reach everything, and a guest phone has been talking to the NAS. I rewrite the router rules: guests get DNS and the web, nothing inside, and default deny at the end.",
                 "after": "The Firewall program replays a week of real connections against my rules. The guest-to-NAS flow is now denied and the clinic's own traffic still works. I export the updated inventory for the manager."},
            ],
            "outro": "Know what's there, close what doesn't need to be open, separate guests from patient data, and leave the owner a clear list. Now try your own visit.",
        },
    }
    return folder("x03-secure-a-small-office", about, files, steps, net)


def sim_ransom():
    S5 = SEM / "s05-incident-response" / "files"
    files = tree(S5)
    files["README.txt"] = (S5 / "README.txt").read_text(encoding="utf-8") + "\nIn this simulation it is 00:31 UTC on Saturday 7 November. You've just been called in as the on-call incident responder.\n"
    files["alerts-night.json"] = json.dumps([
        {"id": "GA-701", "time": "2026-11-06T22:44:10Z", "severity": "medium", "rule": "VPN login for an account without MFA", "host": "vpn01", "user": "s.kale", "src": "203.0.113.140", "detail": "First login from this address. MFA not enrolled."},
        {"id": "GA-702", "time": "2026-11-06T23:05:45Z", "severity": "high", "rule": "Process opened lsass with full access", "host": "eng-ws14", "user": "s.kale", "detail": "rundll32.exe opened lsass.exe with access 0x1FFFFF"},
        {"id": "GA-703", "time": "2026-11-06T23:20:09Z", "severity": "high", "rule": "New service installed on a server", "host": "fs02", "user": "adm.rjoshi", "detail": "Service WinUpdSvc installed"},
        {"id": "GA-704", "time": "2026-11-06T23:41:01Z", "severity": "critical", "rule": "Shadow copies deleted", "host": "fs02", "user": "SYSTEM", "detail": "vssadmin delete shadows /all /quiet"},
        {"id": "GA-705", "time": "2026-11-06T23:42:10Z", "severity": "critical", "rule": "Mass file rename on a file share", "host": "fs02", "user": "SYSTEM", "detail": "D:\\Shares files renamed to *.garnet-locked"},
    ], indent=1)
    net = {
        "hosts.txt": hosts([
            ["10.50.0.1", "vpn01.garnet.lan", 443, "tcp", "ssl/http", "VPN gateway", 0, "Garnet remote access"],
            ["10.50.1.10", "dc01.garnet.lan", 389, "tcp", "ldap", "Active Directory LDAP", 0, ""],
            ["10.50.1.12", "fs02.garnet.lan", 445, "tcp", "microsoft-ds", "Windows Server 2022 SMB", 0, ""],
            ["10.50.2.14", "eng-ws14.garnet.lan", 3389, "tcp", "ms-wbt-server", "Microsoft Terminal Services", 0, ""],
            ["10.50.2.14", "eng-ws14.garnet.lan", 445, "tcp", "microsoft-ds?", "", 0, ""],
        ]),
        "dns.txt": "SERVER 10.50.1.10\nA vpn01.garnet.lan 10.50.0.1\nA dc01.garnet.lan 10.50.1.10\nA fs02.garnet.lan 10.50.1.12\nA eng-ws14.garnet.lan 10.50.2.14",
    }
    steps = {
        "01-what-is-happening.md": """
## 1. What is happening right now

It's 00:31 UTC on Saturday 7 November at Garnet Precision Engineering. The helpdesk says CAD files won't open and every folder has RESTORE-FILES.txt. First: what is encrypting, where, and is it still running?

- [ ] Which program is encrypting, on which server, which folder?
- [ ] Which alerts in the queue tell the story?

?> Which program is encrypting the shares? :: locker.exe
""",
        "01-what-is-happening.sh": "cd ~/case\ngrep -i locker process.csv",
        "02-how-did-they-get-in.md": """
## 2. How did they get in?

Containment needs to know the way in, or you'll cut one door and leave another open.

- [ ] Which account came in over the VPN, from where, and did it have MFA?
- [ ] How much data went out through that session?

> Hint: vpn.log has the logins and, when the session closed, `bytes_out`.

?> Which account logged in over the VPN? :: s.kale
""",
        "02-how-did-they-get-in.sh": "cd ~/case\ngrep s.kale vpn.log",
        "03-contain-and-decide.md": """
## 3. Contain, then decide

Cut the attacker's session, isolate the machines they're on, stop the encryption. Then the decisions: which backup is clean, and when must CERT-In be told?

- [ ] VPN cut, fs02 and eng-ws14 isolated, locker.exe ended
- [ ] Which backup can you restore from?
- [ ] When is the six-hour CERT-In report due?

> Hint: Garnet noticed at 00:31 UTC, when the incident team was called. The clock starts when you noticed.

?> By what time (UTC, HH:MM) must CERT-In be told? :: 06:31
""",
        "03-contain-and-decide.sh": "cd ~/case\ncat backups.txt",
    }
    sim = {
        "title": "Ransomware night shift",
        "role": "On-call incident responder",
        "start": "2026-11-07T00:31:00Z",
        "speed": 1,
        "pins": ["files", "terminal", "tickets", "rdp", "rack", "tool-timeline", "chat", "notes"],
        "first": True,
        "cast": {"lead": {"name": "Rohan Deshpande", "role": "IT manager"}, "ceo": {"name": "Vandana Joshi", "role": "CEO"}},
        "story": "It's 00:31 UTC on Saturday 7 November 2026, six in the morning in Pune. Your phone rings: you're the on-call incident responder for Garnet Precision Engineering in Chakan.\n\nAt 00:12 the helpdesk logged that the engineering CAD files won't open and every folder has a file called RESTORE-FILES.txt. That's ransomware. It may still be running, and whoever started it may still be inside.\n\nStop the bleeding first: cut the way in, isolate what's infected, stop the encryption. Then answer the questions the CEO will ask in an hour: how did they get in, what did they take, can we restore, and who do we have to tell, by when?",
        "events": [
            {"at": 1, "chat": "lead", "text": "Thanks for picking up. Engineering share on fs02 is getting encrypted, files end in .garnet-locked. I don't know if it's still going. What do you need?"},
            {"at": 8, "chat": "lead", "text": "Everything we have is in ~/case, alerts are in Tickets. You can isolate machines from the Remote desktop and shut ports in the Server room."},
            {"after": "vpn", "chat": "lead", "text": "s.kale is Sachin Kale, a design engineer. HR says he's been on medical leave at home in Nashik since Monday. That wasn't him."},
            {"after": "kill", "chat": "lead", "text": "fs02's disk activity just dropped. I think it's stopped."},
            {"at": 900, "chat": "ceo", "text": "Rohan just woke me. I need to know in plain words: did they take anything, and can we be working on Monday?"},
            {"after": "backup", "chat": "ceo", "text": "Fourteen hours to restore from Thursday's tape. And we lose Friday's work. Understood. Who else needs to know?"},
        ],
        "replies": [
            {"match": "tape|backup|restore|monday", "who": "ceo", "text": "Then let's start the restore as soon as you're sure it's clean."},
            {"match": "cert-?in|report|regulator|6 ?hours|six", "who": "ceo", "text": "Six hours from when we noticed? Then draft it now and I'll sign it."},
        ],
        "objectives": [
            {"id": "what", "text": "Which program is encrypting the shares?", "ask": "Program", "answer": ["locker.exe", "locker"], "points": 10, "hint": "process.csv, or Remote desktop, fs02, Task Manager: C:\\ProgramData\\gpe\\locker.exe --path D:\\Shares."},
            {"id": "kill", "text": "Stop the encryption: end locker.exe on fs02", "after": "what", "points": 15, "on": {"event": "rdp.endtask", "host": "fs02", "image": "locker"}, "hint": "Remote desktop, fs02, Task Manager, End task on locker.exe."},
            {"id": "isofs", "text": "Isolate fs02", "points": 10, "on": {"event": "rdp.isolate", "host": "fs02", "isolated": True}, "hint": "Remote desktop, fs02, Isolate from the network. Keep it running: memory is evidence."},
            {"id": "vpn", "text": "Which account came in over the VPN?", "ask": "Account", "answer": ["s.kale"], "points": 10, "hint": "vpn.log: a failed then a successful login at 22:43 and 22:44, from 203.0.113.140, MFA not enrolled."},
            {"id": "cut", "text": "Cut the attacker's VPN session", "after": "vpn", "points": 15, "on": {"event": "rack.port", "ip": "10.50.0.1", "shut": True}, "hint": "Server room, vpn01, Shut port 443. At this hour nobody else needs the VPN; disable s.kale in the directory too."},
            {"id": "isows", "text": "Isolate eng-ws14, the first machine they reached", "after": "vpn", "points": 10, "on": {"event": "rdp.isolate", "host": "eng-ws14", "isolated": True}, "hint": "eng-ws14 logged an RDP logon for s.kale from the VPN address at 22:52, then rundll32 opened lsass at 23:05."},
            {"id": "admin", "text": "Which admin account reached fs02?", "ask": "Account", "answer": ["adm.rjoshi"], "after": "vpn", "points": 10, "hint": "fs02's Security log at 23:20:03: a network logon from ENG-WS14 with special privileges."},
            {"id": "exfil", "text": "Roughly how much data went out through the VPN session?", "ask": "Amount", "answer": ["~1[.,]8|1840|1\\.84"], "after": "vpn", "points": 10, "hint": "vpn.log, the session line closed by the admin: bytes_out=1840221190, about 1.8 GB."},
            {"id": "backup", "text": "Which backup can you restore from?", "ask": "Backup", "answer": ["~tape|offline|weekly|thursday"], "points": 10, "hint": "backups.txt: the NAS backup was reachable from fs02 and is encrypted too; shadow copies were deleted; the weekly LTO tape from Thursday 21:00 was taken off site and verified."},
            {"id": "certin", "text": "By what time (UTC) is the six-hour CERT-In report due?", "ask": "HH:MM UTC", "answer": ["06:31", "6:31"], "points": 10, "hint": "Garnet noticed at 00:31 UTC, when the incident team was called and confirmed ransomware. Six hours later: 06:31 UTC (12:01 IST)."},
            {"id": "esc", "text": "Escalate GA-705 in Tickets with what you know and what you did", "after": "kill", "points": 10, "on": {"event": "ticket.escalate", "id": "GA-70"}, "hint": "Tickets, GA-705: the way in, the machines, what you contained, the backup decision and the CERT-In deadline."},
        ],
        "debrief": "A strong night goes in this order. Stop the encryption: locker.exe on fs02, ended from Task Manager, and fs02 isolated but left running. Then the way in: s.kale over the VPN at 22:44 from 203.0.113.140, with MFA not enrolled, on an account whose owner is on leave. Cut that session at the VPN gateway, and isolate eng-ws14, where the attacker landed and took credentials from lsass at 23:05. Those credentials were adm.rjoshi's, used to reach fs02 at 23:20.\n\nThen answer the CEO. About 1.8 GB left through the VPN before it was cut, so assume data was taken. The NAS backup was on the network and is encrypted too; Thursday's tape is clean, so expect fourteen hours to restore and Friday's work lost. And the six-hour CERT-In report is due at 06:31 UTC, six hours after Garnet noticed at 00:31, not after the attack began.\n\nThe usual mistakes: switching fs02 off (memory gone), restoring before the way in is closed, and starting the CERT-In clock at the wrong moment.",
        "pass": 70,
    }
    about = {
        "title": "Simulation: Ransomware night shift",
        "kicker": "Simulation",
        "summary": "A 6 a.m. call: files are being encrypted. Stop it, close the way in, find what was taken, choose a clean backup and start the CERT-In clock.",
        "units": [4, 5], "level": "Intermediate", "minutes": 45, "order": 304,
        "tools": ["Remote desktop", "Server room", "Tickets", "Timeline", "Terminal"], "seminar_id": None, "published": True, "sim": sim,
        "script": {
            "intro": "Hello, and welcome to a simulation. It's six in the morning in Pune and your phone is ringing: you're the on-call incident responder, and a factory's files are being encrypted right now. Watch the order things happen in, because order is everything in a ransomware night.",
            "steps": [
                {"say": "First, stop the bleeding. The process list shows locker.exe on fs02, encrypting D colon Shares. I end it in Task Manager and isolate fs02, but I don't switch it off: memory is evidence.",
                 "after": "The IT manager confirms the disk activity dropped. Now I need the way in, or they'll just come back."},
                {"say": "The VPN log: a failed login for s.kale at 22:43, then a success at 22:44, from an outside address, and MFA not enrolled. The IT manager tells me Sachin Kale is on medical leave this week.",
                 "after": "So I cut the session at the VPN gateway in the Server room, and isolate eng-ws14, where the attacker landed and took credentials from lsass. Those credentials were adm.rjoshi's, used on fs02 at 23:20."},
                {"say": "Now the CEO's questions. What did they take? The VPN session sent out about 1.8 gigabytes. Can we restore? backups.txt says the NAS backup was on the network and is encrypted too, but Thursday's tape is off site and verified.",
                 "after": "And who do we tell? CERT-In within six hours of noticing. Garnet noticed at 00:31 UTC, when the incident team was called, so the report is due at 06:31 UTC. I escalate GA-705 with all of that."},
            ],
            "outro": "Stop the encryption, close the way in, isolate without switching off, then answer the business: what was taken, how to restore, and who to tell by when. Now take the night shift yourself.",
        },
    }
    return folder("x04-ransomware-night-shift", about, files, steps, net)


def sim_cloud():
    S8 = SEM / "s08-cloud-devsecops" / "files"
    files = tree(S8)
    files["README.txt"] = (S8 / "README.txt").read_text(encoding="utf-8") + "\nIn this simulation it is 06:30 UTC on Thursday 12 November. The cloud bill alarm has just gone off and the CTO has asked you to look now.\n"
    steps = {
        "01-who-is-spending-our-money.md": """
## 1. Who is spending our money?

The bill for 11 November is 3.4 times normal. The audit trail records every call to the cloud, with the identity, the key, the address and the region.

- [ ] Which identity, from which address, in which region?
- [ ] How many GPU instances were started?

> Hint: The CI runners call from 203.0.113.20, and the company only uses ap-south-1.

?> Which identity's key was used from 198.51.100.91? :: ci-deployer
""",
        "01-who-is-spending-our-money.sh": "cd ~/case/cloud\ngrep 198.51.100.91 audit.json | grep -o '\"action\": \"[A-Za-z]*\"\\|\"region\": \"[a-z0-9-]*\"' | sort | uniq -c",
        "02-how-did-the-key-leak.md": """
## 2. How did the key leak?

A pipeline key doesn't walk out on its own. Scan the repository, including Git history.

- [ ] Where is the key, and is it still in today's files?
- [ ] What does deleting it from the file not fix?

?> Which package has a critical advisory? :: pyyaml
""",
        "03-the-buckets.md": """
## 3. The buckets

Two buckets are public. One should be: product images. One shouldn't: customer invoices. And the attacker read from it.

- [ ] Which bucket must be closed, and which public alert is expected?
- [ ] What did the attacker create at 21:49 to keep access?

?> Which public bucket holds customer invoices? :: monsoon-invoices
""",
        "03-the-buckets.sh": "cd ~/case/cloud\ngrep -i 'bucket/monsoon-invoices\\|CreateAccessKey' audit.json | cut -c1-200",
    }
    sim = {
        "title": "Cloud bucket left open",
        "role": "Cloud security engineer, on call",
        "start": "2026-11-12T06:30:00Z",
        "speed": 1,
        "pins": ["files", "terminal", "tickets", "tool-cloudiam", "tool-codescan", "chat", "notes"],
        "first": True,
        "cast": {"lead": {"name": "Farah Sheikh", "role": "CTO"}, "plat": {"name": "Vikram", "role": "Platform team"}},
        "story": "It's 06:30 UTC on Thursday 12 November 2026 at Monsoon Mart, an online grocery company in Bengaluru. The cloud bill alarm has just gone off: yesterday cost 3.4 times normal.\n\nThe CTO wants answers before the morning stand-up: who is spending our money, how did they get in, what did they see, and is it stopped? The audit trail, the cloud alerts, the repository and the platform team's scanner output are in the case folder.",
        "events": [
            {"at": 1, "chat": "lead", "text": "Bill alarm just fired, 3.4x. I've put everything in ~/case. Tell me who, how, what they saw, and whether it's stopped."},
            {"after": "who", "chat": "plat", "text": "ci-deployer is the pipeline's key. It should only ever call from our runners, 203.0.113.20, in Mumbai."},
            {"after": "leak", "chat": "lead", "text": "So the key is in Git history? Revoke it. Vikram can issue a new one to the pipeline today."},
            {"after": "policy", "chat": "plat", "text": "Policy looks good. The pipeline deploy still works with it. Rolling it out now."},
        ],
        "replies": [
            {"match": "revok|rotate|disable|delete.*key|new key", "who": "plat", "text": "On it. Old key disabled, new key in the pipeline's secret store, not in the repo this time."},
            {"match": "invoice|bucket|public", "who": "lead", "text": "Customer invoices? Then we may have a personal data breach to report. Find out exactly which files they read."},
        ],
        "objectives": [
            {"id": "who", "text": "Which identity's key was used from 198.51.100.91?", "ask": "Identity", "answer": ["ci-deployer"], "points": 10, "hint": "cloud/audit.json, or alert CL-501 in Tickets."},
            {"id": "region", "text": "In which region were the GPU instances started?", "ask": "Region", "answer": ["ap-southeast-3"], "after": "who", "points": 10, "hint": "The RunInstances calls in audit.json. Monsoon only uses ap-south-1."},
            {"id": "count", "text": "How many GPU instances were started?", "ask": "Number", "answer": ["8", "eight"], "after": "who", "points": 10, "hint": "gpu-xl-1 to gpu-xl-8, started between 21:43 and 21:45."},
            {"id": "persist", "text": "What did the attacker create at 21:49 to keep access?", "ask": "What", "answer": ["~access ?key|createaccesskey|new key|key"], "after": "who", "points": 10, "hint": "CreateAccessKey on user/ci-deployer at 21:49: a second key the attacker owns. Revoking only the old key isn't enough."},
            {"id": "scan", "text": "Scan the repository, including Git history, in the Code scan program", "points": 10, "on": {"event": "tool.result", "tool": "codescan"}, "hint": "Start, Code scan, scan everything, then read the Secrets tab."},
            {"id": "leak", "text": "Where did the key leak from?", "ask": "Where", "answer": ["~git|history|deploy\\.sh|patch"], "after": "scan", "points": 10, "hint": "git-history.patch: the line removed from deploy.sh still holds the key. Anyone who clones the repo can read it."},
            {"id": "bucket", "text": "Which public bucket must be closed?", "ask": "Bucket", "answer": ["monsoon-invoices"], "points": 10, "hint": "CL-505: monsoon-invoices allows public read. CL-504's monsoon-assets holds product images and is public on purpose."},
            {"id": "benign", "text": "Close CL-504 (public product images) as expected activity", "points": 5, "on": {"event": "ticket.close", "id": "CL-504", "disp": "~benign|false"}, "hint": "Tickets, CL-504, Close as Benign, with a reason: product images are meant to be public."},
            {"id": "policy", "text": "Write a policy that blocks every attacker action without breaking the pipeline", "after": "who", "points": 15, "on": {"event": "tool.result", "tool": "cloudiam", "data.n": 0, "data.broken": 0}, "hint": "Cloud IAM: allow ci-deployer only from 203.0.113.20 and only in ap-south-1. The checker shows attacker actions still allowed and normal actions broken; get both to 0."},
            {"id": "esc", "text": "Escalate CL-502 with who, how, what they saw and what you did", "after": "policy", "points": 10, "on": {"event": "ticket.escalate", "id": "CL-50"}, "hint": "Tickets, CL-502: the leaked key in Git history, the eight GPU instances, the invoices read, the second key, the policy and the revocation."},
        ],
        "debrief": "A strong run follows the money. The audit trail shows ci-deployer's key used from 198.51.100.91 instead of the CI runners' 203.0.113.20, starting eight GPU instances in ap-southeast-3, a region Monsoon never uses, and then creating a second access key at 21:49 so the attacker keeps access when the first is revoked. It also read invoices from monsoon-invoices.\n\nThe code scan shows how: the key was removed from deploy.sh, but Git history still has it. Deleting a secret never un-leaks it: revoke both keys, issue a new one to the pipeline's secret store, and lock ci-deployer to its runners' address and region with a policy that breaks nothing else. Close the invoices bucket; leave the product-images bucket public and close its alert as expected. Then escalate: customer invoices read by an outsider may be a personal data breach to report.",
        "pass": 70,
    }
    about = {
        "title": "Simulation: Cloud bucket left open",
        "kicker": "Simulation",
        "summary": "The cloud bill is 3.4 times normal. Follow the money to a leaked pipeline key, a public invoices bucket and a second key the attacker made, then lock it down.",
        "units": [6], "level": "Intermediate", "minutes": 40, "order": 305,
        "tools": ["Cloud IAM", "Code scan", "Tickets", "Terminal"], "seminar_id": None, "published": True, "sim": sim,
        "script": {
            "intro": "Hello, and welcome to a simulation. It's early on a Thursday and a cloud bill alarm has gone off. In the cloud, a stolen key turns straight into money and data, so let's follow the money.",
            "steps": [
                {"say": "The audit trail records every call. I look for the address that isn't ours.",
                 "after": "ci-deployer's key, used from 198.51.100.91, started eight GPU instances in ap-southeast-3, a region Monsoon never uses. And at 21:49 it created a second access key, so revoking the first won't be enough."},
                {"say": "How did the key get out? I scan the repository, including the Git history.",
                 "after": "The key was deleted from deploy.sh, but the removed line is still in the history. Anyone who clones the repo has it. So both keys get revoked and the pipeline gets a new one from a secret store."},
                {"say": "Two public buckets. One is product images, public on purpose, so I close that alert as expected. The other is customer invoices, and the attacker read from it.",
                 "after": "I write a policy that only lets ci-deployer call from its runners and only in Mumbai, and the checker confirms it blocks every attacker action and breaks nothing. Then I escalate, because invoices read by an outsider may be a reportable breach."},
            ],
            "outro": "Follow the money, find the leak, revoke every key the attacker made, lock the identity to where it belongs, and tell the business what was seen. Now try it yourself.",
        },
    }
    return folder("x05-cloud-bucket-left-open", about, files, steps, None)


if __name__ == "__main__":
    which = sys.argv[1:] or ["phish", "pentest", "office", "ransom", "cloud"]
    made = {"phish": sim_phish, "pentest": sim_pentest, "office": sim_office, "ransom": sim_ransom, "cloud": sim_cloud}
    for w in which:
        print(made[w]())
