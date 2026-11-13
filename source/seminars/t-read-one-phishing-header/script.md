# Lecture script: Read one phishing header

Free tutorial · about 15 minutes of lab work · the video runs about 6 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word.

## Opening

Welcome. Five emails were reported. For each one you decide: phishing, payment fraud, spam or genuine, and you prove it from the headers.

## 1. The setting

Read the setting so you know the company, the date and the time zone. Then open the evidence in the case folder.

On screen: the step text and the tool.

## 2. Triage the reported emails

For every email, read who really sent it: the Return-Path and the Received line, not the display name. Read what SPF, DKIM and DMARC said. Hover the link to see where it really goes. In password-expiry the link text shows the company sign-in address, but the href goes somewhere else. In bank-details the display name says CFO, the address is a free mail account, and SPF, DKIM and DMARC all pass for that free mail domain, because passing only proves the free mail service sent it. Name the pressure tactics too: urgency, authority, secrecy. Then write the verdict.

On screen: the step text and the tool.

## 3. Where next

Verdict plus evidence is a triage note. Seminar 3 turns this into a full phishing and alert-triage routine.

On screen: the step text and the tool.

## Wrap-up

Verdict plus evidence is a triage note. Seminar 3 turns this into a full phishing and alert-triage routine.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:24 1. The setting
1:36 2. Triage the reported emails
2:47 3. Where next
```
