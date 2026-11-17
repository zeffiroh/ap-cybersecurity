# Lecture script: Design, risk and audit

Seminar 10 · about 360 minutes of lab work · about 19 minutes of narration

This is what `python tools/teach.py demo s10-design-risk-audit` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice s10-design-risk-audit`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script s10-design-risk-audit` to refresh this file.

## Opening

Hello, and welcome to Design, risk and audit. The cheapest security bug is the one that never ships. Banyan Learning, a school fees and learning app company in Pune, wants to launch a new feature called Parent Pay on Friday the fourth of December 2026. Parents open the app, see the fees due for their child, pay, and get a receipt by SMS. The design is version 0.9, dated the thirteenth of November. Kunal Desai owns it for Product, and Sana Pillai leads the engineering. Today you're the security reviewer. We'll read the design like a reviewer, threat-model it with STRIDE and an attack tree, and write a memo that says what must change before launch. Then we'll put the risks in a register that leadership signs, show an auditor which ISO 27001 controls exist and which don't, write an honest exception for one that isn't met, and decide whether to trust the SMS vendor. There are no log times in this case. The dates are the ones the documents give, on the office calendar in India.

## 1. Read the design like a reviewer

Step one: read the design like a reviewer. A design review starts with questions, not tools. For every part, ask three things. What data does it hold or carry? Who can reach it? And what has the team already decided? The decisions taken are where most of the risk hides, because nobody thinks of them as open any more. The Linux cell simply prints design.md, the document under review.

*After it runs:*

Six parts. The Banyan app, where parents sign in with their mobile number and a one-time code. The Fees API, the only part marked new, running in Banyan's own cloud account. The Student records DB and the Admin console already exist. And two parts belong to someone else. PayGate is the payment provider: the parent is sent to PayGate's page to enter card or UPI details, and Banyan never sees the card number. TextBridge is the SMS vendor. Now follow the money and the personal data. Money is decided in two places that should worry you. Decision one: the webhook, the address PayGate calls to say paid, accepts a JSON body with an order number and a status, and signature checking is marked later. Decision three: the fee amount is sent from the app. Both let the parent's side decide what the school believes about money. Decision two: any office staff member can refund with one click. Decision four: logs keep the full request body for ninety days, for debugging, so personal data sits in the logs. Decision five: TextBridge was chosen for price, and the contract isn't signed. Notice what the design doesn't say, too. Is the admin console reachable from the internet? A good reviewer writes that down as a question. Answer the questions: PayGate, and two.

On screen: the step text, the Linux cell.

## 2. Threat-model it with STRIDE

Step two: threat-model it with STRIDE. We draw the system as elements and the flows between them, with the trust boundaries, the lines where data passes from one owner or level of trust to another. STRIDE is six kinds of threat: Spoofing, pretending to be someone else. Tampering, changing data. Repudiation, denying you did something. Information disclosure. Denial of service. And Elevation of privilege, gaining rights you shouldn't have. The tool reads dataflow.txt and lists the threats that apply to each kind of element. People and companies outside get S and R. Flows get T, I and D. A data store gets T, R, I and D. Processes get all six. Our job is to write the real ones, each with a control.

*After it runs:*

The tool counts seventeen elements: four outsiders, the parent, PayGate, TextBridge and the office staff; two processes, the Fees API and the Admin console; one store, the Student records DB; seven flows; and three trust boundaries. That's forty-five possible threats. The recorded model answers eleven of them, and that's the point: you write the ones that are real for this system, not all forty-five. The worst first. The webhook from PayGate is unsigned, so anyone on the internet can pretend to be PayGate and say paid for any order. That's spoofing, and the result is tampering with the fee record. The control: check PayGate's signature, and confirm each payment with PayGate's API before marking it paid. The amount from the app is tampering: the parent can edit it, so the server must look the amount up in the database. Never trust the client. The admin console is spoofing, three shared logins and no MFA, and elevation, because any office login can refund any amount. The controls: named accounts with MFA, and a second approver for refunds over five thousand rupees. The flow to TextBridge is information disclosure: a child's name and class leave for a vendor. Cut the receipt to the amount and a reference. And the Fees API's own logs hold personal data: log events, not bodies. What does PayGate handle for us? Card data never touches Banyan, so the card number disclosure threats sit with PayGate, and Banyan's card compliance scope is much smaller. Answer the question: S, for spoofing.

On screen: the step text, the threatmodel tool with the model answer.

## 3. The attack tree: the cheapest way in

Step three: the attack tree, the cheapest way in. STRIDE gives you a list. An attack tree gives you an order. It asks one question: what's the cheapest way to reach the goal? The goal at the top is get a fee marked paid without paying. OR means any one child will do. AND means every child is needed, so their costs add up. The costs are rough effort, not rupees. The tool finds the cheapest path. Then we cut it, and see what becomes cheapest next.

*After it runs:*

