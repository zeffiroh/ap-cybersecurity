## 2. Triage the reported emails

Five emails were reported. For each one, read who **really** sent it (Return-Path and the Received line), what SPF, DKIM and DMARC said, where the link **really** goes, and which pressure tactics it uses. Then give a verdict: phishing, payment fraud (BEC), spam, or genuine.

- [ ] Sender, Reply-To and Return-Path for each email
- [ ] Authentication results, and which domain each result is about
- [ ] The real link target, not the link text
- [ ] Pressure tactics: urgency, secrecy, authority, fear of loss
- [ ] Anything in the email that isn't meant for a human reader
- [ ] A verdict for each

> Hint: In guest-complaint.eml the link text says extranet.bookingpartner.example, but the href goes somewhere else. In supplier-bank-change.eml the display name says General Manager, but the address is a free mail account, and SPF, DKIM and DMARC all pass for that free mail domain. gst-refund.eml has a line in 1-pixel white text.

```tool email
{"d": {"reported/guest-complaint.eml": "phish", "reported/gst-refund.eml": "phish", "reported/linen-offer.eml": "spam", "reported/payslips.eml": "legit", "reported/supplier-bank-change.eml": "bec"}, "n": 3, "files": ["reported/guest-complaint.eml", "reported/gst-refund.eml", "reported/linen-offer.eml", "reported/payslips.eml", "reported/supplier-bank-change.eml"], "blank": ["d"]}
```

?> Which host does the guest-complaint link really go to? :: bookingpartner-extranet.login-verify.example

?> How many of the five emails are phishing or payment fraud? :: 3
