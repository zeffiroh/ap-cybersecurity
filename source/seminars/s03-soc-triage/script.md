# Lecture script: SOC triage: alerts, phishing, threat intel and AI verdicts

Seminar 3 · about 360 minutes of lab work · the video runs about 9 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word, so a recording made with `./teach demo` already has subtitles.

## Opening

Welcome to SOC triage. It's the morning after the ransomware at Kestrel Logistics, everyone is nervous, and everything is being reported. You have ten alerts. Today you'll triage five reported emails, write and test a YARA rule, check indicators against threat intel and map them to ATT&CK, decode a suspicious command in CyberChef, and check an AI assistant's verdicts. Only one alert deserves an escalation. Let's find it.

## 1. Morning queue

Read the queue end to end before deciding anything. Ten alerts: some about yesterday's incident, some new. One has money and a deadline in it, and that's usually where an attacker goes when the laptops are locked down. We hash the evidence and list the alerts.

On screen: the step text, the Linux cell.

## 2. Triage the reported emails

Five reported emails. For each, we read who really sent it: the Return-Path and the Received line, not the display name. Then SPF, DKIM and DMARC, and the real link target, which isn't always the link text. The password email's link text says the company's sign-in page, but the href goes to a look-alike. The CFO email comes from a free mail account and asks for secrecy and speed. Three are malicious, one is marketing, one is genuine.

On screen: the step text, the Linux cell, the tool with the model answer.

## 3. Work the queue

Now the whole queue. Exactly one escalation: the payment request, because a person must act before 3 pm. Yesterday's activity that's already contained is handled. The scanner in its scheduled window is benign. And two are false positives, which we'll prove in a moment.

On screen: the step text, the tool with the model answer.

## 4. Decode the suspicious command

Encoded PowerShell looks scary, which is why attackers use it. But we decode before we judge. CyberChef, From Base64, then UTF-16. It's Get-ComputerInfo writing an inventory file: IT's daily script. False positive, with a note to IT so it stops tripping the alert every morning.

On screen: the step text, the Linux cell.

## 5. A YARA rule for the lure

A YARA rule for the mail gateway. The first rule matches on the domain alone, and it also catches the intel feed and the logs. That's noise. The tuned rule needs the subject, the link path and the threat together, and it matches only the lure email. The third rule shows how YARA is usually used: on the malware's own strings.

On screen: the step text, the tool with the model answer.

## 6. Indicators and intel

We extract the indicators, check them against the feed, and note who reported each one. The feed also lists internal assets as benign, so we don't block our own intranet. Then we map the campaign to ATT&CK and write the intel note, with every indicator defanged.

On screen: the step text, the tool with the model answer.

## 7. Review the AI assistant's verdicts

The AI assistant is fast and usually right, but it only sees the alert text. We agree with seven verdicts and override three. It trusted a display name, it panicked at encoding without decoding it, and it didn't know about the VPN exit. Every override has a fact from the evidence behind it.

On screen: the step text, the tool with the model answer.

## 8. Escalate the payment fraud

The one escalation goes to the Finance controller. The ask first: stop the payment and confirm with the CFO on a known number, before 3 pm. Then why it's high, what we know and don't, and what we have not done: we did not reply to the sender.

On screen: the step text, the tool with the model answer.

## 9. Hand in

Hand in the notebook: dispositions, email verdicts, YARA tests, intel note, AI review and the escalation. The rubric is on screen.

On screen: the step text.

## Wrap-up

That's the morning shift. Ten dispositions with one escalation, five emails judged on evidence, a YARA rule that catches the lure and nothing else, an intel note with defanged indicators, and an AI review where every override had a fact behind it. Next comes Capstone A, where you run a whole night shift alone.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:28 1. Morning queue
1:13 2. Triage the reported emails
2:30 3. Work the queue
3:20 4. Decode the suspicious command
4:05 5. A YARA rule for the lure
5:46 6. Indicators and intel
6:36 7. Review the AI assistant's verdicts
7:26 8. Escalate the payment fraud
8:16 9. Hand in
8:41 Wrap-up
```
