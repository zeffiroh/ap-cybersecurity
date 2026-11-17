# Lecture script: Capstone A: the night shift

Seminar 4 · Capstone · about 270 minutes of lab work · about 14 minutes of narration

This is what `python tools/teach.py demo s04-capstone-night-shift` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice s04-capstone-night-shift`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script s04-capstone-night-shift` to refresh this file.

## Opening

This is Capstone A, the night shift. You work for a managed SOC, a company that watches other companies' networks around the clock. Tonight's client is Wattle and Finch Accountants, a fourteen-person practice in Brisbane. When it's ten in the morning in Brisbane, it's half past five in India, so their working day is your night. The queue has twelve alerts and no severities, because the client's old SIEM doesn't send them. One real intrusion is hiding in there. In a capstone the steps tell you what to deliver, not how, and every hint you open costs a point. I'll walk the whole shift once, so you can see what good looks like, and then it's your turn.

## 1. How the night desk works

Step one: how the night desk works. A capstone uses every program from seminars two and three at once, so start by seeing how they fit. The alert queue says what you have to decide. The SIEM says how big it is: which hosts, how often, how much data. The event viewer says exactly what ran on one laptop and what started it. The packet viewer shows what really crossed the wire. The intel feed and ATT&CK say whether anyone has seen this before and what to call it. Sigma leaves a better rule behind. And the report builder turns it all into words for the client. Let's see what the SIEM can search tonight.

*After it runs:*

Eight sources and 308 events. The biggest is dns.log, with 148 queries from every laptop in the office, then the firewall's session log, with 62 connections. Those two cover the whole office. The three Windows event logs and the process list come from one laptop only, acc-lt03, which tells you that someone has already pulled extra evidence from it. The alert queue and the intel feed are JSON, so the SIEM reads them too. The packet capture isn't here at all: the packet viewer reads it. Notice what this firm doesn't have: a web proxy. Laptops go straight out through the firewall, so the firewall's log is the only record of where the data went. Answer the question: dns.log.

On screen: the step text, the siem tool with the model answer.

## 2. Start of shift

Step two: start of shift. Before touching anything, hash the evidence and read the queue end to end. Twelve alerts. Write down your first guess of which ones belong together, because we'll test it.

*After it runs:*

Twelve alerts, and one host keeps coming up: acc-lt03, the practice manager's laptop. A download at 00:03, a remote access tool at 00:04, discovery commands at 00:09, a program written to ProgramData at 00:13 and a large upload at 00:46. The rest are spread across the office: an inbox rule, Windows Update, failed logons, an archive job, a new service, a new phone, and an unknown device on the Wi-Fi. That's my first guess: one intrusion on acc-lt03, and a lot of ordinary Thursday morning. Answer the question: twelve.

On screen: the step text, the Linux cell.

## 3. Work the queue

Step three: work the queue. Every alert gets a disposition and a reason that points at evidence. Severity is yours to judge. And the five alerts that belong to one intrusion should say so, so the client reads one story, not five.

*After it runs:*

The five on acc-lt03 are escalated together: AL-8401, 8403, 8404, 8408 and 8406. Now the noise, and every one of these has a reason. AL-8402, a new inbox rule, sounds alarming, because attackers love inbox rules for hiding replies. But this one moves tax-office letters into a folder called Tax Office, and it was made in Outlook on a.nguyen's own laptop from the office's own internet address. Benign. AL-8405 is Windows Update during the patch push. AL-8407 is four typing mistakes with Caps Lock on, then a good logon from the same desk. AL-8409 is the monthly archive job, and AL-8410 a service installed during the patch window, both under change numbers. AL-8411 is a new iPhone, with MFA approved, from the office. And AL-8412, an unknown Android device on the staff Wi-Fi, gets needs more information, with a question for the office manager: did someone connect a new phone today? Answer the question: acc-lt03.

On screen: the step text, the alerts tool with the model answer.

## 4. Scope it with search

