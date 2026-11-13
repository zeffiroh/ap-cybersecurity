# Lecture script: Write a YARA rule for a lure

Free tutorial · about 15 minutes of lab work · the video runs about 6 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word.

## Opening

Welcome. A YARA rule describes what a file looks like. In this tutorial you write one that catches a phishing lure and nothing else.

## 1. The setting

Read the setting so you know the company, the date and the time zone. Then open the evidence in the case folder.

On screen: the step text and the tool.

## 2. A YARA rule for the lure

The first rule matches on the lure's domain alone. Run it against every file in the case and see what else it catches: the threat-intel feed and the proxy log mention that domain too, so it is too loose. A rule for email should need things only the email has: the subject line, the link path and the threat wording. Add all three as strings, require all of them in the condition, and test again. One match, on the right file, is the goal. A rule that fires on the wrong file wastes an analyst's night.

On screen: the step text and the tool.

## 3. Where next

Tight rules are trusted rules. Seminar 3 puts this next to alert triage, threat intelligence and checking an AI's verdicts.

On screen: the step text and the tool.

## Wrap-up

Tight rules are trusted rules. Seminar 3 puts this next to alert triage, threat intelligence and checking an AI's verdicts.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:24 1. The setting
1:36 2. A YARA rule for the lure
2:47 3. Where next
```
