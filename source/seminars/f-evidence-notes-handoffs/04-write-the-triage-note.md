## 4. Write the triage note

Now rewrite ticket 88213 as a triage note for alert **AL-2203**. The report builder checks each section as you type: it wants an alert ID, times with a time zone, the exact searches you ran, at least one gap, a disposition and an owner.

Rules that make notes useful:

- One time zone for everything (UTC here), written every time.
- Facts say where you saw them. Guesses go under "What I don't know yet".
- Write what you ran, so the next person can repeat it without asking you.

- [ ] Fill every section, then press Check the report
- [ ] Compare yours with the model answer only after you've written your own
- [ ] Download the Markdown: it is part of your hand-in

> Hint: "What I don't know yet" is never empty. Here: did the other two people open the invoice, and was anything copied out?

```tool report
{"tpl": "triage", "title": "Triage note: AL-2203 macro document on hr-pc07", "text": "# Triage note: AL-2203 macro document on hr-pc07\n\n## What fired\n\nAL-2203 \"Office document with macros opened from the internet\", severity high, host hr-pc07, user priya.nair, 2026-11-02 09:02:44 UTC.\n\n## What I checked\n\n- mail.log: grep 4A1F21C02 (the reported message)\n- proxy.log: grep -E 'docm|s2.bin'\n- process.csv: the process tree for hr-pc07 (Python cell, step 3)\n- alerts.json: the other alerts on hr-pc07 between 09:00 and 10:00 UTC\n\n## What I found\n\n- 08:51 UTC: message 4A1F21C02 from bounce-7781@kestrel-logistlcs.com (look-alike domain, 203.0.113.45) was delivered to 3 people: priya.nair, dev.kapoor, tomas.reyes.\n- 09:02 UTC: 10.20.0.14 downloaded INV-30412.docm from kestrel-logistlcs.com (proxy TCP_MISS/200).\n- 09:02:55 UTC: WINWORD.EXE started cmd.exe, which started a hidden PowerShell running C:\\Users\\Public\\upd.ps1.\n- 09:03:09 UTC: hr-pc07 downloaded s2.bin from cdn-update-check.net (198.51.100.140).\n- 09:03:20 UTC: PowerShell started C:\\Users\\Public\\svchost-upd.exe (PID 4810).\n- 09:41 UTC: PID 4810 mapped \\\\fs01\\shared and started renaming files to .kestrel-locked (AL-2208).\n\n## What I don't know yet\n\n- Whether dev.kapoor or tomas.reyes opened the attachment (10.20.0.15 was blocked at 09:20 UTC; the third person is unknown).\n- What s2.bin does, and whether data was copied out before the encryption.\n- Whether other hosts talked to 198.51.100.140.\n\n## Disposition and why\n\nTrue positive, escalate: a macro document from a look-alike domain started PowerShell and an unknown program, and the same program is encrypting the file share.\n\n## Next step and owner\n\nEscalate to the incident lead now (09:55 UTC). Owner: SOC analyst on shift until the incident lead takes it; keep hr-pc07 off the network and do not reboot it.\n", "n": 6, "blank": ["text"]}
```

?> Which disposition fits AL-2203? (escalate, handled, benign, false positive or more information) :: escalate
