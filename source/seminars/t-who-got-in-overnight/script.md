# Lecture script: Who got in overnight?

Free tutorial · about 25 minutes of lab work · the video runs about 9 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word.

## Opening

Welcome. Tamarind Health, a small chain of clinics, had a strange night. You will find a password-guessing attack in a Linux log using only grep, sort and uniq.

## 1. The setting

Read the setting so you know the company, the date and the time zone. Then open the evidence in the case folder.

On screen: the step text and the tool.

## 2. Linux: who was knocking

The server is open to the internet on port 22, and auth dot log records every SSH login, good or bad. Count the failures, then count them by source address. Grep dash o keeps only the address; sort, uniq dash c, sort dash r n ranks them. One address making dozens of guesses is a brute force.

On screen: the step text and the tool.

## 3. Linux: the login and what came next

A brute force only matters if it worked. Find the Accepted line, then read everything that account did afterwards. The sudo lines show each command run as root. Then check the two things an attacker leaves to come back: a scheduled job and a running process. The deploy account logs in with a key every night, and that one is normal. Compare the cron lines with what the script added.

On screen: the step text and the tool.

## 4. Where next

That is the whole shape of an intrusion in one log. Seminar 1 reads four kinds of evidence this way.

On screen: the step text and the tool.

## Wrap-up

That is the whole shape of an intrusion in one log. Seminar 1 reads four kinds of evidence this way.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:24 1. The setting
1:36 2. Linux: who was knocking
2:47 3. Linux: the login and what came next
4:00 4. Where next
```
