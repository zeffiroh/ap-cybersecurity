# Lecture script: Write a YARA rule for a lure

Free tutorial · about 15 minutes of lab work · about 4 minutes of narration

This is what `python tools/teach.py demo t-a-yara-rule-for-a-lure` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice t-a-yara-rule-for-a-lure`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script t-a-yara-rule-for-a-lure` to refresh this file.

## Opening

Hello, and welcome. YARA is a pattern-matching tool that security teams use to find files: malware, phishing emails, anything with a recognisable fingerprint. Today you'll write a YARA rule that catches this morning's phishing lure and nothing else. The hard part isn't catching the bad file. It's not catching the good ones.

## 1. The setting

The setting. Lotus Lake Hotels, three lake-side hotels in Udaipur, Wednesday the eleventh of November 2026, the start of the wedding season. This morning the reservations team reported a fake guest complaint: an email pretending to come from a booking website, with a link to a fake sign-in page on login-verify.example. The mail gateway can scan every incoming email with a YARA rule, so a good rule stops the next one. The case folder has the lure, guest-complaint.eml in the reported folder, and plenty of other files that mention it.

On screen: the step text.

## 2. A YARA rule for the lure

A YARA rule has three parts. meta, which describes the rule. strings, the text or bytes to look for. And condition, which says how many of those strings must be found. The first rule is the obvious one: match anything that mentions the phishing domain. We'll test it on every file in the case, not just the email, because that's how you find out what else it catches.

*After it runs:*

Five files match. Only one of them is an email. The others are the alert queue, the threat-intel feed, the hotel association's block list and the proxy log. They all mention the domain because they're about the attack. On a mail gateway, this rule would be fine, but in a file scanner or across an analyst's notes it would fire all day, and analysts stop trusting rules that cry wolf. Now the tuned rule. It needs three things together that only the lure email has: a subject starting Guest complaint BKG, a link to login-verify.example slash complaints, and the threat in the body, hidden from search results. The condition says all of them. Press Test. It matches one file: guest-complaint.eml. That's the rule you'd ship. The third rule shows how YARA is usually used: on malware. The antivirus quarantined a file at the front desk, Boarding_Pass.pdf.exe, a password stealer left on a guest's USB stick. The rule describes it by four strings from inside the program: its mutex name, the path to Chrome's saved passwords, its grab-all switch, and the address it sends stolen files to. The condition says three of them, so one changed string doesn't let a new version slip past. One match. Finally, write one line for each rule on what it would miss. For the tuned rule: a new email with a different subject or domain. That's the trade-off: tighter rules make fewer false alarms but miss more variations. Answer the questions: five files for the domain rule, one for the tuned rule.

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
1:07 2. A YARA rule for the lure
3:32 3. Where next
4:02 Wrap-up
```
