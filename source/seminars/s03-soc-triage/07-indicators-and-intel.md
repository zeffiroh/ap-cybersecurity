## 7. Indicators and intel

Pull every indicator out of the evidence, check it against the intel feed, and map what you saw to ATT&CK. Your intel note lists each indicator **defanged** (login-verify[.]example), says which source knows it, and says what to do: block, watch or ignore.

- [ ] Extract indicators
- [ ] Which are on the feed, and from which source?
- [ ] Which names and addresses must not be blocked?
- [ ] Map the three campaigns to ATT&CK: the fake booking partner, the fake GST refund and the USB stealer, plus the payment fraud
- [ ] Write the intel note

> Hint: The feed also lists the real booking-partner extranet and internal systems as benign. Blocking extranet.bookingpartner.example would stop Reservations from working.

```tool ioc
{"attack": ["T1566.002", "T1583.001", "T1656", "T1091", "T1204.002", "T1555.003", "T1567"], "blank": ["iocs", "attack"]}
```

?> Which source on the feed reported bookingpartner-extranet.login-verify.example? :: Hospitality ISAC
