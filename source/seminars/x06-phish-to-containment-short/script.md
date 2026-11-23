# Lecture script: Simulation: Phish to containment (short)

Free simulation · about 15 minutes of lab work · about 2 minutes of narration

This is what `python tools/teach.py demo x06-phish-to-containment-short` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice x06-phish-to-containment-short`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script x06-phish-to-containment-short` to refresh this file.

## Opening

Hello, and welcome to a free simulation. For the next ten minutes you're the SOC analyst on the Monday morning shift at Kestrel Logistics. A phishing email has been reported, and malware is already running on one laptop. The clock runs twice as fast as real time, so watch how I work it from the first message to containment.

## 1. The report

It's 09:16. The SOC lead hands me the case in chat. First, the email itself. In Mail, the From line says Kestrel Logistics Accounts, but read the domain letter by letter.

*After it runs:*

kestrel-logistlcs, with an L instead of an i. A look-alike domain. Receiving it isn't the incident, though. Opening it is. So the next question is who downloaded the document.

On screen: the step text, the Linux cell.

## 2. Who opened it

The web proxy logs every download. In a terminal I search proxy.log for the look-alike domain.

*After it runs:*

One success: 10.20.0.14, hr-pc07, Priya Nair's HR laptop, fetched the invoice document. Another laptop tried later and the proxy blocked it. Meanwhile IT asks in chat whether to restart Priya's laptop. The answer is no: restarting wipes memory, which is evidence.

On screen: the step text, the Linux cell.

## 3. Contain, then escalate

Contain first, investigate second. In the Remote desktop I open hr-pc07 and press Isolate from the network. The laptop stays on, but it can't reach the file server any more. Then Tickets: alert AL-2203, a note with what fired, what I found, what I did and what I don't know yet, and Escalate.

*After it runs:*

Contained before 09:41, so the HR share is safe, and that's the bonus. The debrief shows the score and every action with its story time. The full simulation, with Labs, goes further: who else got the email, the process chain from Word to the malware, ending it, and the hand-over to your lead.

On screen: the step text.

## Wrap-up

That's a SOC morning in ten minutes: read carefully, find who actually opened it, contain without destroying evidence, and hand on a note someone can act on. Now it's your turn. Open it in the Hacker Room and beat 09:41. When you want the whole morning, the full simulation is in Labs, and Seminar F, the free seminar, teaches the notes and the hand-over.

## YouTube chapters (estimate; `python tools/teach.py demo x06-phish-to-containment-short` writes the exact ones)

```
0:00 Opening
0:34 1. The report
1:02 2. Who opened it
1:29 3. Contain, then escalate
2:11 Wrap-up
```
