## 8. Automate the response

Cloud alerts arrive at night. A SOAR playbook does the routine part automatically (look up indicators, open tickets, block known-bad addresses, disable a key that's being abused) and leaves judgement calls to a person. Run it on the cloud alert queue.

```tool soar
{"pb": "when severity >= high\n  enrich\n  ticket\n  if intel == malicious then block\n  if rule contains \"access key\" then disable\n  if rule contains \"gpu\" then disable\n  notify\n\nwhen severity == medium\n  enrich\n  if intel == malicious then block\n  ticket\n\nwhen severity == low\n  enrich\n  ticket\n", "file": "cloud/alerts-cloud.json", "n": 12, "blank": ["pb"]}
```

- [ ] The abused key is disabled and the attacker's address blocked automatically
- [ ] The public product-images bucket and the intern's login are **not** acted on automatically
- [ ] Nothing high or critical is closed automatically
- [ ] Which alert would you never automate? Why?

> Hint: Disabling ci-deployer stops tonight's deploys too. That's the right trade at 21:40 with a miner running, but say so in the ticket.

?> Which account does the playbook disable? :: ci-deployer
