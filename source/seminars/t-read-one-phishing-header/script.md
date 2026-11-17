# Lecture script: Read one phishing header

Free tutorial · about 15 minutes of lab work · about 4 minutes of narration

This is what `python tools/teach.py demo t-read-one-phishing-header` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice t-read-one-phishing-header`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script t-read-one-phishing-header` to refresh this file.

## Opening

Hello, and welcome. Five emails were reported to the security team this morning. Your job is to decide which ones are dangerous, and to prove it from the email itself, not from a feeling. By the end you'll read a header the way an analyst does.

## 1. The setting

The setting. Kestrel Logistics, Tuesday the third of November 2026, the morning after a ransomware attack. Staff are nervous and reporting everything, which is good. All times are UTC. The reported emails are in the reported folder of the case, and the invoice that started yesterday's attack is there too, invoice.eml.

On screen: the step text.

## 2. Triage the reported emails

For each email, check four things. One: who really sent it. The From line is easy to fake, so also read the Return-Path, where bounces go, and the Received lines, which servers it passed through. Two: what SPF, DKIM and DMARC said. These are the checks the receiving mail server ran on the sender's domain. Three: where the link really goes, not what the link text says. Four: the pressure tactics, urgency, secrecy and authority. The Linux cell prints the sender lines, the authentication results and the real link target.

*After it runs:*

Let's go through them. The HR newsletter comes from hr at kestrel-logistics.com, the Return-Path matches, and SPF, DKIM and DMARC all pass. Genuine. The webinar comes from an events company through a bulk mailer. It's not dangerous, just unwanted: spam. Now password-expiry.eml. The From line says Kestrel IT Service Desk, but the Return-Path is a different domain, the Reply-To is a free mail account, SPF soft-failed, and DKIM and DMARC failed. And the link: the text says sso.kestrel-logistics.com, but the real address in the href is kestrel-sso.login-check.example. That's phishing for passwords, with a two-hour deadline to make you hurry. bank-details.eml is the clever one. Every check passes. But look at the address: the display name says the CFO, and the address is a free mail account, and the checks pass for that free mail domain, not for Kestrel. It asks for a supplier's bank details to change before 3 pm, urgent and confidential. That's payment fraud, called business email compromise. Passing checks only prove who owns the sending domain, not who the person is. Last, the invoice from kestrel-logistlcs.com. Read it slowly: logistlcs, with an L where the i should be. A look-alike domain. Phishing. The email tool lets you mark each verdict and checks you. Answer the questions: the real host is kestrel-sso.login-check.example, and three of the five are phishing or payment fraud.

On screen: the step text, the Linux cell, the email tool with the model answer.

## 3. Where next

That was one step from Seminar 3, SOC triage: alerts, phishing, threat intel and AI verdicts. The full seminar has a longer video, every step at three levels, walkthrough, practice and solo, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen. If you want to try the Hacker Room, the analyst desktop where all these programs live together, the free trial is linked there too.

On screen: the step text.

## Wrap-up

To recap. The display name is decoration. Read the address, the Return-Path and the Reply-To. SPF, DKIM and DMARC tell you who owns the sending domain, not whether the person is who they claim. Hover over every link and read the real target. And when an email pushes you to hurry or keep a secret, slow down. Thank you for watching.

## YouTube chapters (estimate; `python tools/teach.py demo t-read-one-phishing-header` writes the exact ones)

```
0:00 Opening
0:29 1. The setting
0:49 2. Triage the reported emails
3:02 3. Where next
3:32 Wrap-up
```
