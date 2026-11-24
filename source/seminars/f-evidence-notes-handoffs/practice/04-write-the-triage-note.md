## 4. Write the triage note

Write a triage note for alert **AL-3303**, the script run from the downloaded archive. The report builder checks each section: alert ID, times with a time zone, the exact searches you ran, at least one gap, a disposition and an owner.

- [ ] Fill every section, then press Check the report
- [ ] Compare yours with the model answer only after you've written your own
- [ ] Download the Markdown: it is part of your hand-in

```tool report
{"tpl": "triage", "title": "Triage note: AL-3303 script from a downloaded archive on acct-lt04", "text": "# Triage note: AL-3303 script from a downloaded archive on acct-lt04\n\n## What fired\n\nAL-3303 \"Script run from a downloaded archive\", severity high, host acct-lt04, user meera.shah, 2026-11-10 10:15:41 UTC.\n\n## What I checked\n\n- mail.log: grep 7C3E90B14 (the reported message), and grep -E 'report|blocklist'\n- proxy.log: grep -E 'AWB-77120|upd.dat|files-cdn-sync', times turned into UTC (Python cell, step 2)\n- process.csv: the process tree for acct-lt04 (Python cell, step 3)\n- alerts.json: the other alerts on acct-lt04 between 10:00 and 11:20 UTC\n\n## What I found\n\n- 10:12 UTC: message 7C3E90B14 from noreply@swiftroute-delivery.example (look-alike courier domain, 203.0.113.62) was delivered to 3 people: meera.shah, arjun.rao, kiran.joshi.\n- 10:14:58 UTC: 10.30.0.21 downloaded AWB-77120.zip from swiftroute-delivery.example (proxy TCP_MISS/200).\n- 10:15:40 UTC: wscript.exe ran AWB-77120.pdf.js from Downloads; it started cmd.exe and a hidden PowerShell running C:\\ProgramData\\cache\\p.ps1.\n- 10:16:12 UTC: acct-lt04 downloaded upd.dat from files-cdn-sync.example (198.51.100.77).\n- 10:16:31 UTC: PowerShell started C:\\ProgramData\\cache\\OneDriveSync.exe (PID 5302). The real OneDrive.exe runs from C:\\Program Files.\n- 10:17 UTC: PID 5302 created local account svc_sync and added it to Administrators; PowerShell turned off antivirus real-time protection.\n- From 10:16:40 UTC: an encrypted session to files-cdn-sync.example every 600 seconds; the one at 11:06:40 was far larger (88,004 bytes).\n- 11:02 UTC: PID 5302 mapped \\\\fs02\\dept and started renaming files to .saffron-locked (AL-3309).\n\n## What I don't know yet\n\n- Whether kiran.joshi opened the archive (arjun.rao's attempt was blocked at 10:36 UTC; there is no proxy line for kiran.joshi).\n- What was sent in the larger session at 11:06:40 UTC.\n- Whether svc_sync was used anywhere else.\n\n## Disposition and why\n\nTrue positive, escalate: a script from a look-alike courier's archive started a hidden PowerShell and an unknown program that is now encrypting the file share.\n\n## Next step and owner\n\nEscalate to the incident lead now (11:16 UTC). Owner: SOC analyst on shift until the incident lead takes it; keep acct-lt04 off the network and do not reboot it.\n", "n": 6, "blank": ["text"]}
```

?> Which disposition fits AL-3303? (escalate, handled, benign, false positive or more information) :: escalate

?> Which internal IP address is sales-lt11, arjun.rao's laptop? :: 10.30.0.33

?> Of the three people who received the email, how many are known to have tried to open the archive? :: 2
