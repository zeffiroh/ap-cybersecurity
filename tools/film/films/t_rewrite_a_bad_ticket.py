from kit import TREE, after, build, chapter, clear, close, cmd, edit, files_window, save_note, say, term, wait, write

TRIAGE = """TRIAGE NOTE  AL-2203  Office document with macros opened from the internet
Analyst: day shift SOC    Written: 2026-11-02 10:05 UTC    All times UTC

What fired
  09:02:44 UTC  AL-2203 on hr-pc07 (priya.nair): INV-30412.docm enabled macros.

What I checked (repeat these)
  grep 4A1F21C02 mail.log
  awk with strftime on proxy.log (epoch to UTC)
  python3 tree.py hr-pc07 (process tree from process.csv)

What I found (fact, source)
  08:51:09  invoice from kestrel-logistlcs.com delivered to 3 mailboxes (mail.log)
  09:02:31  hr-pc07 downloaded INV-30412.docm, 48 KB (proxy.log)
  09:02:55  WINWORD started cmd, then hidden PowerShell upd.ps1 (process.csv)
  09:03:09  hr-pc07 downloaded s2.bin from cdn-update-check.net (proxy.log)

What I don't know yet
  Whether the other two people opened the email. Whether anything left the network.

Disposition
  ESCALATE. Macro document led to a downloaded program.

Next and owner
  Incident lead decides containment. SOC owns the queue.
"""

scenes = [
 chapter("Opening"),
 files_window(),
 say("Hello, and welcome. Most security work is handed from one person to the next: helpdesk to the SOC, the SOC to the incident lead, the night shift to the morning shift. If the note is poor, the next person starts from zero, and the attack keeps running while they do. Today you'll take a ticket nobody can act on and turn it into a triage note someone can."),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say("The setting. Kestrel Logistics, a freight company. Monday the second of November 2026. All times are UTC, and India is five and a half hours ahead. This morning a fake invoice reached three people, and the HR laptop opened it. The case folder has helpdesk ticket 88213 and last night's shift handover."),
 close("files"),
 term,

 chapter("1. A ticket nobody can act on"),
 say("Read both notes as the person who receives them. Ask four questions. Which facts have a time and a source? Which words are guesses? What does the next person need that isn't there? And what's wrong with a handover that says all quiet?"),
 cmd("cat ticket-88213.txt", 3),
 after("The ticket does have some real facts. At 09:16 dev.kapoor reported message 4A1F21C02 as phishing, and at 09:52 the helpdesk pulled the network cable on the HR PC. Every line has a time, but no time zone. The rest is guesswork: probably spam, maybe virus, three question marks. It doesn't name the host or the user, says nothing about which alert fired, and someone was told to delete the evidence."),
 cmd("cat handover-night.txt", 3),
 after("The handover is worse. All quiet, couple of alerts, nothing major names no alert and no host, and someone on the VPN from Singapore, didn't check, is a lead that was left for nobody. The morning shift can't check a single word of it. A simple test for any note: it answers five questions. What fired, what I checked, what I found, what I don't know yet, and what happens next."),
 clear,

 chapter("2. Find the facts behind the ticket"),
 say("So find the facts behind the ticket. The mail log first."),
 cmd("grep 4A1F21C02 mail.log", 3),
 cmd("awk '{ print strftime(\"%H:%M:%S\", $1, 1), $3, $4, $7 }' proxy.log", 3.5),
 after("The proxy log keeps times as seconds since 1970, so awk turns them into readable UTC. Now what ran on the HR PC."),
 cmd("python3 tree.py hr-pc07", 3.5),
 after("Word started cmd, which started a hidden PowerShell. That's the fact the ticket was missing."),
 clear,

 chapter("3. Write the triage note"),
 say("Now rewrite ticket 88213 as a triage note for alert AL-2203. Three rules make notes useful. One time zone for everything, UTC here, written every time. Every fact says where you saw it, and guesses go under what I don't know yet. And write the exact searches you ran, so the next person can repeat them without asking you."),
 cmd("mkdir -p notes && ls", 1),
 edit("notes/triage-AL-2203.txt"),
 write(TRIAGE, cps=44),
 save_note(),
 after("What fired. What I checked. What I found, each fact with its source. What I don't know yet, never empty. Then the disposition, escalate, and who owns it now."),
 close("note"),
 clear,

 chapter("Where next"),
 say("That was one step from Seminar F, Evidence, notes and handoffs, the free foundation seminar. The full seminar has a longer video, every step at three levels, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen."),
 chapter("Wrap-up"),
 say("To recap. A good note names the alert, shows the searches you ran, gives each fact a time and a source, keeps guesses apart, and ends with a disposition and an owner. That's how the next person starts from where you stopped. Thank you for watching."),
 wait(2),
]

build("t-rewrite-a-bad-ticket", scenes, host="kestrel-soc", files={"tree.py": TREE})