Step four: scope it with search. Before you escalate, know how big it is. Which laptop sent the most data out? Where did it go, and does anyone else send data there? Who else talked to the fake support site? And what did the firewall stop? We finish by writing the cloud storage search again in KQL, to check ourselves.

*After it runs:*

acc-lt03 sent about 2.26 gigabytes out of the office. The next highest, reception, sent about five megabytes. Everyone else sent less than one. Now storage.cloudbox.example: two hosts. Reception sent two small uploads, three and a half megabytes and just over one megabyte, which fits the intel file: reception uses that cloud storage to send files to clients. acc-lt03 sent eight uploads of around 270 megabytes each. Same site, very different story. And that's the hard lesson of tonight: the data went to a site that's on the allow list. Only one client ever asked DNS for ledgerpro-support.example: 10.40.0.23, acc-lt03. And the firewall denied two things: acc-lt01 trying an outside time server, which is policy noise, and acc-lt03 trying filedrop.example, an anonymous file-sharing site, at 00:15. The KQL version gives the same two hosts. Answer the questions: acc-lt03, two, and filedrop.example.

On screen: the step text, the siem tool with the model answer.

## 5. Confirm on the host and the wire

Step five: confirm on the host and the wire. Search results are a summary, so now we confirm on the laptop's own logs and in the packet capture. Sysmon event 1 records every program that starts, with its command line, its parent, and one more field that matters a lot tonight: OriginalFileName, the name the program was built with. Renaming the file doesn't change it.

*After it runs:*

Seventeen programs started. Follow the chain. At 00:02 Chrome opened the firm's real accounting software, app.ledgerpro.example. At 00:03 it went to ledgerpro-support.example instead, a lookalike, and at 00:04 LedgerPro_Support.exe was saved and run. Its OriginalFileName is RemoteHelper.exe: it's a remote access tool. It installed a service, started an agent, and connected to relay.remotehelper.example. From 00:09, through that agent, someone ran whoami, then net use, which lists the network drives, and then counted the PDFs in S Clients 2026, the client files on the file server. At 00:12 PowerShell downloaded a zip from a software mirror, and at 00:13 svc-sync.exe appeared in ProgramData. Filter for rclone.exe and three events match: svc-sync.exe is rclone, a free tool for copying files to cloud storage, run once to test it, once towards filedrop, which the firewall blocked, and at 00:16 towards cloudbox, with eight transfers at once. Network events show eight connections to 203.0.113.150. And in the capture, the filter on the TLS server name shows eight Client Hellos to storage.cloudbox.example: the start of eight upload streams. Answer the questions: relay.remotehelper.example, svc-sync.exe, rclone.exe, 00:16, and 203.0.113.150.

On screen: the step text, the events, packets tools with the model answer.

## 6. Check the indicators

Step six: check the indicators. Pull every indicator out of the evidence and check it against the intel feed and the client's allow list. Then map the behaviour to ATT&CK, so the morning team, the client and anyone they report to use the same words.

*After it runs:*

ledgerpro-support.example is on the vendor feed as malicious: a phone scam where callers pretend to be accounting-software support, first seen on the ninth of November. So the most likely story is a phone call. j.walsh was talked into downloading a support tool. The remote-access relay is suspicious because this client doesn't use any remote access tool. The software mirror and filedrop are suspicious by category. And storage.cloudbox.example is on the client's own allow list. You can't simply block it without breaking reception's work, which is why the detection has to be about behaviour, not destination. On the heatmap: spearphishing by voice, remote access software, the three discovery techniques, ingress tool transfer for the download, masquerading for the renamed rclone, and exfiltration to cloud storage. Defang everything before it leaves your notebook. Answer the question: ledgerpro-support.example.

On screen: the step text, the ioc tool with the model answer.

## 7. Escalate

Step seven: escalate. One escalation for the whole intrusion, not one per alert. The reader is the practice principal, reading on a phone between client meetings. The ask goes first, with a time in UTC and in Brisbane time. Then severity and the fact that decided it, what we know, what we don't, and what we have and haven't changed.

