# Lecture script: Breach clocks: CERT-In 6 hours, DPDP, RBI and GDPR

Seminar 6 · about 300 minutes of lab work · the video runs about 5 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word, so a recording made with `./teach demo` already has subtitles.

## Opening

Welcome to Breach clocks. This is a rehearsal set in June 2027, after India's new data protection breach rules have started. Kaveri Microfinance runs a loan app, and this morning its security team found that someone pulled thousands of customers' records out of the app's API. From the moment they noticed, clocks are running: CERT-In, the Reserve Bank, the Data Protection Board, and for a few customers, Europe. Today you'll start the clock, scope the breach, file on time while new facts arrive, and write what each reader needs.

## 1. Start the clock

Every clock starts when you noticed. The scraping began at 08:40 India time, but nobody knew. The analyst noticed at 10:20 India time, 04:50 UTC. That's the start. Six hours later, 10:50 UTC, is when CERT-In and the Reserve Bank must have their reports. Write both time zones down; people will mix them up all morning.

On screen: the step text, the Linux cell.

## 2. Scope it from the logs

Now how much. The scraper made 2060 requests, each for a different customer, one every two seconds, from 08:40 to 09:48 India time: 03:10 to 04:18 UTC. Normal app traffic asks for the signed-in customer's own record. This client had one customer's token and walked through everyone else's IDs. That's a missing ownership check.

On screen: the step text, the Linux cell.

## 3. Who is affected

To whom. Counting by country: 1932 in India, 64 in the UAE, 41 in Germany and 23 in Ireland. Every record has a name, mobile number, loan amount, the last four digits of Aadhaar and an address. That's enough for convincing fraud calls. And 64 people in the EU means GDPR may apply too.

On screen: the step text, the Linux cell.

## 4. File with CERT-In inside six hours

File now, with what we know. The form checks the detection time against the evidence, the type, and whether indicators, systems and actions are filled in. Data breach is the type. We file at 08:15 UTC, well inside six hours. Then the inbox: CERT-In asks for logs, the CISO says the flaw is three weeks old and fixed, and the press office has a journalist on the line. The update goes to CERT-In quoting the reference.

On screen: the step text, the tool with the model answer.

## 5. Every clock, in order

CERT-In is only the first clock. The tool's clock panel shows the rest: the Reserve Bank, also six hours; the Data Protection Board and every affected customer, without delay; the detailed report to the Board within 72 hours; and if GDPR applies, the Irish regulator within 72 hours. One page, one owner per row, every time in UTC.

On screen: the step text.

## 6. Decide with four regulators watching

Now the people. The CEO wants to wait for the root cause; we file on time with partial facts. The DPO asks about customers; they're told today in plain words. The journalist gets a short honest confirmation, after the regulators and customers. And the 64 people in Europe mean we check GDPR rather than ignore it.

On screen: the step text, the tool with the model answer.

## 7. The DPDP pack: the Board note and the notice

Two more readers. The Board note starts with the ask: approve fraud alerts for a year and an outside review. The notice to customers is the hardest writing of the day. What happened, what they saw, what could happen, what we did, what you can do, and a person to call. No jargon, and no line about taking privacy seriously. Read it aloud. If your grandmother couldn't act on it, rewrite it.

On screen: the step text, the tool with the model answer.

## 8. Hand in

Hand in the notebook: the CERT-In filing and update, the notification order, the Board note, the customer notice and your tabletop path. The rubric is on screen.

On screen: the step text.

## Wrap-up

That's the morning at Kaveri. The clock started at 04:50 UTC, the CERT-In and RBI reports went in before 10:50, the update followed the new facts, the Board note went out at once, and customers got a notice in words they can use. The detailed report to the Data Protection Board is due within 72 hours, and Ireland's regulator gets its own. Next is seminar seven: identity, where most of these breaches begin.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:38 1. Start the clock
1:07 2. Scope it from the logs
1:34 3. Who is affected
2:02 4. File with CERT-In inside six hours
2:38 5. Every clock, in order
3:07 6. Decide with four regulators watching
3:36 7. The DPDP pack: the Board note and the notice
4:11 8. Hand in
4:27 Wrap-up
```
