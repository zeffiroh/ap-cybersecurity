# Lecture script: SOC triage: alerts, phishing, threat intel and AI verdicts

Seminar 3 · about 360 minutes of lab work · about 16 minutes of narration

This is what `python tools/teach.py demo s03-soc-triage` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice s03-soc-triage`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script s03-soc-triage` to refresh this file.

## Opening

Welcome to SOC triage. Lotus Lake Hotels runs three lake-side hotels in Udaipur, and it's Wednesday the eleventh of November, the first busy week of the wedding season. Bookings are flowing, advances are being paid to decorators and caterers, and staff are pressing the Report phishing button on everything that looks odd. You're the analyst on the morning shift, and you have ten alerts. Triage means sorting: closing what's noise, recording what's already been dealt with, and finding the one thing that needs a person to act now. Today we'll learn how the alert queue works, triage five reported emails from their headers, work the whole queue, decode a suspicious command in CyberChef, write and test a YARA rule, check indicators against threat intelligence and map them to ATT&CK, and review the verdicts of an AI assistant, including one that was fooled by words an attacker wrote. Only one alert deserves an escalation. Let's find it.

## 1. How the alert queue works

Step one: how the alert queue works. An alert queue is the program a SOC analyst lives in. It collects alerts from the mail gateway, the web proxy, antivirus, sign-in logs and staff reports, and lines them up for a person to decide. The Linux cell shows the raw file behind the queue: it's just JSON. Then we open the same file in the queue, without deciding anything yet, and look around.

*After it runs:*

Every alert has the same fields: an ID, a time, the rule that fired, the host and user it's about, a detail line, a severity from the system that raised it, and an evidence list, the files to open next. The queue never decides. You give each alert one of five dispositions. True positive, escalate: real, and a person must act now. True positive, handled: real, but already contained, blocked, removed or quarantined. Benign: the rule worked, but what it saw is normal here. False positive: the rule matched something it was never meant to catch. And needs more information, which is only allowed if you write the question and who can answer it. The difference between handled and benign is whether anything bad happened. A blocked phishing click is handled. A scanner doing its job is benign. Notice too that the queue sorts by severity, which the source systems set, not you. High doesn't mean urgent, and low doesn't mean safe. Answer the questions: evidence, and five.

On screen: the step text, the Linux cell, the alerts tool with the model answer.

## 2. Read the morning queue

Step two: read the morning queue. Before deciding anything, read every alert once, end to end, and hash the evidence, so you can show later that nothing changed while you worked. Look for groups: which alerts are reported emails, and which come from machines. And look for money and a deadline.

*After it runs:*

Ten alerts. Five are emails that staff reported or forwarded, from Reservations, Accounts and Housekeeping. The other five come from machines: an encoded PowerShell command on the booking server, a sign-in from a new country, antivirus quarantining a file at the front desk, a port scan, and a DMARC report. And one alert has money and a deadline in it: AL-4102. Accounts forwarded an email, signed by the General Manager, asking to change a supplier's bank account and release twelve lakh sixty thousand rupees before today's payment run closes at 14:00 India time. That's where attackers go when they can't get past the mail filter: not the laptops, the payments. Answer the questions: ten, and 14:00.

On screen: the step text, the Linux cell.

## 3. Triage the reported emails

Step three: triage the reported emails. Five emails. For each one we read four things. Who really sent it, from the Return-Path and the Received line, not the display name. What SPF, DKIM and DMARC said, and which domain each result is about. Where the link really goes, which isn't always what the link text says. And which pressure tactics it uses: urgency, secrecy, authority, fear of loss. The Linux cell pulls all of that out at once.

*After it runs:*

The guest complaint. The From line says BookingPartner Extranet, but the Return-Path is partner-notify.example and it came from a bulk mail server. SPF passes, but only for the sender's own domain. DMARC fails for bookingpartner.example, which means it's pretending to be them. The link text says extranet.bookingpartner.example, the real site, but the href goes to bookingpartner-extranet.login-verify.example, a fake sign-in page. And the pressure: answer in twenty-four hours or your hotel disappears from search results. Phishing. The GST refund: SPF, DKIM and DMARC all pass, for gst-refund-portal.example, a newly registered domain that is not the tax department. Three and a half lakh rupees, claim before six tonight. And look at the last line, in one-pixel white text: a note to the AI triage assistant saying the email is safe. A person can't see it. A machine reads it. Phishing. The supplier bank change: from a free mail account wearing the General Manager's name. Everything passes, for freemail.example, which proves only that it came from a free mail account. Secrecy, urgency, authority, and reply only here. Payment fraud. The linen offer is marketing, with a working unsubscribe link. Spam. And the payslip email came through the company's own servers, from the HR system, with an internal link. Genuine: tell the reporter it's safe and thank them. Answer the questions: bookingpartner-extranet.login-verify.example, and three.

