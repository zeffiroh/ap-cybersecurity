# Lecture script: Evidence, notes and handoffs

Free seminar · about 120 minutes of lab work · the video runs about 8 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word, so a recording made with `./teach demo` already has subtitles.

## Opening

Welcome to Evidence, notes and handoffs. This is the free seminar, and it's about the skill every security job runs on: writing things down so the next person can act. Today we take one real case, a fake invoice that turned into ransomware at Kestrel Logistics, and a helpdesk ticket nobody can use. By the end you'll have rewritten it three ways: as a triage note, as an escalation, and as a shift handover. Everything runs in your browser. Let's start with the ticket.

## 1. A ticket nobody can act on

Here is ticket 88213, exactly as the helpdesk left it. Read it with me. "Probably spam." "Maybe virus." "Not sure if related." Every line is a guess, and not one line says which host, which user or which alert. Below it is last night's handover: "all quiet, nothing major". Keep both open. Our job is to replace every guess with a fact, a time and the place we saw it.

On screen: the step text, the Linux cell.

## 2. Find the facts behind the ticket

Facts come from evidence. First the mail log: we search for the message ID dev.kapoor reported, and it shows the email went to three people. Then the proxy log: one address, 10.20.0.14, downloaded the invoice successfully, and a second machine was blocked. The Python cell turns the proxy's epoch times into UTC, so every fact in our notes uses one time zone.

On screen: the step text, the Linux cell, the Python cell.

## 3. What ran on the PC

"HR PC slow" isn't evidence. The process list is. Follow the parent column: Word started cmd.exe, which started a hidden PowerShell, which started a program called svchost-upd in the Public folder. The real svchost lives in System32 and runs as SYSTEM. This one is pretending. And at 09:41 the same program reached the file share.

On screen: the step text, the Python cell.

## 4. Write the triage note

Now we write. The report builder has six sections and checks each one as we type: an alert ID, times with a time zone, the exact searches we ran, at least one thing we don't know, a disposition and an owner. Watch the model note. The "What I don't know yet" section is never empty, and every fact says where it came from.

On screen: the step text, the tool with the model answer.

## 5. Escalate

An escalation is read in ten seconds by someone who has just been woken up, so the ask goes first: what we need, from whom, by when. Then the severity and the one fact that decided it: files on the share are being encrypted right now. The Linux cell counts the encrypted files and hashes the evidence, and we say where it's saved, so nothing gets lost.

On screen: the step text, the Linux cell, the tool with the model answer.

## 6. Work the queue before you hand over

Before handing over, we work the whole queue. Ten alerts. Some belong to the incident, and some are ordinary noise: the Singapore sign-in is the company VPN exit, and the antivirus update fixed itself. Each one gets a disposition and one line of reason a stranger could check. The queue then writes a handover for us.

On screen: the step text, the tool with the model answer.

## 7. Write the shift handover

Last night's note said "all quiet". Ours lists every open item by ID with the next step and its owner, what we closed, what to watch, who we called and when, and the temporary blocks someone must remember to review. A handover like this lets the next shift start working instead of starting over.

On screen: the step text, the tool with the model answer.

## 8. Hand in

Your hand-in is these three pieces of writing. Your teacher scores them with the rubric on screen, and the certificate follows once it's scored. Before you press Hand in, read each piece aloud once. If a sentence needs you to explain it, rewrite it.

On screen: the step text.

## Wrap-up

That's the seminar. You turned a ticket that said "probably spam" into a triage note with facts and times, an escalation someone can decide on in ten seconds, and a handover that leaves nothing behind. Those three pieces are your hand-in. Use the Practice level to write them yourself with hints, then the Solo level without. In the next seminar we take the same habits into log search and detection rules.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:35 1. A ticket nobody can act on
1:24 2. Find the facts behind the ticket
2:25 3. What ran on the PC
3:05 4. Write the triage note
3:56 5. Escalate
5:09 6. Work the queue before you hand over
5:59 7. Write the shift handover
6:49 8. Hand in
7:14 Wrap-up
```
