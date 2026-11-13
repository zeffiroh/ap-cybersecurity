## 10. Leave detections behind

Two rules that would have caught this hours earlier: one for the spray, one for the local admin logon.

```tool siem
{"q": "source=*vpn.log result=failure | stats count by src", "n": 1, "files": ["vpn.log"], "blank": ["q"]}
```

```tool sigma
{"rule": "title: Network logon by a local administrator account\nid: 4c7e1a20-5b3f-4d8e-8f1a-2c0d00001201\nstatus: experimental\ndescription: Local admin accounts should never log on over the network; with LAPS each server's password is different. A network logon by one usually means a reused password.\nlogsource:\n  product: windows\n  service: security\ndetection:\n  selection:\n    EventID: 4624\n    LogonType: '3'\n    TargetUserName: 'localadmin'\n  condition: selection\nfalsepositives:\n  - Break-glass use during an outage; record it in the change log\nlevel: high\ntags:\n  - attack.lateral_movement\n  - attack.t1078.003\n", "n": 1, "ls": true, "blank": ["rule"]}
```

- [ ] The spray search finds one source with many failures
- [ ] The Sigma rule matches the attacker's logon and nothing normal
- [ ] For each, the time it would have fired, against the time Indigo noticed

?> How many failed VPN logins came from the spraying address? :: 17
