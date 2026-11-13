## 3. File with CERT-In inside six hours

File the CERT-In report now, with what you know. The form checks your times against the evidence and says what's missing. After you file, advance the clock: replies and new facts arrive in the inbox. Answer them, and send an update when the facts change.

```tool certin
{"file": "certin-kaveri.json", "form": {"name": "Meenal Rao", "role": "Chief Information Security Officer", "email": "ciso@kaveri.example", "phone": "+91 80 4000 1200", "org": "Kaveri Microfinance Ltd", "sector": "Finance (NBFC regulated by RBI)", "occurred": "2027-06-08 03:10", "detected": "2027-06-08 04:50", "type": "Data breach", "systems": "Loan app API api.kaveri.example (/v2/customers/{id}/kyc), Linux servers behind the WAF; customer KYC database.", "symptoms": "One client with a valid session for customer 118842 requested other customers' KYC records in sequence from 03:10 to 04:18 UTC. The API returned 2,060 records: name, mobile, loan amount, last four digits of Aadhaar, address. A missing ownership check, released on 21 May 2027.", "indicators": "198.51.100.66; User-Agent python-requests/2.31.0; sequential requests to /v2/customers/{id}/kyc with the token of customer 118842.", "actions": "Blocked 198.51.100.66 at the WAF; switched rule 9021 to block; revoked the token; ownership check fix deployed 07:15 UTC; logs preserved; DPO and Board informed.", "personal": "yes", "filed": "2027-06-08 08:15"}, "n": 0, "blank": ["form"]}
```

- [ ] Detection time matches the evidence
- [ ] The incident type fits; personal data marked
- [ ] Indicators, affected systems and actions so far
- [ ] Filed before 10:50 UTC
- [ ] Inbox answered; an update sent after the CISO's message

> Hint: "Data breach" fits best: personal data was taken by someone who shouldn't have it. Partial facts are fine; say what you don't know yet in the symptoms.

?> Which CERT-In incident type fits best? :: Data breach
