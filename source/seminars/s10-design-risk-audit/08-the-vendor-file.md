## 8. The vendor file

TextBridge is cheapest, and the contract isn't signed yet: the best moment to ask for things. Read their answers and write the vendor review. End with a **decision**: approve, approve with conditions, or reject.

```tool report
{"tpl": "vendor", "title": "Vendor security review: TextBridge Messaging (SMS receipts for Parent Pay)", "text": "# Vendor security review: TextBridge Messaging (SMS receipts for Parent Pay)\n\n## Vendor and service\n\nTextBridge Messaging Pvt Ltd, transactional SMS over an HTTPS API. 22% cheaper than the next quote.\n\n## Data they will handle\n\nParents' mobile numbers and the receipt text. Today's design adds the child's first name, class and amount; we will cut that to the amount and a reference.\n\n## Evidence of security\n\nISO 27001 certificate expired in June 2026 (renewal \"in progress\"); no SOC 2 report; yearly pen test (March 2026), summary under NDA, not yet seen.\n\n## Access and encryption\n\nTLS 1.2 in transit; storage encryption by their cloud host; support staff can read message logs; MFA \"for most staff\".\n\n## Incident notice\n\n\"Within 7 working days of confirmation\". Not acceptable: we need notice within 24 hours of them noticing, so we can meet the CERT-In six-hour rule and tell parents without delay.\n\n## Sub-processors and location\n\nMumbai, with backups in Singapore; two named operators, one named host, \"others as needed\" (must be named and notified before change).\n\n## Exit plan\n\nData deleted 90 days after termination on request: we need deletion within 30 days, with written confirmation. A second SMS provider is set up as a fallback.\n\n## Risk rating and decision\n\nMedium-high as offered. **Conditional approval:** sign only with a DPA that sets 24-hour incident notice, named sub-processors, MFA for all staff with access, logs kept 90 days not 2 years, and the renewed ISO certificate or the pen test summary before go-live. Minimal receipt text either way.\n", "n": 8, "blank": ["text"]}
```

- [ ] What data they get, and how to give them less
- [ ] Evidence you've seen versus claims you've been told
- [ ] Incident notice: is their promise fast enough for your own legal clocks?
- [ ] An exit plan, and a decision with conditions

> Hint: Your own breach clocks (CERT-In six hours; DPDP "without delay") don't stop because the breach happened at a vendor. Their notice period has to fit inside yours.

?> How many working days does TextBridge offer for incident notice? :: 7
