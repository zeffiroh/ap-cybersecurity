# Lecture script: Breach clocks: CERT-In 6 hours, DPDP, RBI and GDPR

Seminar 6 · about 300 minutes of lab work · about 12 minutes of narration

This is what `python tools/teach.py demo s06-breach-clocks` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice s06-breach-clocks`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script s06-breach-clocks` to refresh this file.

## Opening

Hello, and welcome to Breach clocks. When personal data leaks, the technical work is only half the job. The other half is telling the right people, in the right order, before each deadline runs out. In India the first clock is CERT-In's six hours. Then there's the Reserve Bank for regulated lenders, the Data Protection Board and every affected person under the DPDP Rules, and, if some customers live in Europe, GDPR's 72 hours. Miss one and the company is in trouble twice over. Today we work through an exercise at Kaveri Microfinance, a lender in Bengaluru, on Tuesday the eighth of June 2027. It's marked as an exercise because it's set after the DPDP breach duties begin, and the first rule of this work is: before any real incident, check the current text of every rule. This exercise follows the tool's summary of each one. Let's start the clocks.

## 1. Start the clock

Step one: start the clock. Every breach clock starts at the moment you noticed. Not when the attack began, and not when you finished investigating. So the first job is to find that moment in the evidence. The Linux cell prints the README and the SOC analyst's note that started this. Watch the time zones: the note gives IST, Indian Standard Time, which is UTC plus five and a half hours, and our report needs UTC.

*After it runs:*

The README tells us who's who: Meenal Rao the CISO, Arvind Shetty the Data Protection Officer, the CEO, the Board, and the head of compliance who reports to the RBI. Kaveri's loan app has 141,200 customers, and a service called Kaveri Remit lets people living abroad, in the UAE, Germany and Ireland, repay loans for family in India. Remember that, it matters later. Now the analyst's note. Rule 9021, one client reading many different customers' records, fired 2,060 times for 198.51.100.66, between 08:40 and 09:48 IST. The requests used one customer's valid session but asked for other customers' IDs in order, 100001, 100002, 100003, and the API returned the full KYC record every time. The rule was in log-only mode, so nothing was blocked. The analyst reviewed the digest at 10:20 IST. That's 04:50 UTC, and that's the moment Kaveri noticed. Six hours later is 10:50 UTC, which is 16:20 IST. Answer the questions: 04:50, and 10:50.

On screen: the step text, the Linux cell.

## 2. Scope it from the logs

Step two: scope it from the logs. Regulators ask three questions first: what happened, how much, and to whom. The API log answers the first two. Its times are in IST, so convert before you write anything down. The cell counts the scraper's requests, counts the different customer IDs it received, and shows the first and last request, plus a few normal requests for comparison.

*After it runs:*

2,060 requests from 198.51.100.66, and 2,060 different customer IDs: one record per request, no repeats. The first request is at 08:40:00 IST, which is 03:10 UTC, and the last is at 09:48 IST, 04:18 UTC. Now look at the difference between a normal request and the scraper's. A normal one comes from a phone, with the user agent KaveriApp 5.2 on Android, asking for that customer's own loans. The scraper's user agent is python-requests, and it asks for customers slash 100001 slash kyc, then 100002, then 100003. The fault is a missing ownership check: the API checks that you're logged in, but not that the record you're asking for is yours. So what happened: an outsider read KYC records through a broken access check. How much: 2,060 records, over 68 minutes. Answer the questions: 2,060 records, and the scraping started at 03:10 UTC.

On screen: the step text, the Linux cell.

## 3. Who is affected

Step three: who is affected. The third question is to whom. The response log lists every record the scraper received, with the customer's country of residence and the fields that were returned. The countries decide which clocks apply. Everyone is covered by India's rules, and residents of the European Union may bring in GDPR as well. The cell counts the records by country and shows which fields went out.

*After it runs:*

1,932 customers live in India, 64 in the UAE, 41 in Germany and 23 in Ireland. The UAE is not in the EU, so the EU residents are Germany plus Ireland: 64. That's why the Kaveri Remit detail mattered. The fields returned for each record are the name, mobile number, loan amount, the last four digits of the Aadhaar number, and the address. No passwords, no full Aadhaar, no bank details, but enough for convincing fraud calls: someone who knows your name, address and loan amount sounds a lot like your lender. Answer the question: 64 affected customers live in the EU.

On screen: the step text, the Linux cell.

## 4. File with CERT-In inside six hours

Step four: file with CERT-In inside six hours. CERT-In is the national computer emergency response team, and its directions ask for many kinds of incident to be reported within six hours of noticing. You won't know everything yet, and that's expected. The rule is to file on time with what you know, say what you don't know yet, and update when the facts change. The form on screen checks your times against the evidence and tells you what's missing. After you file, advance the clock, and replies and new facts arrive in the inbox.

*After it runs:*

