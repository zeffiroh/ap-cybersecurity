# Lecture script: Your first SPL search

Free tutorial · about 15 minutes of lab work · about 3 minutes of narration

This is what `python tools/teach.py demo t-your-first-spl-search` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice t-your-first-spl-search`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script t-your-first-spl-search` to refresh this file.

## Opening

Hello, and welcome. Today you'll run your first searches in SPL, the search language of Splunk, one of the most common tools in a security operations centre. Two moves are all you need to start: count, then pivot. Let's go.

## 1. The setting

The setting first. Kestrel Logistics, a freight company. Monday the second and Tuesday the third of November 2026. All times are UTC, and India is five and a half hours ahead. The evidence is in the case folder. We'll search auth.log, the SSH and sudo log from web01, the public web shop. web01 has SSH open to the internet, so people try to guess its passwords all day. The question is whether anyone succeeded.

On screen: the step text.

## 2. SPL: count, then pivot

SPL reads from left to right. First a search that picks events, then a pipe, the vertical bar, then a command that works on those results. Our first search picks failed logins, action equals failure. Then stats count by src_ip groups them by the address they came from, and sort minus count puts the biggest at the top. That's counting. Watch the table it builds.

*After it runs:*

Look at the top row. One address, 203.0.113.7, failed far more than anyone else. That's what password guessing looks like: one source, many failures. Now the second move, the pivot. Take what you found, the address, and search for it again, this time for a success. The second search looks for Accepted logins from 203.0.113.7 and shows the time, the user and the authentication method. It found one. The address logged in as deploy. So the guessing worked. The third search asks what that account did next. Every sudo line is a command run as root, and the table shows the user, who it ran as, and the command. The one that matters reads /etc/shadow, the file that holds the password hashes for every account on the server. That's an attacker collecting passwords to crack later. So in three searches you've told the whole story: guessing, a successful login as deploy, and theft of the password hashes. A tip for when you try it yourself: click any field name in the results to add it to your search. Answer the three questions: 203.0.113.7, deploy, and /etc/shadow.

On screen: the step text, the siem tool with the model answer.

## 3. Where next

That was one step from Seminar 2, Log search and detection as code. The full seminar has a longer video, every step at three levels, walkthrough, practice and solo, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen. If you want to try the Hacker Room, the analyst desktop where all these programs live together, the free trial is linked there too.

On screen: the step text.

## Wrap-up

To recap. Count first, to find what stands out. Then pivot: take the address, the user or the host you found, and search again for the next step. Every investigation is a chain of small, simple searches like these. Thank you for watching, and try the same hunt in KQL next. It's the other big search language.

## YouTube chapters (estimate; `python tools/teach.py demo t-your-first-spl-search` writes the exact ones)

```
0:00 Opening
0:27 1. The setting
0:56 2. SPL: count, then pivot
2:51 3. Where next
3:20 Wrap-up
```
