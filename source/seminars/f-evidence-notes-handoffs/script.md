# Lecture script: Evidence, notes and handoffs

Free seminar · about 120 minutes of lab work · about 16 minutes of narration

This is what `python tools/teach.py demo f-evidence-notes-handoffs` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice f-evidence-notes-handoffs`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script f-evidence-notes-handoffs` to refresh this file.

## Opening

Hello, and welcome to Evidence, notes and handoffs, the free foundation seminar. I'm going to start with a confession about this job. Most of the work in a security team isn't hacking and it isn't clever tools. It's writing things down so the next person can act. A ticket goes from the helpdesk to the SOC. An alert goes from the SOC to the incident lead. The night shift hands over to the morning shift. Every one of those handoffs is a moment where an attack can slip through, because the note was vague, or had no times, or mixed up facts with guesses. So today we take one real case, a fake invoice that turned into ransomware at a freight company called Kestrel Logistics, and one helpdesk ticket that nobody can use. Over the next twenty minutes you'll rewrite it three ways: as a triage note, as an escalation, and as a shift handover. By the end, you'll have three pieces of writing that any analyst could pick up and act on. Everything runs in your browser, in the notebook on your screen. Let's start where the analyst starts: with the ticket.

## 1. A ticket nobody can act on

Step one: a ticket nobody can act on. It's Monday the second of November 2026, at Kestrel Logistics. All the times in this case are in UTC, and India is five and a half hours ahead, so 09:00 UTC is 2:30 in the afternoon in India. Keep that in mind, because mixing time zones is the most common mistake in incident notes. The Linux cell prints two notes: helpdesk ticket 88213, and last night's shift handover. Read them the way the next person would, someone who wasn't there and has to decide what to do in the next five minutes.

*After it runs:*

Let's look closely. The ticket was opened automatically at 09:16, when dev.kapoor pressed the Report phishing button on message 4A1F21C02. That's a real fact, with a time and a source. Then Ramesh from the helpdesk writes: user says got weird invoice email, probably spam, told her to delete it. Notice three problems in that one line. Which user? Probably spam is a guess. And told her to delete it means he asked someone to destroy the evidence. Next line: HR PC slow, three question marks, maybe virus, will check later. Another guess, and later is not a time. Then: someone said files on share have funny names, not sure if related. That's the most important line in the whole ticket, files being renamed is what ransomware does, and it's written as an afterthought. Finally, at 09:52, he pulled the cable on the HR PC. That was the right thing to do, but there's no time zone and no host name. Now the night handover: all quiet, couple of alerts, nothing major, printer thing again, AV update failed somewhere, think it fixed itself, someone on VPN from Singapore, didn't check. Not one alert ID, not one host, and a lead that was left for nobody. Here's the test I want you to remember for every note you ever write. A useful note answers five questions: what fired, what I checked, what I found, what I don't know yet, and what happens next. This ticket answers almost none of them. Answer the two questions: the message ID is 4A1F21C02, and the cable was pulled at 09:52.

On screen: the step text, the Linux cell.

## 2. Find the facts behind the ticket

Step two: find the facts behind the ticket. A good note is built from evidence, not from what someone said on the phone. We'll check two logs. First mail.log, the mail server's delivery log. In it, nrcpt means the number of recipients, and each to line is one mailbox. Then proxy.log, the web proxy, which records every download. In the proxy log, TCP_MISS slash 200 means the download worked, and TCP_DENIED slash 403 means the proxy blocked it. One more thing: proxy times are Unix epoch seconds, a count of seconds since 1970. The Python cell turns them into ordinary UTC clock times, so every fact in your note uses the same clock.

*After it runs:*

The mail log tells us message 4A1F21C02 arrived at 08:51 from bounce at kestrel-logistlcs.com. Read that domain slowly: logistlcs, with an L where the i should be. It went to three people: priya.nair, dev.kapoor and tomas.reyes. At 09:15 dev.kapoor reported it, and at 09:18 the proxy's blocklist was updated with the fake domain. Now the proxy. At 09:02:31 UTC, 10.20.0.14 downloaded INV-30412.docm, a Word document with macros. At 09:03:09 the same address downloaded s2.bin from cdn-update-check.net, a program. And at 09:20:47, 10.20.0.15, the Finance laptop, tried to download the same invoice and was denied, because the blocklist had gone in two minutes earlier. Look how much we now know that the ticket didn't say. Three recipients, one download, one blocked attempt, and a second download that wasn't an invoice at all. And every fact has a time and a file name, so anyone can check it. Answer the questions: three people received it, and 10.20.0.14 downloaded it.