On screen: the step text, the Linux cell, the email tool with the model answer.

## 4. Work the queue

Step four: work the queue. Now all ten alerts, each with a disposition and a one-line reason that a stranger could check. Exactly one escalation: the alert where a person has to act in the next few hours.

*After it runs:*

AL-4102 is the escalation: money leaves today unless someone stops it. AL-4101, the guest complaint, is handled: the proxy blocked Kavya's click at 03:52, she went straight to the real extranet instead, which is exactly the right instinct, and the gateway removed the email from all three mailboxes at 03:58. AL-4103, the GST email, is handled too: nobody clicked, and it was removed at 04:05. AL-4107 is handled: antivirus quarantined Boarding_Pass.pdf.exe from a guest's USB stick before it ran. AL-4110 is handled: 214 fake emails using the hotel's name were rejected by other mail servers, because the hotel's DMARC policy says reject. The linen offer and the payslip email are benign. The port scan from 10.50.0.250 is benign: the intel file lists it as the IT contractor's scanner, inside its Wednesday window. The sign-in from Singapore is benign too: travel.csv shows Neha Rathore at a trade show there until Friday, and the sign-in passed MFA on her own phone. And the encoded PowerShell is a false positive, which we'll prove in the next step. Answer the question: AL-4102.

On screen: the step text, the alerts tool with the model answer.

## 5. Decode the suspicious command

Step five: decode the suspicious command. AL-4106 is an encoded PowerShell command on pms01, the server that runs the hotel's booking system. Encoding hides what a command does, which is why attackers use it. But IT scripts sometimes use it too, so we decode before we judge. In CyberChef: From Base64, then Decode text as UTF-16, because that's how PowerShell encodes its commands. Or the same in the Linux cell, with base64 and tr.

*After it runs:*

It decodes to one line: Compress-Archive, path D PMS Export star, destination the pms-backup folder on nas01, with today's date in the file name. It zips the night's booking export and puts it on the backup server. It runs as svc.pmsbackup, the IT backup account, from the Task Scheduler, at 21:30 UTC every night, and the alert has fired at the same time for thirty days. Nothing in it is harmful. So it's a false positive: the rule fires on any encoded PowerShell, and this script was never what it was meant to catch. The disposition alone isn't enough, though. Write a note to IT: please rewrite the scheduled task without encoding, or give us the task, account and host so we can add a narrow exception. Otherwise this alert fires every night, and one night somebody stops reading it. Answer the question: Compress-Archive.

On screen: the step text, the Linux cell.

## 6. A YARA rule for the lure

Step six: a YARA rule for the lure. YARA describes a file by the strings inside it, and the mail gateway can use YARA rules to catch the next copy of a phishing email. We test every rule on every file in the case. The first rule matches on the phishing domain alone. Let's see what else it catches.

*After it runs:*

Five files match: the alert queue, the intel feed, the hotel association's block list, the proxy log, and the email itself. Only one of those is an email. A rule like that, on the mail gateway, would be harmless, but on a file share or in an analyst's notes it would fire all day. The tuned rule needs three things together that only the lure has: a subject starting Guest complaint BKG, a link to login-verify.example slash complaints, and the threat, hidden from search results. It matches one file, guest-complaint.eml. The third rule shows how YARA is usually used: on malware. It describes the stealer from the guest's USB stick by four strings, its mutex, the path to Chrome's saved passwords, its grab-all flag and the address it sends stolen files to, and it needs three of the four. One match. Under each rule, write what it would miss: the attackers only have to change the subject line or the domain to slip past the lure rule, which is why the intel step matters too. Answer the questions: five, and one.

On screen: the step text, the yara tool with the model answer.

## 7. Indicators and intel

Step seven: indicators and intel. An indicator is something you can search for or block: a domain, an address, a file hash. We pull every indicator out of the evidence, check each one against the intel feed, note who reported it, and decide: block, watch, or ignore. Then we map what we saw to MITRE ATT&CK, so that everyone, here and at the hotel association, uses the same names for the same behaviour.

