## 1. How the night desk works

A capstone uses every program from seminars 2 and 3 at once, so start by seeing how they fit. Each program answers one kind of question, and a night shift moves through them in order:

| Program | The question it answers | Reads |
|---|---|---|
| Alert queue | What do I have to decide tonight? | alerts-night.json |
| SIEM search | How big is it: which hosts, how often, how much data? | fw_sessions.csv, dns.log, process.csv, the event logs |
| Event viewer | What exactly ran on the laptop, started by what? | eventlogs/*.jsonl |
| Packet viewer | What really crossed the wire, and to where? | capture.pcap |
| Indicators and ATT&CK | Has anyone seen this before, and what do we call it? | intel.json |
| Sigma rules | How do we catch it sooner next time? | the event logs |
| Report builder | What does the client need to decide, and what does the morning shift need to know? | your notes |

The client tonight is **Wattle & Finch Accountants** in Brisbane. Their working day is your night. Read `README.txt` first, then run the inventory search below: it shows which files the SIEM can search and how many events each holds. The alert queue and the intel feed are JSON, so the SIEM reads them too. The packet capture isn't in the SIEM; the packet viewer reads it.

- [ ] Run the inventory search
- [ ] Which file holds the most events? Which one is about the whole office, and which only about one laptop?
- [ ] Note which program you would open for each kind of question

> Hint: `stats count by source sourcetype` makes one row per file: eight files, from 308 events. The firewall and DNS logs cover every laptop; the event logs and process list come from one laptop only.

```tool siem
{"q": "* | stats count by source sourcetype", "n": 8, "files": ["fw_sessions.csv", "dns.log", "process.csv", "eventlogs/Sysmon.jsonl", "eventlogs/Security.jsonl", "eventlogs/System.jsonl"], "blank": ["q"]}
```

?> Which evidence file holds the most events? :: dns.log
