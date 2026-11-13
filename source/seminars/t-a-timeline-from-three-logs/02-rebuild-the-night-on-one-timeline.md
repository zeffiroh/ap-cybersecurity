## 2. Rebuild the night on one timeline

Put every log on one clock. The merged timeline reads the VPN log, both machines' event logs and the process export together, sorted by time. Star the events that tell the story; the gaps tell you something too.

```tool timeline
{"keys": ["vpn.log#6@1794005050", "eventlogs/eng-ws14-Security.jsonl#4@1794005551", "eventlogs/eng-ws14-Sysmon.jsonl#8@1794006344", "eventlogs/fs02-Security.jsonl#5@1794007203", "eventlogs/fs02-System.jsonl#1@1794007209", "process.csv#17@1794008461", "process.csv#19@1794008530"], "n": 7, "blank": ["keys"]}
```

- [ ] When did the attacker get in, and through what?
- [ ] When did they reach eng-ws14, and how?
- [ ] When did they reach fs02, and as whom?
- [ ] Star the key events and download the timeline

> Hint: Narrow it with From 2026-11-06 22:40 and To 2026-11-07 00:00. The VPN log uses the same UTC clock as Windows.

?> At what time (UTC, HH:MM:SS) did the VPN login succeed? :: 22:44:10

?> Which account was used for the VPN login? :: s.kale
