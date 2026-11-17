# Lecture script: Your first Sigma rule

Free tutorial · about 15 minutes of lab work · about 4 minutes of narration

This is what `python tools/teach.py demo t-your-first-sigma-rule` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice t-your-first-sigma-rule`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script t-your-first-sigma-rule` to refresh this file.

## Opening

Hello, and welcome. In the next few minutes you'll write your first detection rule. A search you run once finds one attack. A rule keeps watching and finds the next one. We'll use Sigma, the open format that detection teams share, and we'll test it on a real-looking Windows log.

## 1. The setting

First, the setting. Always read it, because the time zone and the date change how you read every log. We're at Kestrel Logistics, a freight company. It's Monday the second of November 2026. A fake invoice reached three people this morning, and the HR laptop, hr-pc07, opened it. Every time in this case is in UTC. India is five and a half hours ahead. The evidence is in the case folder, and the file we need is the Windows Security log from hr-pc07, Security.jsonl, one event per line.

On screen: the step text.

## 2. From hunt to rule: your first Sigma rule

Here's the idea behind a rule. When Word or Excel starts a command shell, that's almost never a person at work. It's usually a macro in a booby-trapped document. Windows records every new process as event 4688, with the program that started it, called the parent. So our rule says: event 4688, where the parent ends in WINWORD, EXCEL or OUTLOOK, and the new process is cmd or PowerShell. Before the rule, let's count what we're searching. The first tool runs a quick SIEM search for every 4688 event on this laptop.

*After it runs:*

Fifteen process-creation events on hr-pc07. That's our haystack. Now look at the Sigma rule below it. Read it top to bottom: a title, a description, the log source, which is Windows Security, then the detection block. The selection lists the parents and the children, and the condition says the selection must match. Notice the false-positives line. A good rule tells the next analyst when it might fire on something innocent. Press Test. It matches one event: Word starting cmd.exe on hr-pc07. Now press Convert with pySigma. That's the real open-source converter, and it turns the same rule into SPL for Splunk. Compare it with the search you'd write by hand. They ask the same question. Here's the puzzle in this step: the attacker also ran PowerShell, so why didn't the rule catch it? Look at PowerShell's parent. It was cmd.exe, not Word. The chain went Word, then cmd, then PowerShell, and our rule only watches the first link. You can fix that with a second rule, cmd starting a hidden PowerShell, or one rule for each step of the chain. Answer the two questions: fifteen 4688 events, and one match.

On screen: the step text, the siem, sigma tools with the model answer.

## 3. Where next

That was one step from Seminar 2, Log search and detection as code. The full seminar has a longer video, every step at three levels, walkthrough, practice and solo, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen. If you want to try the Hacker Room, the analyst desktop where all these programs live together, the free trial is linked there too.

On screen: the step text.

## Wrap-up

Let's recap. A rule is a hunt that never sleeps. Sigma lets you write it once and convert it for any SIEM. Always test a rule on real data, count what it matches, and write down what it would miss. You found that PowerShell slipped past because its parent was cmd, and that's exactly the thinking detection engineers do every day. Thank you for watching. See you in the next one.

## YouTube chapters (estimate; `python tools/teach.py demo t-your-first-sigma-rule` writes the exact ones)

```
0:00 Opening
0:31 1. The setting
1:06 2. From hunt to rule: your first Sigma rule
3:10 3. Where next
3:38 Wrap-up
```
