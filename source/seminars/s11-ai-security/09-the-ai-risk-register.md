## 9. The AI risk register

Put the AI risks in the same register as every other risk, with likelihood, impact, treatment, control, owner and date. AI isn't special: it's another system with an owner.

```tool risk
{"rows": [{"asset": "Tara assistant", "threat": "Prompt injection leaks confidential data", "weakness": "Secret in the system prompt", "likelihood": 5, "impact": 3, "treatment": "mitigate", "control": "Remove secrets from prompts; strict output filter", "owner": "Head of Digital", "due": "2026-11-30"}, {"asset": "Tara assistant", "threat": "Poisoned partner documents steer the assistant", "weakness": "Partner content goes straight into the knowledge base", "likelihood": 4, "impact": 4, "treatment": "mitigate", "control": "Review partner documents; clean instructions from retrieved text", "owner": "Content lead", "due": "2026-12-15"}, {"asset": "Tara tools", "threat": "Refunds or emails without approval", "weakness": "Risky tools run automatically", "likelihood": 4, "impact": 5, "treatment": "mitigate", "control": "Approval gate on refund and send_email", "owner": "Head of Customer Support", "due": "2026-11-30"}, {"asset": "Staff use of AI", "threat": "Customer data pasted into public AI tools", "weakness": "No policy, no approved tool list", "likelihood": 4, "impact": 4, "treatment": "mitigate", "control": "AI policy; approved tools; block others on company devices", "owner": "CISO", "due": "2027-01-15"}, {"asset": "Tara answers", "threat": "Wrong travel rules given as fact", "weakness": "Answers not checked against the source", "likelihood": 3, "impact": 3, "treatment": "mitigate", "control": "Answers quote the source document; hand-over to a person", "owner": "Head of Digital", "due": "2027-01-31"}], "n": 4, "blank": []}
```

- [ ] The risks from today's tests, plus staff use of AI
- [ ] Every row has an owner who can actually fix it
- [ ] No high risk accepted without sign-off

?> How many of your AI risks are high (score 15 or more)? :: 4
