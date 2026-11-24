## 5. Escalate

Write the escalation for the incident lead. The ask goes in the first line, with who and by when. Then severity and the one fact that decided it, what you know, what you don't, impact, what you did (and didn't), and where the evidence is.

- [ ] First line: the ask, with a time
- [ ] Severity, and the one fact that decided it
- [ ] Facts with times, newest last
- [ ] Where the evidence is saved (file names or hashes)

```tool report
{"tpl": "escalation", "title": "Escalation: ransomware on acct-lt04 and fs02", "text": "# Escalation: ransomware on acct-lt04 and fs02\n\n## The ask\n\nPlease open a critical incident and approve keeping acct-lt04 isolated, taking the Accounts and Purchase shares on fs02 read-only and disabling the account svc_sync on vpn01, by 11:30 UTC. Incident lead and IT operations, please call the SOC.\n\n## Severity and why\n\nCritical: files on fs02 were being encrypted (AL-3309), and someone outside is trying the attacker's new account on the VPN (AL-3310).\n\n## What we know\n\n- 10:12 UTC: a fake courier email from swiftroute-delivery.example reached 3 people (mail.log, message 7C3E90B14).\n- 10:14:58 UTC: meera.shah on acct-lt04 downloaded AWB-77120.zip; at 10:15:40 wscript.exe ran the .js inside it, which started a hidden PowerShell (proxy.log, process.csv).\n- 10:16 UTC: PowerShell downloaded upd.dat from files-cdn-sync.example and started OneDriveSync.exe from C:\\ProgramData\\cache (proxy.log, process.csv).\n- 10:17 UTC: local administrator svc_sync was created and antivirus real-time protection was turned off (AL-3311, AL-3307).\n- 11:02 to 11:12 UTC: files on \\\\fs02\\dept\\Accounts and \\Purchase were renamed to .saffron-locked (share_listing.txt).\n- 11:14 UTC: the helpdesk unplugged acct-lt04 (ticket 55120).\n- 11:19 UTC: 5 failed VPN logons for svc_sync and Administrator from 198.51.100.77, the same address as the download server (AL-3310).\n\n## What we don't know\n\n- Whether kiran.joshi opened the archive.\n- What was sent in the larger session to files-cdn-sync.example at 11:06:40 UTC.\n- Whether the attacker has access to any other host.\n\n## Impact so far\n\nHost acct-lt04 and user account meera.shah are compromised. 8 files on the Accounts and Purchase shares are encrypted, including bank reconciliation, salary advances and the supplier master with bank details (personal and financial data). Warehouse is not encrypted. The encryption stopped after the laptop was unplugged.\n\n## What I've done\n\n- 11:14 UTC: the helpdesk unplugged acct-lt04 (not me; I have not changed anything on the host).\n- 11:16 UTC: I asked the proxy team to confirm swiftroute-delivery.example and files-cdn-sync.example are blocked.\n\n## Evidence\n\nSaved in the incident folder with SHA-256 hashes: alerts.json, mail.log, proxy.log, process.csv, share_listing.txt and courier.eml. Ticket 55120 holds the helpdesk notes.\n", "n": 7, "blank": ["text"]}
```

?> How many files on the share were encrypted? :: 8

?> Which folder on the share was not encrypted? :: Warehouse

?> How many minutes passed between the first and the last encrypted file? :: 10
