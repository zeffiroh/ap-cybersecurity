# Lecture script: A risk register row a board understands

Free tutorial · about 15 minutes of lab work · about 3 minutes of narration

This is what `python tools/teach.py demo t-a-risk-register-row` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice t-a-risk-register-row`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script t-a-risk-register-row` to refresh this file.

## Opening

Hello, and welcome. Security teams find far more problems than any company can fix at once. A risk register is how leadership decides what to fix first, what to accept, and who is responsible. Today you'll fix a weak register and see what makes each row useful.

## 1. The setting

The setting. Banyan Learning in Pune, which runs a school fees and learning app. Its new payment feature, Parent Pay, launches on the fourth of December 2026, and we're doing the security review before launch. The case folder has the product team's first risk register and the threat model.

On screen: the step text.

## 2. Build the risk register

The product team's first register has holes. Some rows have no owner, some have no treatment, and one high risk is accepted with nobody's name on it. Each row needs: the asset, the threat, the weakness, a likelihood and an impact from one to five, a treatment, a control, an owner and a date. Likelihood times impact gives the score, and fifteen or more is high. The risk tool checks every row and flags any high risk that's accepted without sign-off. Watch it load the fixed register.

*After it runs:*

Let's read it from the top. The Fees API can be sent a fake payment confirmation, because the payment webhook isn't signed. Likelihood five, impact five, score twenty-five, the worst risk here. Treatment: mitigate, by verifying the payment gateway's signature and confirming with the gateway. Owner Sana Pillai, due the first of December, before launch. Next, the fee amount changed by the parent, sixteen. Then two at fifteen: refund fraud through a stolen staff login on the admin console, and an exploit of the outdated web framework. Four high risks, sitting in the red corner of the heat map. Notice every row now has a named person and a date. And look at treatment. Accept is a real choice, but it belongs to someone senior enough to pay for the consequence. A high risk accepted without leadership's sign-off is the tool's red flag, because it usually means nobody actually decided. Answer the question: four high risks.

On screen: the step text, the risk tool with the model answer.

## 3. Where next

That was one step from Seminar 10, Design, risk and audit. The full seminar has a longer video, every step at three levels, walkthrough, practice and solo, a graded hand-in that I mark myself, and a certificate at the end. The links are on your screen. If you want to try the Hacker Room, the analyst desktop where all these programs live together, the free trial is linked there too.

On screen: the step text.

## Wrap-up

To recap. Every risk needs a score, a treatment, a control, an owner and a date. Score it as likelihood times impact. Mitigate what you can before launch, and when you accept a risk, get the right person's name on it. A register like this turns a list of worries into decisions. Thank you for watching.

## YouTube chapters (estimate; `python tools/teach.py demo t-a-risk-register-row` writes the exact ones)

```
0:00 Opening
0:29 1. The setting
0:49 2. Build the risk register
2:34 3. Where next
3:02 Wrap-up
```
