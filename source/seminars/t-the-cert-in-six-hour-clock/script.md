# Lecture script: The CERT-In six-hour clock

Free tutorial · about 25 minutes of lab work · about 5 minutes of narration

This is what `python tools/teach.py demo t-the-cert-in-six-hour-clock` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice t-the-cert-in-six-hour-clock`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script t-the-cert-in-six-hour-clock` to refresh this file.

## Opening

Hello, and welcome. In India, many cyber incidents must be reported to CERT-In, the national computer emergency response team, within six hours. Six hours from when, though? That one question decides whether a company files on time. Today you'll start the clock correctly and file the report.

## 1. The setting

The setting, and it's marked EXERCISE, because this is a rehearsal. Kaveri Microfinance, a non-banking finance company in Bengaluru, regulated by the Reserve Bank of India. Tuesday the eighth of June 2027, after the Digital Personal Data Protection Rules' breach duties have started. All times are UTC unless marked IST, and IST is UTC plus five thirty. Before any real incident, always check the current text of each rule, because rules change.

On screen: the step text.

## 2. Start the clock

Every breach clock starts at the moment you noticed. Not when the attack began, and not when you finished investigating. Read the analyst's note, the WAF alert, and the README, and write down three times: when the attack started, when Kaveri noticed, and when the six-hour report is due, in UTC and in IST.

*After it runs:*

The analyst's note says rule 9021, one client reading many different customers' records, fired two thousand and sixty times for one address, between 08:40 and 09:48 IST. The requests used one customer's valid login but asked for other customers' records, in order, and the API returned the full KYC record each time. The rule was in log-only mode, so nothing was blocked. So the attack started at 08:40 IST, which is 03:10 UTC. But Kaveri noticed when the analyst reviewed the digest, at 10:20 IST, which is 04:50 UTC. That's the time that starts the clock. Six hours later is 10:50 UTC, or 16:20 IST. Answer the questions: noticed at 04:50 UTC, and CERT-In must be told by 10:50 UTC.

On screen: the step text, the Linux cell.

## 3. File with CERT-In inside six hours

Now file the CERT-In report with what you know. You won't know everything yet, and that's expected: file on time with partial facts, and say what you don't know. The form checks your times against the evidence and tells you what's missing. After you file, advance the clock. Replies and new facts arrive in the inbox, and when the facts change, you send an update.

*After it runs:*

Here's the filled form. The reporter is the CISO, Meenal Rao, with her contact details. The organisation and its sector, finance, regulated by the RBI. The time it occurred, 03:10 UTC, and the time it was detected, 04:50 UTC, which matches the evidence. The incident type: data breach, because personal data was taken by someone who shouldn't have it. Personal data is marked. Then the indicators, the affected system, the loan app's API, and the actions so far, such as blocking the address. It's filed before 10:50 UTC. The form also wants the attacking address, 198.51.100.66, and how many records were exposed. Then advance the clock and read the inbox. CERT-In asks you to preserve the API and WAF logs and confirm how the servers keep time. Then the CISO writes: the missing ownership check was released on the twenty-first of May, and the developers searched back to then. That changes the facts, so you send an update. Later the press office says a journalist has a sample of customer records. Every message needs an answer. Remember, CERT-In is only one clock. The DPDP Board and the RBI have their own, and the seminar covers all of them. Answer the question: data breach.

On screen: the step text, the certin tool with the model answer.

## 4. Where next

That was one step from Seminar 6, Breach clocks: CERT-In 6 hours, DPDP, RBI and GDPR. The full seminar has a longer video, every step at three levels, walkthrough, practice and solo, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen. If you want to try the Hacker Room, the analyst desktop where all these programs live together, the free trial is linked there too.

On screen: the step text.

## Wrap-up

To recap. The clock starts when you noticed, not when the attack began. Convert every time carefully between IST and UTC. File on time with what you know, say what you don't, and update when the facts change. A late perfect report is worse than an on-time honest one. Thank you for watching.

## YouTube chapters (estimate; `python tools/teach.py demo t-the-cert-in-six-hour-clock` writes the exact ones)

```
0:00 Opening
0:29 1. The setting
0:58 2. Start the clock
2:12 3. File with CERT-In inside six hours
4:06 4. Where next
4:36 Wrap-up
```
