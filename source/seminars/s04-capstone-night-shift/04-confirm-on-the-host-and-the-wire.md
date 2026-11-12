## 4. Confirm on the host and the wire

Search results are a summary. Confirm on the host's own logs and on the packet capture: which program made the lookups, how it got there, and where the answers came from.

- [ ] Sysmon event 1: what was downloaded, what did it copy itself as, which task did it create?
- [ ] Sysmon event 22: which program made the TXT lookups?
- [ ] Capture: which server answered the tunnel queries?

> Hint: In the packet viewer, the filter `dns.qry.name contains cloudmetric` shows the tunnel. Look at the destination of the answers' questions.

```tool events
{"file": "eventlogs/Sysmon.jsonl", "ids": "1", "n": 8, "blank": ["ids", "src", "q"]}
```

```tool events
{"file": "eventlogs/Sysmon.jsonl", "ids": "22", "q": "cloudmetric.example", "n": 26, "blank": ["ids", "src", "q"]}
```

```tool packets
{"file": "capture.pcap", "f": "dns.qry.name contains cloudmetric", "n": 104, "blank": ["f"]}
```

?> What file name does the malware use to look like the chat app? :: msteams-update.exe

?> What is the name of the scheduled task it created? :: TeamsUpdateCheck

?> At what time (HH:MM) did the first tunnel query go out? :: 11:09

?> Which IP address is the attacker's name server? :: 198.51.100.53