Cheapest attack costs one: send a fake webhook saying order paid. One request, no skill, no stolen password. Fix it the way the threat model said: check PayGate's signature and confirm with PayGate. Delete that branch and solve again. Now the cheapest costs two: change the amount in the app to one rupee. Fix that by taking the amount from the database. Next is the AND branch: get an office staff login, cost four, plus issue a refund with one click, cost one, so five in total. That's where MFA and a second approver come in. They raise both steps at once. What's left is break into PayGate: find a flaw, nine, and use it before they patch, six, so fifteen. That one is PayGate's problem, not Banyan's. You stop when the cheapest path costs more than the money it would get. The trap is to spend the budget on the scary branch, the provider breach, while the one-request attack is still open. Answer the question: one.

On screen: the step text.

## 4. Write the design review memo

Step four: write the design review memo. The model is for us. The memo is for the people who decide. It turns the threats into decisions: ranked, short, with conditions for go-live, things to fix soon, and what's good. Write it in a Notes cell. The model memo is in the step if you get stuck, but write your own first.

*After it runs:*

Look at the shape of the model. It's to Kunal Desai and Sana Pillai, from Security, dated the sixteenth of November. The first line is the decision asked for: go live on the fourth of December only if three conditions are met; otherwise delay. Then three musts, each with its reason. One: the webhook checks PayGate's signature and the Fees API confirms each payment, because today anyone can mark any fee paid with one request. Two: the amount comes from the database, never from the app. Three: a signed data processing agreement with the SMS vendor, and the receipt cut to Fee received, rupees X, reference Y, with no child's name or class. Then the shoulds, before the end of term: MFA and named accounts on the admin console, the second approver over five thousand rupees, and logs that record events, not bodies. Accepted risks: none proposed, and the memo says the one-click refund risk is high and can't be accepted by Product alone. Then what's good: card data never touches Banyan, the database is encrypted, and parents sign in with a one-time code. Why only three musts? With twenty, nothing launches or nothing gets fixed. One more check before you send it: how long the logs are kept. It's tempting to cut ninety days to thirty, but CERT-In's directions ask for logs of ICT systems to be kept for a hundred and eighty days, in India. So keep the event log for a hundred and eighty days, and keep the personal data out of it.

On screen: the step text.

## 5. Build the risk register

Step five: build the risk register. A risk register is where the organisation writes down each risk, how likely and how bad it is, what it will do about it, who owns it and by when. The product team's first try is risk-register-banyan.csv. The tool loads it and checks every row: an owner, a control if the treatment is mitigate, a due date, and no high risk accepted without sign-off. The score is likelihood times impact, each from one to five. Fifteen or more is high.

*After it runs:*

The first register has four rows and seven things to fix. The fake webhook scores five by five, twenty-five, the highest there is, and has no treatment, no owner and no date. The refund fraud row scores fifteen, high, and is marked accept with nobody's name on it. That's the classic hole: accept looks like a decision, but nobody has decided anything. The logs row names no control, owner or date. Now the fixed register: six risks, four of them high. The webhook, twenty-five, owned by Sana Pillai, due the first of December. The amount, sixteen, the same. The refund fraud, fifteen, now mitigate, with MFA, named accounts and the second approver, owned by the Head of Finance, due the fifteenth of January 2027. Finance owns it because Finance loses the money. The logs, twelve, and the SMS receipts, twelve, both medium. And a row the product team never thought of: the admin console's outdated web framework, VM-311, open forty-one days, likelihood three, impact five, fifteen, owned by the IT manager until the thirty-first of January 2027. On the heat map, those four highs sit in the red corner. The tool says every risk has an owner, a treatment and a date. Accept is still a real choice, but it belongs to someone senior enough to pay for the consequence. Answer the question: four.

On screen: the step text, the risk tool with the model answer.

## 6. The Statement of Applicability

Step six: the Statement of Applicability. An ISO 27001 auditor asks three things: which controls apply, which are in place, and where's the evidence? The Statement of Applicability is the answer, control by control. In the compliance tool choose ISO 27001 and mark each of the twenty controls met, partly, gap or not applicable, with the evidence from controls-evidence.txt. The rule to remember: met without evidence isn't met.

*After it runs:*

The tool says forty-eight per cent met, counting partly as half: three met, thirteen partly, four gaps, none left unassessed. Three met, each with proof. 5.1, the policy, approved by the CEO on the second of February 2026, acknowledged by ninety-four per cent of staff. 5.24, the incident response plan, version two, with the CERT-In six-hour step and a tabletop held in August. And 8.7, managed anti-malware on all laptops. Thirteen partly: that's normal and honest. MFA is on for cloud and email, but not the admin console. The last restore test was the fourteenth of March. Four gaps. 5.19, supplier security: no standard clauses, and TextBridge has no data agreement. 5.29 and 5.30: no continuity plan for the apps and no recovery test this year. And 8.8, vulnerabilities: three criticals past the fifteen-day target. Parent Pay makes two of these worse. It adds a supplier, so 5.19, and it logs request bodies, so 8.15. Now switch the framework to DPDP and CERT-In. Today's work already touches security safeguards, breach reporting and children's data under the Act, and CERT-In's six-hour report and log rules. Most of the DPDP duties phase in under the Rules, with the main ones due from May 2027, so treat that mapping as an exercise and check the current text. The trap is to chase the percentage. An auditor trusts a company that marks its own gaps far more than one that marks everything met. Answer the question: four.

