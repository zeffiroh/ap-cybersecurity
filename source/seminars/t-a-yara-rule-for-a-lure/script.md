# Lecture script: Write a YARA rule for a lure

Free tutorial · about 15 minutes of lab work · about 3 minutes of narration

This is what `python tools/teach.py demo t-a-yara-rule-for-a-lure` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice t-a-yara-rule-for-a-lure`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script t-a-yara-rule-for-a-lure` to refresh this file.

## Opening

Hello, and welcome. YARA is a pattern-matching tool that security teams use to find files: malware, phishing emails, anything with a recognisable fingerprint. Today you'll write a YARA rule that catches yesterday's phishing lure and nothing else. The hard part isn't catching the bad file. It's not catching the good ones.

## 1. The setting

The setting. Kestrel Logistics, Tuesday the third of November 2026, the morning after the ransomware. The attack began with an email: a fake overdue invoice from a look-alike domain, kestrel-logistlcs.com. The mail gateway can scan every incoming email with a YARA rule, so a good rule stops the next one. The case folder has the lure, invoice.eml, and plenty of other files that mention it.

On screen: the step text.

## 2. A YARA rule for the lure

A YARA rule has three parts. meta, which describes the rule. strings, the text or bytes to look for. And condition, which says how many of those strings must be found. The first rule is the obvious one: match anything that mentions the look-alike domain. We'll test it on every file in the case, not just the email, because that's how you find out what else it catches.

*After it runs:*

Six files match. Only one of them is an email. The others are the alerts file, the threat-intel feed, the known-bad list, the mail log and the proxy log. They all mention the domain because they're about the attack. On a mail gateway, this rule would be fine, but in a file scanner it would raise five false alarms, and analysts stop trusting rules that cry wolf. Now the tuned rule. It needs three things that only the lure email has: the exact subject line, the invoice path in the link, and the threat in the body, service suspension. The condition says all of them. Press Test. It matches one file: invoice.eml. That's the rule you'd ship. The third rule is for the malware itself, svchost-upd.exe, using strings from inside the program: its mutex name, the file extension it adds, the ransom note's name and a command-line switch. The condition says three of them, so one changed string doesn't let a new version slip past. Finally, write one line for each rule on what it would miss. For the tuned rule: a new email with a different subject. That's the trade-off: tighter rules make fewer false alarms but miss more variations. Answer the questions: six files for the domain rule, one for the tuned rule.

On screen: the step text, the yara tool with the model answer.

## 3. Where next

That was one step from Seminar 3, SOC triage: alerts, phishing, threat intel and AI verdicts. The full seminar has a longer video, every step at three levels, walkthrough, practice and solo, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen. If you want to try the Hacker Room, the analyst desktop where all these programs live together, the free trial is linked there too.

On screen: the step text.

## Wrap-up

To recap. A YARA rule is meta, strings and a condition. Always test on every file you have, not just the bad one. Pick strings that only the bad thing has, and say what the rule would miss. That's how a rule earns the team's trust. Thank you for watching.

## YouTube chapters (estimate; `python tools/teach.py demo t-a-yara-rule-for-a-lure` writes the exact ones)

```
0:00 Opening
0:31 1. The setting
0:57 2. A YARA rule for the lure
3:05 3. Where next
3:35 Wrap-up
```
