## 7. Map the attack to ATT&CK

ATT&CK gives each step a shared name, so a reader at another company, an insurer or CERT-In knows exactly what you mean. Map every step on your timeline to one technique, with the evidence that proves it.

```tool ioc
{"attack": ["T1133", "T1078", "T1021.001", "T1087.002", "T1018", "T1105", "T1059.001", "T1003.001", "T1550.002", "T1021.002", "T1569.002", "T1490", "T1486", "T1657"], "blank": ["iocs", "attack"]}
```

| Time (UTC) | Step | Technique | Evidence |
|---|---|---|---|
| 22:44 | VPN login with a valid account, no MFA | T1133, T1078 | vpn.log |
| 22:52 | RDP to eng-ws14 | T1021.001 | eng-ws14 4624 type 10 |
| 22:54 | whoami, net group, nltest | T1087.002, T1018 | process.csv |
| 22:58 | Toolkit downloaded with hidden PowerShell | T1105, T1059.001 | process.csv |
| 23:05 | lsass dumped with comsvcs.dll | T1003.001 | Sysmon 1, 10, 11; Volatility |
| 23:20 | adm.rjoshi's hash used on fs02 over SMB | T1550.002, T1021.002 | fs02 4624 NTLM, 5140 ADMIN$ |
| 23:20 | Service WinUpdSvc runs the payload | T1569.002 | 7045; Velociraptor |
| 23:41 | Shadow copies deleted, recovery off | T1490 | Hayabusa; process.csv |
| 23:42 | Share encrypted, extortion note | T1486, T1657 | share_listing.txt; note |

- [ ] Every row has a technique and a piece of evidence
- [ ] Mark the techniques on the heatmap
- [ ] Which one step, if blocked, would have stopped the rest?

?> Which ATT&CK technique ID is "Inhibit System Recovery"? :: T1490
