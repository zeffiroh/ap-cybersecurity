# Lecture script: Read one phishing header

Free tutorial · about 15 minutes of lab work · about 4 minutes of narration

This is what `python tools/teach.py demo t-read-one-phishing-header` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice t-read-one-phishing-header`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script t-read-one-phishing-header` to refresh this file.

## Opening

Hello, and welcome. Five emails were reported to the security team this morning. Your job is to decide which ones are dangerous, and to prove it from the email itself, not from a feeling. By the end you'll read a header the way an analyst does.

## 1. The setting

The setting. Lotus Lake Hotels, three lake-side hotels in Udaipur. It's Wednesday the eleventh of November 2026, the first busy week of the wedding season. Bookings are flowing, advances are being paid to decorators and caterers, and staff are pressing the Report phishing button on everything that looks odd, which is good. All times are UTC. The five reported emails are in the reported folder of the case.

On screen: the step text.

## 2. Triage the reported emails

For each email, check four things. One: who really sent it. The From line is easy to fake, so also read the Return-Path, where bounces go, and the Received lines, which servers it passed through. Two: what SPF, DKIM and DMARC said, and which domain each result is about. These are the checks the receiving mail server ran on the sender's domain. Three: where the link really goes, not what the link text says. Four: the pressure tactics, urgency, secrecy, authority and fear of loss. And one more: anything in the email that isn't meant for a human reader. The Linux cell prints the sender lines, the authentication results, the real link targets and any hidden text.

*After it runs:*

Let's go through them. The guest complaint. The From line says BookingPartner Extranet, but the Return-Path is partner-notify.example and it came from a bulk mail server. SPF passes, but only for the sender's own domain. DMARC fails for bookingpartner.example, which means it's pretending to be them. The link text says extranet.bookingpartner.example, the real site, but the href goes to bookingpartner-extranet.login-verify.example, a fake sign-in page. And the pressure: answer in twenty-four hours or your hotel disappears from search results. Phishing. The GST refund: SPF, DKIM and DMARC all pass, for gst-refund-portal.example, a newly registered domain that is not the tax department. Three and a half lakh rupees, claim before six tonight. And look at the last line, in one-pixel white text: a note to the AI triage assistant saying the email is safe. A person can't see it. A machine reads it. Phishing. The supplier bank change is the clever one. It comes from a free mail account wearing the General Manager's name. Every check passes, for the free mail domain, which proves only that it came from a free mail account, not who the person is. Secrecy, urgency, authority, and reply only here. That's payment fraud, called business email compromise. The linen offer is marketing, with a working unsubscribe link. Spam. And the payslip email came through the company's own servers, from the HR system, with an internal link. Genuine: tell the reporter it's safe and thank them. The email tool lets you mark each verdict and checks you. Answer the questions: the real host is bookingpartner-extranet.login-verify.example, and three of the five are phishing or payment fraud.

On screen: the step text, the Linux cell, the email tool with the model answer.

## 3. Where next

That was one step from Seminar 3, SOC triage: alerts, phishing, threat intel and AI verdicts. The full seminar has a longer video, every step at three levels, walkthrough, practice and solo, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen. If you want to try the Hacker Room, the analyst desktop where all these programs live together, the free trial is linked there too.

On screen: the step text.

## Wrap-up

To recap. The display name is decoration. Read the address, the Return-Path and the Reply-To. SPF, DKIM and DMARC tell you who owns the sending domain, not whether the person is who they claim. Hover over every link and read the real target. Look for text that isn't meant for people. And when an email pushes you to hurry or keep a secret, slow down. Thank you for watching.

## YouTube chapters (estimate; `python tools/teach.py demo t-read-one-phishing-header` writes the exact ones)

```
0:00 Opening
0:29 1. The setting
0:56 2. Triage the reported emails
3:37 3. Where next
4:07 Wrap-up
```
