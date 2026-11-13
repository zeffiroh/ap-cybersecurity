# Lecture script: Design, risk and audit

Seminar 10 · about 360 minutes of lab work · the video runs about 5 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word, so a recording made with `./teach demo` already has subtitles.

## Opening

Welcome to Design, risk and audit. The cheapest security bug is the one that never ships. Banyan Learning wants to launch Parent Pay in three weeks: parents pay school fees in the app, and get receipts by SMS. Today you're the security reviewer. You'll threat-model the design, decide what has to change before launch, put the risks in a register the leadership signs, show an auditor which controls exist, write an honest exception for one that doesn't, and decide whether to trust the SMS vendor.

## 1. Read the design like a reviewer

A review starts with questions. What's new: the Fees API. What's someone else's: PayGate takes the card, TextBridge sends the SMS. Where is money decided? Worryingly, partly on the parent's phone: the amount comes from the app, and the webhook that says paid isn't signed. And the logs keep everything for ninety days.

On screen: the step text, the Linux cell.

## 2. Threat-model it with STRIDE

Now the model: four outsiders, two processes, one data store, eight flows, three trust boundaries. The tool lists the STRIDE threats for each. The unsigned webhook is spoofing: anyone can say paid. The amount from the app is tampering. The admin console is spoofing and elevation: shared logins, no MFA, one-click refunds. And the SMS flow is information disclosure: a child's name and class leaving to a vendor.

On screen: the step text, the tool with the model answer.

## 3. The attack tree: the cheapest way in

The attack tree asks what's cheapest. Today: send a fake webhook, cost one. Fix it by checking PayGate's signature and confirming with PayGate, and the cheapest becomes changing the amount in the app, cost two. Fix that, and it's a stolen staff login plus a one-click refund, cost five. That's where MFA and a second approver come in. Breaking PayGate itself costs fifteen, and that's PayGate's problem.

On screen: the step text.

## 4. Write the design review memo

The memo turns the model into decisions. Go live on the fourth only if three conditions are met: the webhook is signed and confirmed, the amount comes from the database, and the SMS vendor signs a data agreement with a shorter receipt. Then the shoulds, and what's good. Three musts, not twenty, or nothing ships and nothing gets fixed.

On screen: the step text.

## 5. Build the risk register

The first register had a high risk accepted by nobody. We fix every row: likelihood, impact, treatment, control, owner, date. Six risks, 4 of them high. The fake webhook is five by five. The one-click refund was accepted without sign-off; now it's mitigated with an owner in Finance. And the open vulnerability from the audit goes in too.

On screen: the step text, the tool with the model answer.

## 6. The Statement of Applicability

The Statement of Applicability. Twenty controls, each marked with evidence. Policy: met, with the approval date. Incident response: met, with the August tabletop. Most are partial, and that's normal and honest. 4 are gaps: supplier security, continuity, recovery testing, and vulnerabilities past target. An auditor trusts the company that marks its own gaps.

On screen: the step text, the tool with the model answer.

## 7. Write the audit exception

Three criticals are past target and can't all be fixed today. The exception says so honestly. What isn't met, why, the risk meanwhile, and compensating controls: the admin console only over VPN, a WAF rule, the VPN management page closed, daily log review. An owner, an expiry at the end of January, and approval by the risk owner, not just IT.

On screen: the step text.

## 8. The vendor file

The vendor file. TextBridge would get mobile numbers and, as designed, children's names and classes, so first we give them less. Their ISO certificate has expired, there's no SOC 2, and incident notice is seven working days, which can't fit inside our own six-hour and without-delay clocks. Decision: approve with conditions, in the contract, before it's signed. That's the moment you have leverage.

On screen: the step text, the tool with the model answer.

## 9. Hand in

Hand in the notebook: the threat model, the attack tree, the memo, the register, the Statement of Applicability, the exception and the vendor file. The rubric is on screen.

On screen: the step text.

## Wrap-up

That's a design review that changes the design. The threat model found the gaps before an attacker did, the memo made three of them go-live conditions, the register has owners and signatures, the Statement of Applicability tells the truth with evidence, the exception has an end date, and the vendor file ends in a decision. Next is seminar eleven, AI security, where the system you review talks back.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:37 1. Read the design like a reviewer
1:04 2. Threat-model it with STRIDE
1:37 3. The attack tree: the cheapest way in
2:10 4. Write the design review memo
2:39 5. Build the risk register
3:08 6. The Statement of Applicability
3:36 7. Write the audit exception
4:06 8. The vendor file
4:37 9. Hand in
4:55 Wrap-up
```
