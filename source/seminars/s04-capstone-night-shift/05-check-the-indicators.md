## 5. Check the indicators

Pull every indicator out of the evidence and check it against the client's intel feed. Map what you saw to ATT&CK so the morning team and the client speak the same language.

- [ ] Extract indicators from the logs
- [ ] Which are on the intel feed, and which are new?
- [ ] Map the behaviour to ATT&CK techniques
- [ ] Defang indicators before you paste them anywhere

> Hint: Download, scheduled task, PowerShell discovery, exfiltration over DNS: four techniques, four tiles on the heatmap.

```tool ioc
{"attack": ["T1204.002", "T1053.005", "T1059.001", "T1083", "T1048.003", "T1071.004"], "blank": ["iocs", "attack"]}
```

?> From which domain was the program downloaded? :: taxhelp-tools.example