On screen: the step text, the Linux cell, the Python cell.

## 3. What ran on the PC

Step three: what ran on the PC. The ticket said HR PC slow, maybe virus. That's a guess. The process list from the company's endpoint tool says exactly what ran, when, and which program started it. Every process has a PID, its own number, and a ppid, the number of its parent. The Python cell builds the family tree for hr-pc07, so you can follow it from top to bottom.

*After it runs:*

Here's the chain. At 09:02:41, WINWORD.EXE opens INV-30412.docm from Priya's Downloads folder. At 09:02:55, Word starts cmd.exe, with a command that starts PowerShell minimised. Ask yourself: should a word processor ever start a command prompt? No. That's the macro running. One second later, PowerShell starts with the window hidden and runs a script from C:\Users\Public. At 09:03:20 PowerShell starts svchost-upd.exe, PID 4810, from the same Public folder. The real svchost.exe lives in C:\Windows\System32 and runs as SYSTEM. A file called svchost-upd.exe in a folder everyone can write to is pretending to be a Windows program. And at 09:41 that same program starts again with the arguments walk Z drive, extension kestrel-locked, note README_RESTORE.txt. Z is the mapped file share. That's the moment the encryption began. So the facts are: Word, then cmd, then hidden PowerShell, then the malware, and forty minutes later, the share. Answer the questions: WINWORD.EXE started cmd.exe, and the malware's PID is 4810.

On screen: the step text, the Python cell.

## 4. Write the triage note

Step four: write the triage note. Now we rewrite ticket 88213 as a proper triage note for alert AL-2203, the macro document alert. The report builder on your screen checks each section as you type. It wants an alert ID, times with a time zone, the exact searches you ran, at least one gap, a disposition and an owner. Three rules make notes useful. One time zone for everything, UTC here, written every single time. Facts say where you saw them, and guesses go in their own section called what I don't know yet. And write what you ran, so the next person can repeat it without having to ask you.

*After it runs:*

Here's the model note. What fired: AL-2203, Office document with macros opened from the internet, severity high, host hr-pc07, user priya.nair, at 09:02:44 UTC. What I checked: the exact grep on mail.log for the message ID, the grep on proxy.log for the document and the download, and the process tree for hr-pc07. What I found: each fact from steps two and three, with its time and its file. What I don't know yet: did the other two recipients open the invoice, and was anything copied out? That section is never empty, and writing it down is what stops the next person assuming everything has been checked. Then the disposition, escalate, and the owner. When you try it yourself, write your own note first and only then compare it with the model. And download the Markdown: it's part of your hand-in. Answer the question: the disposition for AL-2203 is escalate.

On screen: the step text, the report tool with the model answer.

## 5. Escalate

Step five: escalate. An escalation is read in about ten seconds, often by someone who has just been woken up. So the first line is the ask: what you need, from whom, and by when. After that comes the severity and the one fact that decided it, then what you know, what you don't know, the impact, what you did, and where the evidence is. And one thing beginners forget: say what you have not done. I have not changed anything on the host tells the incident lead the evidence is still clean. The Linux cell counts the encrypted files on the share and hashes the evidence, so you can say exactly what you saved.

*After it runs:*

The share listing was taken at 09:58, after the cable was pulled. The HR folder has six files renamed to .kestrel-locked, between 09:41 and 09:42, and a ransom note. The Finance folder has four more, between 09:47 and 09:50: the ledger, vendor bank details, GST returns and the budget. That's ten encrypted files, and the Ops folder is untouched, because the cable was pulled before the malware reached it. The hashes give us a fingerprint of every evidence file, so later we can prove nothing changed. Now read the model escalation. The ask: please open a critical incident and approve isolating hr-pc07 and taking the HR and Finance shares read-only, by 10:05 UTC. Severity: critical, because files are being encrypted right now. That's the deciding fact. Then the timeline from 08:51 to 09:52, each line with its source. What we don't know: the other two recipients, whether data was copied out, and whether the attacker can reach any other host. The impact: payroll and vendor bank details, which are personal data. And the evidence, saved with hashes. Answer the questions: ten files were encrypted, and the Ops folder was not.

