# Lecture script: The same hunt in KQL

Free tutorial · about 15 minutes of lab work · about 3 minutes of narration

This is what `python tools/teach.py demo t-the-same-hunt-in-kql` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice t-the-same-hunt-in-kql`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script t-the-same-hunt-in-kql` to refresh this file.

## Opening

Hello, and welcome. You've counted and pivoted in SPL. Now let's ask the very same question in KQL, the Kusto Query Language used by Microsoft Sentinel and Defender. If two languages give two different answers, one of the searches is wrong, so this is also a lesson in checking your work.

## 1. The setting

Same company, same evidence. Chandni Textiles in Surat, Monday the ninth of November 2026, all times in UTC. We'll search auth.log from shop01, the online shop with SSH open to the internet. The question: did someone guess a password and get in?

On screen: the step text.

## 2. The same hunt in KQL

KQL reads differently from SPL. It starts with a table. The table is named after the file, so auth.log becomes auth. Then each pipe passes the rows to an operator. where filters rows. summarize count by groups them. project picks the columns you want to see, and sort by orders them. Strings go in double quotes, and you compare with two equals signs. Here's the failure count, written in KQL.

*After it runs:*

Same answer as SPL: 203.0.113.45 is at the top, with eleven failed logins. Notice the count column is called count_ with an underscore at the end. That's KQL's default name, and you sort by it. Now the pivot. The second search filters for that address and a success, and projects the time, the user and the authentication method. One row: catalog, with a password, at 19:20. So both languages agree, and that's what you want. If they didn't, one of the searches would be wrong. Now a small exercise for you: write down one thing that's easier in each language. Many analysts find SPL quicker to type for a fast count, and KQL easier to read back a week later because every step names what it does. There's no wrong answer; you'll meet both at work. If you want to practise full KQL, the free KC7 game and the free Azure Data Explorer help cluster both run it. Answer the question: eleven failed logins from that address.

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
0:48 2. The same hunt in KQL
2:34 3. Where next
3:02 Wrap-up
```
