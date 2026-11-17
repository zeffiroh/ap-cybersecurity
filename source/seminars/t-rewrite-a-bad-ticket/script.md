# Lecture script: Rewrite a bad ticket in five minutes

Free tutorial · about 25 minutes of lab work · about 5 minutes of narration

This is what `python tools/teach.py demo t-rewrite-a-bad-ticket` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice t-rewrite-a-bad-ticket`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script t-rewrite-a-bad-ticket` to refresh this file.

## Opening

Hello, and welcome. Most security work is handed from one person to the next: helpdesk to the SOC, the SOC to the incident lead, the night shift to the morning shift. If the note is poor, the next person starts from zero, and the attack keeps running while they do. Today you'll take a ticket nobody can act on and turn it into a triage note someone can.

## 1. The setting

The setting. Kestrel Logistics, a freight company. Monday the second of November 2026. All times are UTC, and India is five and a half hours ahead. This morning a fake invoice reached three people, and the HR laptop opened it. The case folder has helpdesk ticket 88213 and last night's shift handover.

On screen: the step text.

## 2. A ticket nobody can act on

Read both notes as the person who receives them. Ask four questions. Which facts have a time and a source? Which words are guesses, like probably, maybe, or three question marks? What does the next person need that isn't there: which host, which user, which alert, what was already done? And what's wrong with a handover that says all quiet, couple of alerts, nothing major? The Linux cell prints both notes.

*After it runs:*

The ticket does have some real facts. At 09:16 the system logged that dev.kapoor reported message 4A1F21C02 as phishing, and at 09:52 the helpdesk pulled the network cable on the HR PC. Every line has a time, but no time zone. The rest is guesswork: probably spam, maybe virus, three question marks, not sure if related. It doesn't name the host or the user, says nothing about which alert fired or what was checked, and someone was told to delete the evidence. Files on the share with funny names is the most important line, and nobody followed it up. The handover is worse. All quiet, couple of alerts, nothing major names no alert and no host, and someone on the VPN from Singapore, didn't check, is a lead that was left for nobody. The morning shift can't check a single word of it. Here's a simple test for any note. It answers five questions: what fired, what I checked, what I found, what I don't know yet, and what happens next. Answer the questions: message 4A1F21C02, and 09:52.

On screen: the step text, the Linux cell.

## 3. Write the triage note

Now rewrite ticket 88213 as a triage note for alert AL-2203. Three rules make notes useful. One time zone for everything, UTC here, written every time. Every fact says where you saw it, and guesses go under what I don't know yet. And write the exact searches you ran, so the next person can repeat them without asking you. The report builder checks each section as you type: the alert ID, times with a time zone, your searches, at least one gap, a disposition and an owner.

*After it runs:*

Here is the model note, filled in. What fired: AL-2203, an Office document with macros opened from the internet, severity high, on hr-pc07, user priya.nair, at 09:02:44 UTC. What I checked, with each search written out. What I found, each fact with its source. What I don't know yet: did the other two people open the invoice, and was anything copied out? That section is never empty. Then the disposition, escalate, and who owns it now. Press Check the report and the builder ticks each section. When you try it yourself, write your own note before you look at the model answer, and download the Markdown. Answer the question: the disposition is escalate.

On screen: the step text, the report tool with the model answer.

## 4. Where next

That was one step from Seminar F, Evidence, notes and handoffs, the free foundation seminar. The full seminar has a longer video, every step at three levels, walkthrough, practice and solo, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen. If you want to try the Hacker Room, the analyst desktop where all these programs live together, the free trial is linked there too.

On screen: the step text.

## Wrap-up

To recap. A note is for the next person, not for you. One time zone, written every time. Facts with their source, guesses in their own section. Write what you ran. And always say what happens next and who owns it. Do this every time and people will want you on their shift. Thank you for watching.

## YouTube chapters (estimate; `python tools/teach.py demo t-rewrite-a-bad-ticket` writes the exact ones)

```
0:00 Opening
0:38 1. The setting
0:59 2. A ticket nobody can act on
2:42 3. Write the triage note
4:10 4. Where next
4:39 Wrap-up
```
