## 6. The Statement of Applicability

An auditor asks: which controls apply, which are in place, and where is the evidence? In the compliance tool, choose ISO/IEC 27001 and mark each control **met**, **partial**, **gap** or **not applicable**, with the evidence from controls-evidence.txt. "Met" without evidence isn't met.

```tool compliance
{"fw": "iso", "ans": {"iso:5.1": {"s": "met", "e": "Policy v3, CEO approval 2 Feb 2026; 94% acknowledged"}, "iso:5.2": {"s": "partial", "e": "CISO part-time; no vendor RACI"}, "iso:5.9": {"s": "partial", "e": "Cloud listed automatically; 40% without owners"}, "iso:5.15": {"s": "partial", "e": "Policy exists; Q3 access review skipped"}, "iso:5.19": {"s": "gap", "e": "No standard clauses; TextBridge has no DPA"}, "iso:5.24": {"s": "met", "e": "IR plan v2 with CERT-In step; tabletop in August"}, "iso:5.29": {"s": "gap", "e": "No continuity plan for the apps"}, "iso:5.30": {"s": "gap", "e": "No recovery test this year"}, "iso:6.3": {"s": "partial", "e": "Onboarding only; no yearly refresher"}, "iso:7.2": {"s": "partial", "e": "Badges at Pune; key lock in Nashik"}, "iso:8.2": {"s": "partial", "e": "Separate admin accounts; 3 shared admin console logins"}, "iso:8.5": {"s": "partial", "e": "MFA on cloud and email, not on the admin console"}, "iso:8.7": {"s": "met", "e": "Managed anti-malware on all laptops"}, "iso:8.8": {"s": "gap", "e": "3 criticals past the 15-day target (IA-2026-07)"}, "iso:8.13": {"s": "partial", "e": "Nightly encrypted offsite; last restore test March"}, "iso:8.15": {"s": "partial", "e": "Audit trail on; app logs hold personal data"}, "iso:8.16": {"s": "partial", "e": "Alerts to an unwatched inbox at weekends"}, "iso:8.20": {"s": "partial", "e": "Cloud segmented; office Wi-Fi shared with guests"}, "iso:8.24": {"s": "partial", "e": "TLS 1.2+, DB encrypted; key rotation not documented"}, "iso:8.28": {"s": "partial", "e": "Code review; no security testing before release"}}, "n": 4, "blank": []}
```

- [ ] Every control marked, every mark with evidence
- [ ] Be honest: partial is a normal, useful answer
- [ ] Which gaps does Parent Pay make worse? (5.19 suppliers, 8.15 logging)
- [ ] Switch the framework to DPDP and CERT-In: which items does today's work already cover?

> Hint: A Statement of Applicability is about the truth, not the score. An auditor trusts a company that marks its own gaps far more than one that marks everything met.

?> How many ISO controls are gaps? :: 4