On screen: the step text, the compliance tool with the model answer.

## 7. Write the audit exception

Step seven: write the audit exception. Internal audit raised finding IA-2026-07 on the tenth of November. Three critical vulnerabilities are past the fifteen-day target, and fixing all three today isn't possible. An exception is how a company says not yet, honestly. It states what isn't met, why, the risk in the meantime, the compensating controls, an owner, an expiry, and who approved it. Compensating controls are the things you do instead, while the real fix waits. Write it in a Notes cell.

*After it runs:*

Read audit-finding.txt first. VM-311, the admin console's outdated web framework, forty-one days open. VM-318, remote code execution on the reporting server, thirty-eight days. VM-322, the VPN appliance firmware, thirty-three days. The finding asks for a fix, or an exception approved by the CISO and the risk owner. The model exception, EX-2026-04, gives each item a plan. VM-311's fix is in development; VM-318 is fixed on the twentieth of November; VM-322 gets a two-hour VPN outage on Saturday the twenty-eighth. From the seventeenth of November: the admin console only over the VPN, a WAF rule, a web application firewall rule, that blocks the known exploit pattern for VM-311, the VPN's management page closed to the internet, and a daily log review by the SOC. Notice the dependency. The console's protection leans on the VPN, which has its own open critical. That's why closing its management page matters. And check the list against the rule: a compensating control for each open item. The reporting server has only its fix date, three days away. A stronger answer adds a control there too, such as limiting who can reach it. The owner is the IT manager, A. Fernandes. It expires on the thirty-first of January 2027, with no renewal without a new review. Approval comes from the CISO and the Head of Finance, who owns the admin console risk. An exception without an expiry is a permanent decision dressed up as a temporary one, and auditors reject those.

On screen: the step text.

## 8. The vendor file

Step eight: the vendor file. TextBridge is the cheapest SMS vendor, twenty-two per cent below the next quote, and the contract isn't signed yet. That's the moment you have leverage. We read their questionnaire answers, received on the eleventh of November, and write the vendor review in the report builder. It must end in a decision: approve, approve with conditions, or reject.

*After it runs:*

Start with the data. TextBridge gets parents' mobile numbers and the receipt text, and as designed the receipt includes the child's first name, class and amount. So the first control costs nothing: give them less. The amount and a reference. Then separate evidence from claims. Their ISO 27001 certificate expired in June 2026, with renewal in progress. There's no SOC 2 report. The March 2026 pen test summary is available under NDA, and we haven't seen it. Storage is encrypted by our cloud host and MFA for most staff are claims, not evidence. Support staff can read message logs, which are kept two years. Data is in Mumbai with backups in Singapore, and the sub-processors include others as needed, not named. Now the incident notice: within seven working days of confirmation. Two traps in one line. Seven working days can be well over a week, and the clock starts when they confirm, not when they notice. Banyan's own clocks don't stop because the breach happened at a vendor. As usually read, CERT-In's six hours run from when Banyan notices or is told, so the vendor's notice decides how late that is. And the DPDP duty to tell people without delay is due to start in 2027, during this contract, so check the current rule text. The model asks for notice within twenty-four hours of them noticing. Exit: deletion within thirty days, not ninety, with written confirmation, and a second SMS provider as a fallback. Rating: medium-high as offered. Decision: conditional approval, with the conditions in the data agreement before it's signed. Answer the question: seven.

On screen: the step text, the report tool with the model answer.

## 9. Hand in

Step nine: hand in. The notebook carries everything you've done: the threat model, the attack tree, the memo, the risk register, the Statement of Applicability, the exception and the vendor file. Check the list, then press Hand in.

*After it runs:*

The rubric is on screen, thirty points in all. Five each go to the threat model, the memo, the register, the Statement of Applicability and the vendor file. Three go to the exception and two to the attack tree. The marks are for decisions, not length.

On screen: the step text.

## Wrap-up

That's a design review that changes the design. The threat model found the unsigned webhook and the amount from the app before an attacker did. The memo made three go-live conditions. The register gave every risk an owner and a date, and put the high ones in front of people who can sign for them. The Statement of Applicability told the truth with evidence, four gaps included. The exception has an end date. And the vendor file ends in a decision, made while Banyan still had leverage. The lesson to keep: security is cheapest at the design stage, and every finding needs a decision, an owner and a date, or it's just a worry. Next is seminar eleven, AI security: attacking and governing LLM apps, where the system you review talks back. Thank you for watching.

## YouTube chapters (estimate; `python tools/teach.py demo s10-design-risk-audit` writes the exact ones)

```
0:00 Opening
1:21 1. Read the design like a reviewer
3:21 2. Threat-model it with STRIDE
5:58 3. The attack tree: the cheapest way in
7:40 4. Write the design review memo
9:46 5. Build the risk register
11:58 6. The Statement of Applicability
14:10 7. Write the audit exception
16:20 8. The vendor file
18:39 9. Hand in
19:12 Wrap-up
```