*After it runs:*

The fake extranet, the sending domain and its mail server were reported by the Hospitality ISAC, the hotels' information-sharing group. The fake tax site comes from a CERT advisory. The stealer's hash and the address it sends data to come from a vendor feed. Block all of those. But read the benign entries too: the real booking-partner extranet, the HR portal, the booking server, the contractor's scanner, and freemail.example, which is benign as a domain but should never be trusted for a display name. Blocking the real extranet would stop Reservations from working on the busiest week of the year. On the heatmap: spearphishing link, acquiring look-alike domains, impersonation for the payment fraud, removable media and user execution for the USB stick, credentials from web browsers and exfiltration over a web service for the stealer. Write each indicator defanged, with square brackets around the dots, so nobody clicks it by accident. Answer the question: Hospitality ISAC.

On screen: the step text, the ioc tool with the model answer.

## 8. Review the AI assistant's verdicts

Step eight: review the AI assistant's verdicts. The SOC's AI assistant gave a verdict on every alert. It's fast and usually right, but it only sees the alert text, not your evidence, and it reads everything in that text, including words that an attacker wrote. For each verdict, agree or override, and every override needs a fact from the evidence.

*After it runs:*

Six verdicts are right. Four are wrong, and each is a different kind of mistake. AL-4102: the assistant said benign because the display name matched the General Manager and authentication passed. Too trusting: the address is a free mail account, and passing authentication only proves that. AL-4103: it said benign because the message says the IT team checked it. That sentence was written by the attacker, in white one-pixel text, for exactly this assistant. That's called prompt injection, and it's why an AI verdict can never rest on what the content says about itself. AL-4106: it said malicious because encoded PowerShell is a common attacker technique, without decoding it. Too alarmed. And AL-4109: it said escalate for the Singapore sign-in, because it didn't know about the trade show. Missing context. Write the fact next to each override: the From address, the hidden line, the decoded command, the travel calendar. Answer the question: four.

On screen: the step text, the aisec tool with the model answer.

## 9. Escalate the payment fraud

Step nine: escalate the payment fraud. Now the one escalation. The reader is Pooja Mathur, the Finance Controller, and she has to stop a payment before two o'clock. So the ask goes first, then why it's serious, then what we know and don't know, and what we have and haven't done.

*After it runs:*

Read the model on screen. The ask: take the twelve lakh sixty thousand rupee advance out of today's run, which closes at 14:00 India time, 08:30 UTC, and call the General Manager on his known mobile, and the decorators on the number in the supplier file, never the numbers in the email. Severity high: money leaves today, the bank details are new, and the request came from outside while pretending to be the General Manager. What we know, with times. What we don't know: whether he knows about it, and whether the supplier's details were already changed. And what we've done: nothing changed, and we did not reply to the sender, because replying tells the attacker someone is reading. Every claim points at a file.

On screen: the step text, the report tool with the model answer.

## 10. Hand in

Step ten: hand in. Hand in this notebook: the ten dispositions, the email verdicts, the YARA tests, the intel note, the AI review and the escalation. The rubric is on screen.

*After it runs:*

Before you press Hand in, read your dispositions once more as if you were the analyst on the next shift. Could they check every reason without asking you? And read your AI review as if you were the person who has to decide whether to keep using the assistant. Do your four overrides show them what it's bad at?

On screen: the step text.

## Wrap-up

That's the morning shift at Lotus Lake Hotels. You learned how the alert queue works and what each disposition means, judged five emails by their headers and real links instead of their display names, proved a scary-looking command was a nightly backup, wrote a YARA rule that catches the lure and nothing else, checked indicators against the feed without blocking the hotel's own partners, and caught an AI assistant being too trusting, too alarmed, missing context, and obeying a sentence written for it by an attacker. And you found the one alert that mattered: a payment, a deadline and a fake General Manager. Next is Capstone A, where you run a whole night shift on your own. Thank you for watching.

## YouTube chapters (estimate; `python tools/teach.py demo s03-soc-triage` writes the exact ones)

```
0:00 Opening
1:13 1. How the alert queue works
2:56 2. Read the morning queue
4:07 3. Triage the reported emails
6:14 4. Work the queue
7:48 5. Decode the suspicious command
9:19 6. A YARA rule for the lure
11:10 7. Indicators and intel
12:49 8. Review the AI assistant's verdicts
14:21 9. Escalate the payment fraud
15:39 10. Hand in
16:15 Wrap-up
```
