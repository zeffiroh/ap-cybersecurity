## 6. Check the indicators

Pull every indicator out of the evidence and check it against the intel feed and the client's allow list. Map what you saw to ATT&CK so the morning team and the client speak the same language.

- [ ] Extract indicators from the logs
- [ ] Which are on the feed, which are new, and which are on the allow list?
- [ ] An allowed destination received the stolen files. What does that mean for blocking?
- [ ] Map the behaviour to ATT&CK techniques
- [ ] Defang indicators before you paste them anywhere

> Hint: A phone call that talked the user into it, a remote access tool, three discovery commands, a download, a renamed program, and an upload to cloud storage.

```tool ioc
{"attack": ["T1566.004", "T1219", "T1033", "T1135", "T1083", "T1105", "T1036", "T1567.002"], "blank": ["iocs", "attack"]}
```

?> From which domain was the remote access program downloaded? :: ledgerpro-support.example
