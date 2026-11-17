# Lecture script: The same hunt in KQL

Free tutorial · about 15 minutes of lab work · about 3 minutes of narration

This is what `python tools/teach.py demo t-the-same-hunt-in-kql` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice t-the-same-hunt-in-kql`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script t-the-same-hunt-in-kql` to refresh this file.

## Opening

Hello, and welcome. You've counted and pivoted in SPL. Now let's ask the very same question in KQL, the Kusto Query Language used by Microsoft Sentinel and Defender. If two languages give two different answers, one of the searches is wrong, so this is also a lesson in checking your work.

## 1. The setting

Same company, same evidence. Kestrel Logistics, the second and third of November 2026, all times in UTC. We'll search auth.log from web01, the web shop with SSH open to the internet. The question: did someone guess a password and get in?

On screen: the step text.

## 2. The same hunt in KQL

KQL reads differently from SPL. It starts with a table, here the table is called auth. Then each pipe passes the rows to an operator. where filters rows. summarize count by groups them. project picks the columns you want to see, and sort by orders them. Strings go in double quotes, and you compare with two equals signs. Here's the failure count, written in KQL.

*After it runs:*

Same answer as SPL: 203.0.113.7 is at the top, with six failed logins. Notice the count column is called count_ with an underscore at the end. That's KQL's default name, and you sort by it. Now the pivot. The second search filters for that address and a success, and projects the time, the user and the authentication method. One row, the account deploy. So both languages agree, and that's what you want. Now a small exercise for you: write down one thing that's easier in each language. Many analysts find KQL easier to read because every step names what it does, and SPL quicker to type for a fast count. There's no wrong answer; you'll meet both at work. Answer the question: six failed logins from that address.

On screen: the step text, the siem tool with the model answer.

## 3. Where next

That was one step from Seminar 2, Log search and detection as code. The full seminar has a longer video, every step at three levels, walkthrough, practice and solo, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen. If you want to try the Hacker Room, the analyst desktop where all these programs live together, the free trial is linked there too.

On screen: the step text.

## Wrap-up

To recap. KQL starts with a table and pipes it through where, summarize, project and sort. The answer must match your SPL. When it doesn't, slow down and find out why. Knowing both languages makes you useful in almost any security team. Thank you for watching.

## YouTube chapters (estimate; `python tools/teach.py demo t-the-same-hunt-in-kql` writes the exact ones)

```
0:00 Opening
0:31 1. The setting
0:47 2. The same hunt in KQL
2:16 3. Where next
2:44 Wrap-up
```
