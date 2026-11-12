## 6. Indicators and intel

Pull every indicator out of the evidence, check it against the intel feed, and map the campaign to ATT&CK. Your intel note lists each indicator **defanged** (kestrel-logistlcs[.]com), says which feed knows it, and says what to do: block, watch or ignore.

- [ ] Extract indicators
- [ ] Which are on the feed, and from which source?
- [ ] Which internal names and addresses must not be blocked?
- [ ] Map the campaign to ATT&CK
- [ ] Write the intel note

> Hint: The feed also lists internal assets as benign. Blocking intranet.kestrel.lan would be a bad morning.

```tool ioc
{"attack": ["T1566.001", "T1566.002", "T1204.002", "T1071.001", "T1105", "T1486", "T1490", "T1656"], "blank": ["iocs", "attack"]}
```

?> Which source on the feed reported kestrel-logistlcs.com? :: Sector ISAC
