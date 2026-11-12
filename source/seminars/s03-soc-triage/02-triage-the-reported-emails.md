## 2. Triage the reported emails

Five emails were reported. For each one, read who **really** sent it (Return-Path and the Received line), what SPF, DKIM and DMARC said, where the link **really** goes, and which pressure tactics it uses. Then give a verdict: phishing, payment fraud (BEC), spam, or genuine.

- [ ] Sender, Reply-To and Return-Path for each email
- [ ] Authentication results
- [ ] The real link target, not the link text
- [ ] Pressure tactics: urgency, secrecy, authority
- [ ] A verdict for each

> Hint: In password-expiry.eml the link text says sso.kestrel-logistics.com, but the href goes somewhere else. In bank-details.eml the display name says CFO, but the address is a free mail account, and SPF, DKIM and DMARC all pass for that free mail domain.

```tool email
{"d": {"case/reported/bank-details.eml": "bec", "case/reported/hr-newsletter.eml": "legit", "case/reported/password-expiry.eml": "phish", "case/reported/webinar.eml": "spam", "case/invoice.eml": "phish"}, "n": 3, "files": ["case/reported/bank-details.eml", "case/reported/hr-newsletter.eml", "case/reported/password-expiry.eml", "case/reported/webinar.eml", "case/invoice.eml"], "blank": ["d"]}
```

?> Which domain does the password-expiry link really go to? (the host name) :: kestrel-sso.login-check.example

?> How many of the five emails are phishing or payment fraud? :: 3
