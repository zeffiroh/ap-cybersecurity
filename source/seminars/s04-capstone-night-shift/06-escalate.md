## 6. Escalate

Write one escalation for the whole intrusion, not one per alert. The client's duty manager reads it on a phone.

- [ ] The ask first, with a time
- [ ] Severity and the fact that decided it
- [ ] Know / don't know
- [ ] What you have and haven't changed

> Hint: Say clearly that you have not touched the laptop. The client decides on isolation; you give them what they need to decide.

```tool report
{"tpl": "escalation", "title": "Escalation: data leaving fin-lt04 through DNS", "text": "# Escalation: data leaving fin-lt04 through DNS\n\n## The ask\n\nPlease approve isolating fin-lt04 (10.70.0.44) and disabling the account m.devlin's sessions now, by 12:15 UTC. Client duty manager, please call the SOC on the bridge.\n\n## Severity and why\n\nHigh: a program installed from the internet is sending data out through DNS TXT lookups to cloudmetric.example, so data is leaving right now.\n\n## What we know\n\n- 11:02 UTC: m.devlin downloaded TaxRefundCalc_2026.exe from taxhelp-tools.example (AL-7301, proxy.log).\n- 11:04 UTC: it copied itself to AppData as msteams-update.exe and created the task TeamsUpdateCheck (AL-7303, Sysmon event 1).\n- 11:05 UTC: a hidden PowerShell listed the newest spreadsheets in Documents (AL-7304).\n- 11:06 to 11:07 UTC: the proxy blocked an upload to pastebox.example (AL-7306).\n- 11:09 UTC onwards: 26 TXT queries with long names under cloudmetric.example, all from 10.70.0.44 (dns.log, Sysmon event 22, AL-7308).\n\n## What we don't know\n\n- Which file was sent, and whether all of it got out.\n- Whether any other host ran the same download (dns.log shows only 10.70.0.44 asking for cloudmetric.example so far).\n\n## Impact so far\n\nOne laptop, fin-lt04, and one user, m.devlin, in Finance. Board spreadsheets were open on the laptop at 11:00 UTC, so confidential data may be affected.\n\n## What I've done\n\nNothing has been changed on the host. I have added cloudmetric.example and taxhelp-tools.example to the watch list in the SIEM.\n\n## Evidence\n\ndns.log, proxy.log, Sysmon.jsonl, Security.jsonl and capture.pcap are saved in the shift folder with SHA-256 hashes; the queue with dispositions is alerts-night.json.\n", "n": 7, "blank": ["text"]}
```
