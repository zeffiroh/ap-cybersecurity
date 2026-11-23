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
  09:03:25 to 09:38:25  a connection every 5 minutes to 198.51.100.140 (proxy.log)
  09:41:05  svchost-upd.exe walked Z: = \\\\fs01\\shared, adding .kestrel-locked (process.csv)
  09:20:47  fin-pc02 tried the same link; the proxy blocked it, 403 (proxy.log)

What I don't know yet
  Whether tomas.reyes opened the email. Whether anything left the network.
  What support_svc (AL-2210) was used for.

Disposition
  TRUE POSITIVE, escalated as a ransomware incident. Macro document led to a
  downloaded program that encrypted the HR and Finance shares.

Next and owner
  Incident lead decides containment (escalation sent 10:08 UTC). SOC owns the queue.
"""

ESCALATION = """ASK: Incident lead on call, declare a ransomware incident and approve isolating fs01 and blocking 198.51.100.140 at the firewall, by 10:30 UTC.

Severity: CRITICAL. One fact decided it: files on \\\\fs01\\shared are being encrypted (10 files, HR and Finance, 09:41 to 09:50 UTC).

What we know
  hr-pc07 (priya.nair) opened a macro invoice at 09:02 UTC, downloaded s2.bin, and beaconed to 198.51.100.140 every 5 minutes.
  The program walked Z: (\\\\fs01\\shared) at 09:41 UTC. Ops is untouched as of 09:58.
What we don't know
  Whether other PCs are infected. Whether data was copied out (one larger 61 KB connection at 09:38).
Impact
  HR payroll and Finance ledgers unreadable. Staff payments may be delayed.
What we did
  Helpdesk pulled the cable on hr-pc07 at 09:52. Proxy blocks the lookalike domain since 09:18.
What we have NOT done
  We have not changed anything on hr-pc07 or fs01. The evidence is clean.
Evidence
  /case/notes/evidence-hashes.txt (SHA-256 of every file we hold).
"""

DISPOSITIONS = """AL-2201  TRUE POSITIVE, linked to the incident. Lookalike domain sent the invoice (mail.log 08:51).
AL-2202  CLOSED, benign. Singapore is our VPN exit; dev.patel was on the VPN.
AL-2203  TRUE POSITIVE, incident. See triage note.
AL-2204  TRUE POSITIVE, incident. Task UpdCheck keeps svchost-upd.exe running at log on.
AL-2205  TRUE POSITIVE, incident. s2.bin is the program that ran.
AL-2210  TRUE POSITIVE, incident. support_svc created and made admin at 09:04.
AL-2206  CLOSED, benign. AV update retried successfully at 09:25.
AL-2209  CLOSED, benign. Large print job by a.kulkarni, not linked to the incident.
AL-2208  TRUE POSITIVE, incident. The encryption itself.
AL-2207  OPEN, incident. 198.51.100.140 (the beacon address) tried support_svc at 09:59. Block it.
"""

HANDOVER = """SHIFT HANDOVER  day shift to evening shift  2026-11-02 14:00 UTC

OPEN
  INC-1102 ransomware from INV-30412.docm. Owner: incident lead. Next: agree a restore plan with the file server owner.
  AL-2207  failed logons from 198.51.100.140. Owner: network team. Next: confirm the firewall block holds.
CLOSED (one line each)
  AL-2202 VPN exit, benign.  AL-2206 AV retried OK.  AL-2209 print job, benign.
WATCH FOR
  Any host talking to cdn-update-check.net or 198.51.100.140.
  Any log on with support_svc anywhere.
  tomas.reyes: received the invoice, not yet confirmed whether opened.
CALLS MADE
  10:08 UTC incident lead (escalation).  10:20 UTC network team (block).
TEMPORARY CHANGES TO REVIEW
  Firewall block on 198.51.100.140, added 10:24 UTC. Review on 09 Nov.
  hr-pc07 unplugged since 09:52 UTC. Do not reconnect before IR says so.