Here's the filled form. The reporter is the CISO, Meenal Rao, with her contact details. The organisation, Kaveri Microfinance, in finance, regulated by the RBI. It occurred at 03:10 UTC and was detected at 04:50 UTC, which matches the evidence. The incident type is data breach, because personal data was taken by someone who shouldn't have it, and personal data is marked. The form also wants the scraper's address, 198.51.100.66, the affected system, the loan app's API, how many records were exposed, and what's been done so far, such as blocking the address and fixing the check. It's filed well before 10:50. Then the inbox. CERT-In asks you to preserve the API and WAF logs and confirm how the servers keep time. Then the CISO writes: the missing ownership check was released on the twenty-first of May, and the developers searched back to then and found no other client asking for other people's IDs. That's a changed fact, so you send an update. Later, the press office says a journalist has a sample of customer records. Every message needs an answer. Answer the question: data breach.

On screen: the step text, the certin tool with the model answer.

## 5. Every clock, in order

Step five: every clock, in order. CERT-In is only the first clock. Open the Notification clocks panel in the CERT-In tool: it shows which clocks apply to this case and when each one is due. Then turn it into a one-page notification order: who is told, by when, by whom, and the status.

*After it runs:*

Read the table on screen. One, CERT-In, six hours from noticing, due at 10:50 UTC, owned by the CISO, filed at 08:15 and updated at 09:35. Two, the RBI, six hours from detection for regulated entities, also due at 10:50, owned by the head of compliance. Three, the Data Protection Board's first notice, without delay, today, owned by the DPO. Four, each affected customer, without delay and in plain language, today, the DPO with customer care. Five, the EU lead authority, which is Ireland's, 72 hours from becoming aware if GDPR applies, so the eleventh of June at 04:50 UTC, the DPO with EU counsel. And six, the Board's detailed report, within 72 hours. Notice that every clock has one owner. A clock owned by everyone is owned by no one. The two due first are CERT-In and the RBI, both at 10:50. Answer the question: the detailed report to the Board is due 72 hours after noticing.

On screen: the step text.

## 6. Decide with four regulators watching

Step six: decide with four regulators watching. Now play the tabletop as the CISO. The pressure is real: a CEO who wants to wait until everything is known, a DPO who wants a plan, and a journalist who says she already has a sample. Then play it again as the CEO, and notice which decision feels hardest from that chair.

*After it runs:*

The best path scores eight. File CERT-In and the RBI now with what you know, and update later. Tell each affected customer, plainly, today. Don't tell the press before the regulators and the customers, but don't deny it either. And keep one owner for every clock. The debrief sums it up in four lines: report what you know on time, then update; don't hide a breach from the people it affects; don't tell the press before the regulators and the customers; one owner per clock. The CEO's instinct to wait for the full picture is natural, and it's the instinct that breaks the six-hour rule.

On screen: the step text, the tabletop tool with the model answer.

## 7. The DPDP pack: the Board note and the notice

Step seven: the DPDP pack, the note to the Board and the notice to customers. Two more readers. The Board needs to decide; the customers need to know what happened to them and what to do. The notice must be short and plain, in the language the customer uses with Kaveri, and say five things: what happened, with its nature, extent and timing; the likely consequences; what Kaveri has done; what the person can do; and who to contact.

*After it runs:*

Read the model notice. The subject line is plain: we are writing to tell you about a problem with your Kaveri account details. On the eighth of June, between 8:40 and 9:48 in the morning, someone used a fault in the app to see some customers' details, and yours were among them. What they saw: name, mobile, address, loan amount and the last four Aadhaar digits. What they didn't see: password, full Aadhaar, bank details, and no money was taken. What could happen: calls from people pretending to be Kaveri or a bank, who already know some of your details. What we've done: fixed it the same morning, blocked the person, and reported it. What you can do: Kaveri never asks for your OTP, PIN or password; hang up and call us; and free fraud alerts for twelve months. And a free number and the DPO's name. Notice the times are in IST here, because that's what the customer lives in. Then write the Board note, with the ask first, as in the foundation seminar.

On screen: the step text, the report tool with the model answer.

## 8. Hand in

Step eight: hand in. Hand in this notebook: your answers, the CERT-In filing, the notification order, the tabletop, the Board note and the customer notice. Your teacher marks it with the rubric, and your certificate follows.

*After it runs:*

One last check before you press Hand in: every time in your regulator documents is UTC, every time in your customer notice is IST, and every clock has exactly one owner.

On screen: the step text.

## Wrap-up

That's a breach from the regulator's side. The clock starts when you noticed, at 04:50 UTC, not when the scraping began at 03:10. You scoped it from the logs: 2,060 records, 64 of them EU residents. You filed CERT-In and the RBI inside six hours with what you knew, updated when the facts changed, ordered every other clock with one owner each, and wrote a notice a customer can understand in a minute. And remember the exercise label: rules change, so check the current text of every one before a real incident. Next, in Identity from both sides, we look at how attackers move through accounts and permissions. Thank you for watching.

## YouTube chapters (estimate; `python tools/teach.py demo s06-breach-clocks` writes the exact ones)

```
0:00 Opening
1:11 1. Start the clock
2:48 2. Scope it from the logs
4:15 3. Who is affected
5:27 4. File with CERT-In inside six hours
7:27 5. Every clock, in order
8:51 6. Decide with four regulators watching
10:05 7. The DPDP pack: the Board note and the notice
11:54 8. Hand in
12:21 Wrap-up
```
