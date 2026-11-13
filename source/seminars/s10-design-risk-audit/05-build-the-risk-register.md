## 5. Build the risk register

The product team's first register has holes: no owner, no treatment, a high risk "accepted" with nobody's name on it. Load it, fix it, and add the risks your model found. The tool checks every row has an owner, a treatment and a date, and flags high risks that are accepted without sign-off.

```tool risk
{"rows": [{"asset": "Fees API", "threat": "Fake payment confirmation", "weakness": "Webhook isn't signed", "likelihood": 5, "impact": 5, "treatment": "mitigate", "control": "Verify PayGate's signature and confirm with PayGate", "owner": "Sana Pillai", "due": "2026-12-01"}, {"asset": "Fees API", "threat": "Fee amount changed by the parent", "weakness": "Amount comes from the app", "likelihood": 4, "impact": 4, "treatment": "mitigate", "control": "Server looks up the amount", "owner": "Sana Pillai", "due": "2026-12-01"}, {"asset": "Admin console", "threat": "Refund fraud by a stolen staff login", "weakness": "No MFA; shared logins; one-click refunds", "likelihood": 3, "impact": 5, "treatment": "mitigate", "control": "MFA, named accounts, second approver over Rs 5,000", "owner": "Head of Finance", "due": "2027-01-15"}, {"asset": "App logs", "threat": "Personal data in logs", "weakness": "Full request bodies kept 90 days", "likelihood": 4, "impact": 3, "treatment": "mitigate", "control": "Log events not bodies; 30 days", "owner": "Sana Pillai", "due": "2026-12-15"}, {"asset": "SMS receipts", "threat": "Children's details exposed by the SMS vendor", "weakness": "No DPA; receipts include name and class", "likelihood": 3, "impact": 4, "treatment": "mitigate", "control": "DPA signed; minimal receipt text", "owner": "Kunal Desai", "due": "2026-12-01"}, {"asset": "Admin console", "threat": "Exploit of the outdated web framework", "weakness": "VM-311 open 41 days", "likelihood": 3, "impact": 5, "treatment": "mitigate", "control": "Upgrade; until then WAF rule and VPN-only access (exception IA-2026-07)", "owner": "IT manager", "due": "2027-01-31"}], "n": 4, "blank": []}
```

- [ ] Every row: likelihood and impact from 1 to 5, treatment, control, owner, date
- [ ] No high risk accepted without leadership sign-off
- [ ] The heat map: which risks are in the red corner?

> Hint: Likelihood × impact of 15 or more is high. "Accept" is a real choice, but it belongs to someone senior enough to pay for the consequence.

?> How many risks in your register are high (score 15 or more)? :: 4