"""

scenes = [
 chapter("Opening"),
 files_window(),
 say("Welcome to Evidence, notes and handoffs, the free foundation seminar. Here's a confession about this job. Most of the work in a security team isn't hacking, and it isn't clever tools. It's writing things down so the next person can act. A ticket goes from the helpdesk to the SOC. An alert goes from the SOC to the incident lead. The night shift hands over to the morning shift. Every one of those handoffs is a moment where an attack can slip through, because the note was vague, or had no times, or mixed up facts with guesses."),
 {"point": [0.45, 0.3], "in": "files", "secs": 1.0},
 say("This is the case folder from Kestrel Logistics, a freight company, on Monday the second of November 2026. A fake invoice turned into ransomware, and the helpdesk ticket about it is one nobody can use. Over the next twenty minutes we rewrite it three ways: as a triage note, as an escalation, and as a shift handover. Everything you'll see is real software on a real Linux machine: the terminal, a little Python, and a plain text editor."),
 close("files"),
 term,

 chapter("1. A ticket nobody can act on"),
 say("Step one: a ticket nobody can act on. All the times in this case are in UTC. India is five and a half hours ahead, so 09:00 UTC is half past two in the afternoon in India. Keep that in mind, because mixing time zones is the most common mistake in incident notes. First, the helpdesk ticket."),
 cmd("cat ticket-88213.txt", 3),
 after("Read it as the next person would: someone who wasn't there and has to decide what to do in the next five minutes. Probably spam. Maybe virus. Will check later. Files have funny names, not sure if related. Every line is a guess, nothing says where it came from, and the most important fact, files on a share being renamed, is buried in the middle. Now last night's handover."),
 cmd("cat handover-night.txt", 3),
 after("All quiet. Couple of alerts, nothing major. Someone on VPN from Singapore, didn't check. No alert numbers, no times, nothing anyone could follow up. Today we replace both of these with notes that work."),
 clear,

 chapter("2. Find the facts behind the ticket"),
 say("Step two: find the facts behind the ticket. A good note is built from evidence, not from what someone said on the phone. The ticket gives us one solid clue: message 4A1F21C02. grep pulls every line about that message out of the mail server's delivery log."),
 cmd("grep 4A1F21C02 mail.log", 3),
 after("Received at 08:51 from a server called vps-118 at a bulk hosting company. The sender's domain is kestrel-logistlcs, with an l where the i should be. nrcpt equals three: three recipients, and each to line is one mailbox. priya.nair, dev.kapoor and tomas.reyes all got it. The ticket only mentioned one person. Now the headers of the message itself."),
 cmd("grep -E '^(From|Reply-To|To|Subject|    spf|    dmarc)' invoice.eml", 3),
 after("The display name says Kestrel Logistics Accounts, but the address is the lookalike domain, and replies go to a free mail account. SPF and DMARC are none: nothing proves who sent it. Next, the web proxy, which records every download. Its times are Unix epoch seconds, a count of seconds since 1970, so on their own they're unreadable."),
 cmd("head -n 3 proxy.log", 2.5),
 say("awk can rewrite the first field as a UTC clock time. strftime formats a time, and the 1 at the end means UTC. We print the time, the PC's address, the result and the address it fetched."),
 cmd("awk '{ print strftime(\"%H:%M:%S\", $1, 1), $3, $4, $7 }' proxy.log", 3.5),
 after("Now it reads like a story. At 09:02:31, 10.20.0.14, that's hr-pc07, downloaded the invoice document, a docm, which means Word with macros. Thirty-eight seconds later it downloaded s2.bin from a domain called cdn-update-check.net. After that, a connection to the same place every five minutes, like a heartbeat. Analysts call that a beacon. And at 09:20, 10.20.0.15, that's fin-pc02, tried the same invoice link and got TCP_DENIED, 403: the proxy blocked it, because the domain was added to the blocklist at 09:18."),
 clear,

 chapter("3. What ran on the PC"),
 say("Step three: what ran on the PC. The ticket said HR PC slow, maybe virus. That's a guess. The process list from the company's endpoint tool says exactly what ran, when, and which program started it. Every process has a PID, its own number, and a parent PID, the number of the program that started it. Here's a short Python script that turns that list into a family tree."),
 edit("tree.py", "code", (260, 90, 1400, 860)),
 wait(4),
 after("It reads the CSV file, keeps the rows for the computer we name, here hr-pc07, groups every process under its parent, and prints the tree from the top down, one indent per generation."),
 close("code"),
 cmd("python3 tree.py hr-pc07", 3.5),
 after("Read it from the top. Explorer, the Windows desktop, started Outlook, Chrome and Word. Word opened INV-30412.docm from Downloads at 09:02:41. Fourteen seconds later Word started cmd, cmd started a hidden PowerShell running upd.ps1 from the Public folder, and PowerShell started svchost-upd.exe, a program pretending to be part of Windows. At 09:41 that program mapped the Z drive to the file server's shared folder, and started itself again with walk Z, extension kestrel-locked, and a ransom note. That's not a slow PC. That's ransomware, and its parent chain leads straight back to the invoice."),
 clear,

 chapter("4. Write the triage note"),
 say("Step four: write the triage note for alert AL-2203, the macro document alert. On the course site, the report builder checks each section as you type. Here we write it in a plain text editor, which is how most teams start. Three rules make notes useful. One time zone for everything, written every single time. Facts say where you saw them, and guesses go in their own section, called what I don't know yet. And write what you ran, so the next person can repeat it without asking you."),
 cmd("mkdir -p notes && ls", 1),
 edit("notes/triage-AL-2203.txt"),
 write(TRIAGE, cps=34),
 save_note(),
 after("Look at the shape. What fired, with the alert ID and the time in UTC. What I checked, as commands anyone can rerun. What I found, one fact per line, each with its source in brackets. What I don't know yet, kept apart. A disposition, true positive, with one sentence of reasons. And the next step with an owner."),
 close("note"),
 clear,

 chapter("5. Escalate"),
 say("Step five: escalate. Before we write, two facts the incident lead will ask for: how many files are encrypted, and where. grep minus c counts the locked files in the share listing the helpdesk took at 09:58."),
 cmd("grep -c kestrel-locked share_listing.txt", 2),
 cmd("grep -E 'Directory|locked' share_listing.txt | cut -c1-70", 3),
 after("Ten files: six in HR, between 09:41 and 09:42, and four in Finance, between 09:47 and 09:50. Ops is still untouched. Now we fingerprint the evidence, so we can prove later that nobody changed it. sha256sum prints a hash for every file, and we save the list with the notes."),
 cmd("sha256sum *.txt *.log *.csv *.eml *.json | tee notes/evidence-hashes.txt", 3),
 after("An escalation is read in about ten seconds, often by someone who has just been woken up. So the first line is the ask: what you need, from whom, and by when. Then the severity and the one fact that decided it, what you know, what you don't, the impact, what you did, and where the evidence is. And one thing beginners forget: say what you have not done."),
 edit("notes/escalation.txt"),
 write(ESCALATION, cps=34),
 save_note(),
 after("We have not changed anything on the host. That one line tells the incident lead the evidence is still clean, and that they can still choose how to collect it."),
 close("note"),
 clear,

 chapter("6. Work the queue before you hand over"),
 say("Step six: work the queue. Our shift had ten alerts, and the night shift's note said nothing major. Before handing over, every alert needs a disposition and one line of reason a stranger could check. jq reads the alert file, which is JSON, and prints one line per alert: its ID, time, severity, host and rule."),
 cmd("jq -r '.[] | [.id, .time[11:19], .severity, .host, .rule] | @tsv' alerts.json | column -t -s $'\\t'", 3.5),
 after("Six of them belong to the incident: the lookalike email, the macro, the scheduled task, the download, the new local administrator called support_svc, and the mass rename on the file server. Three are ordinary noise: the Singapore sign-in is the company's own VPN exit, the antivirus update retried and worked, and the print job is just a print job. And AL-2207 is new: failed logons for support_svc from 198.51.100.140 at 09:59. That's the beacon address from the proxy log. The attacker is still trying to get back in."),
 edit("notes/dispositions.txt"),
 write(DISPOSITIONS, cps=36),
 save_note(),
 after("Closing the noise matters as much as escalating the attack. The next shift won't waste an hour chasing a printer."),
 close("note"),
 clear,

 chapter("7. Write the shift handover"),
 say("Step seven: the shift handover. We replace last night's all quiet with a note that leaves nothing behind. Every open item by ID, with the next step and who owns it. What we closed, one line each. What the next shift should watch for. Who we called and when. And any temporary change, like a block, that someone must review or undo later."),
 edit("notes/handover.txt"),
 write(HANDOVER, cps=34),
 save_note(),
 after("Compare it with the note we started with. Someone who wasn't here today can pick this up at two o'clock and know exactly what's open, what to watch, and what to undo."),
 close("note"),
 clear,

 chapter("8. Hand in"),
 say("Step eight: hand in. Three pieces of writing: the triage note for AL-2203, the escalation, and the shift handover."),
 cmd("ls -l notes/ && wc -l notes/*.txt", 3),
 after("On the course site, paste them into the report builder, or hand in the notebook, and your teacher marks them with the rubric on screen. Your certificate is issued once the hand-in is scored."),
 chapter("Wrap-up"),
 say("That's the seminar. You started with a ticket that said probably spam and maybe virus, and turned it into three documents an analyst can act on. A triage note with facts, times and sources. An escalation that puts the ask first. And a handover that leaves nothing behind. Remember the five questions: what fired, what I checked, what I found, what I don't know yet, and what happens next. Use one time zone, write down what you ran, and keep facts and guesses apart. When you're ready, the next seminar, Reading evidence, takes you into packets, Linux and Windows logs. Thank you for watching, and well done."),
 wait(2),
]

build("f-evidence-notes-handoffs", scenes, host="kestrel-soc", files={"tree.py": TREE})