On screen: the step text, the Linux cell, the report tool with the model answer.

## 6. Work the queue before you hand over

Step six: work the queue before you hand over. Your shift had ten alerts, and the night shift left a note that said nothing major. Before you hand over, every alert needs a disposition and one line of reason that a stranger could check. Some alerts belong to the incident. Some are ordinary noise and should be closed, so the next shift doesn't waste an hour chasing them. The alert queue on your screen sorts by severity, then by time. Pick an alert, choose a disposition, and write why.

*After it runs:*

Here's how the queue works out. Seven alerts belong to this incident and get escalated: AL-2201, the email from the look-alike domain; AL-2203, the macro document; AL-2204, a scheduled task that runs the malware every time someone logs on; AL-2205, the download of s2.bin; AL-2210, a new local administrator called support_svc; AL-2208, the mass rename on the file share; and AL-2207, failed logons from outside for support_svc and Administrator. Three are benign. AL-2202 looks scary, an impossible-travel sign-in from Singapore, but read the detail line: the Singapore address is the company's own VPN exit. AL-2206, the antivirus update, failed and then worked on retry at 09:25. And AL-2209 is a 412-page print job, which is a lot of paper but not an attack. Closing those three with a clear reason is just as valuable as escalating the other seven. Answer the questions: AL-2202 is the VPN exit, and the account the attacker created is support_svc.

On screen: the step text, the alerts tool with the model answer.

## 7. Write the shift handover

Step seven: write the shift handover. Now rewrite last night's all quiet note as a handover that leaves nothing behind. Every open item by ID, with the next step and who owns it. What you closed, one line each. What the next shift should watch for. Who you called and when. And any temporary change, like a block, that someone must review or undo later.

*After it runs:*

Here's the model handover. Still open: INC-0211, the incident made from five of the alerts, contained at 09:52, with the next step, a restore decision, and the owner, IT operations. AL-2201, same campaign: confirm whether dev.kapoor and tomas.reyes opened the invoice, owned by the afternoon analyst, by 14:00 UTC. AL-2207, the failed logons: confirm support_svc is disabled, owned by IT ops. Closed this shift: the three benign alerts, each with its reason. Watch for: any connection to 198.51.100.140 or cdn-update-check.net, any new account called support_svc, and any new file ending in kestrel-locked. Calls: the escalation by phone at 09:55, and a message to IT ops at 10:02, answered at 10:06. And the temporary proxy blocks, with a review date of the ninth of November and who may remove them. A temporary block nobody remembers becomes a permanent one. Compare that with all quiet, couple of alerts. The afternoon shift can start work the moment they read it.

On screen: the step text, the report tool with the model answer.

## 8. Hand in

Step eight: hand in. You hand in three pieces of writing: the triage note for AL-2203, the escalation, and the shift handover. Your teacher marks them with the rubric on your screen, and your certificate is issued once the hand-in is scored. Use the Hand in button at the top of the notebook, and your notes, your tool work and your answers go with it.

*After it runs:*

Before you press it, one last habit. Read each piece aloud, once. If any sentence needs you to explain it, rewrite it, because you won't be there when someone else reads it. Look at the rubric: most of the points are for the boring parts, the time zones, the sources, the owners, the IDs. That's on purpose. Those are the parts that make a note useful at three in the morning.

On screen: the step text.

## Wrap-up

That's the seminar. You started with a ticket that said probably spam and maybe virus, and you turned it into three documents an analyst can act on: a triage note with facts, times and sources; an escalation that puts the ask first; and a handover that leaves nothing behind. Remember the five questions: what fired, what I checked, what I found, what I don't know yet, and what happens next. Use one time zone, write down what you ran, and keep facts and guesses apart. These habits matter in every security job, from the SOC to the boardroom. When you're ready, the next seminar, Reading evidence, takes you into packets, Linux and Windows logs. Thank you for watching, and well done.

## YouTube chapters (estimate; `python tools/teach.py demo f-evidence-notes-handoffs` writes the exact ones)

```
0:00 Opening
1:28 1. A ticket nobody can act on
3:57 2. Find the facts behind the ticket
5:49 3. What ran on the PC
7:24 4. Write the triage note
9:15 5. Escalate
11:25 6. Work the queue before you hand over
13:10 7. Write the shift handover
14:46 8. Hand in
15:41 Wrap-up
```