*After it runs:*

The ask: approve isolating acc-lt03 now, by 01:30 UTC, half past eleven in Brisbane, ask j.walsh to stop using it, and ask her who phoned her this morning. Severity high, and the deciding fact is in one sentence: about 2.2 gigabytes of client tax files have already left, and someone outside has remote control of the laptop right now. Then the timeline, each line with its alert and its file. What we don't know: exactly which files, whether the copy has finished, and whether she gave the caller a password too. The impact says what was copied, the 2026 tax files of the firm's clients, because that's personal and financial information, and the client may have to tell people. And we say clearly: nothing has been changed on the laptop. The client decides; we give them what they need to decide.

On screen: the step text, the report tool with the model answer.

## 8. Leave a new detection behind

Step eight: leave a new detection behind. The client's upload rule, AL-8406, fired at 00:46, half an hour after the copy started, because it waits until a gigabyte has gone. We want a rule that fires before any data moves. Something the copy tool did that normal programs don't do. We write it in Sigma, test it, and write what would make it noisy.

*After it runs:*

The rule: a Sysmon process event where OriginalFileName is rclone.exe, but the file isn't called rclone.exe. A program built as rclone and running under another name is hiding. It matches three events, all svc-sync.exe, and nothing else on the laptop. The first match is the test run at 00:14:02. AL-8406 fired at 00:46:10. That's thirty-two minutes earlier, and two minutes before the copy started. The tuning note: some IT tools bundle rclone under their own name, so list those by path and signer if the client ever uses one, and watch the first week of hits in test mode. Answer the questions: three, and thirty-two.

On screen: the step text, the sigma tool with the model answer.

## 9. Shift report

Step nine: shift report. Close your shift so that the morning team can carry on without calling you. Everything open, by ID, with an owner. Everything closed, in one line each. What to watch. Who you called, and when. And how many hints you opened.

*After it runs:*

Two items stay open. The incident, with all five alert IDs and the next steps: the client isolates the laptop, and the morning analyst lists exactly which files were copied and helps the client decide who must be told. And the unknown Android device, with its question and an owner. Six alerts are closed, one line each, each with the fact that closed it. The watch list has the three bad domains, any RemoteHelper service, and the new rule in test mode. The calls have times: the practice principal at 01:18, isolation approved at 01:24, and the message to the morning lead. And the hints line, honestly.

On screen: the step text, the report tool with the model answer.

## 10. Hand in

Step ten: hand in. The notebook carries the queue, the searches, the escalation, the rule and the shift report. The rubric is on screen, including the line that takes a point for each hint.

*After it runs:*

Now it's your turn. Do it at the Practice level first, then Solo, alone, with your hints counted. Read your escalation one last time as the practice principal, on a phone, with a client waiting. If it doesn't tell her what to do in its first two lines, fix that before you hand in.

On screen: the step text.

## Wrap-up

That's the night shift. Twelve alerts with no severities, and one real intrusion: a phone call, a fake support site, a remote access tool, three discovery commands, a renamed copy tool, and two gigabytes of clients' tax files sent to a cloud storage site the firm itself allows. You scoped it with search, confirmed it on the laptop and on the wire, saw why blocking a destination wasn't enough, escalated once with the ask first, and left behind a rule that would have fired thirty-two minutes earlier, before any data moved. That's the whole SOC kit from seminars two and three, used alone, at night, for someone else's company. Next, in seminar five, Incident response, we follow an attack all the way from the first call to the boardroom. Thank you for watching.

## YouTube chapters (estimate; `python tools/teach.py demo s04-capstone-night-shift` writes the exact ones)

```
0:00 Opening
0:58 1. How the night desk works
2:39 2. Start of shift
3:32 3. Work the queue
4:58 4. Scope it with search
6:40 5. Confirm on the host and the wire
8:37 6. Check the indicators
9:56 7. Escalate
11:24 8. Leave a new detection behind
12:39 9. Shift report
13:47 10. Hand in
14:23 Wrap-up
```
