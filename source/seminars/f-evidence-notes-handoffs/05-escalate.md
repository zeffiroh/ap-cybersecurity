## 5. Escalate

An escalation is read in ten seconds by someone who has just been woken up. Put **the ask** in the first line: what you need, from whom, by when. Then severity, what you know, what you don't know, impact, what you did, and where the evidence is.

Say what you have **not** done as well: "I have not changed anything on the host" tells the incident lead the evidence is untouched.

- [ ] First line: the ask, with a time
- [ ] Severity, and the one fact that decided it
- [ ] Facts with times, newest last
- [ ] Where the evidence is saved (file names or hashes)

> Hint: Critical means harm is happening now. Files being encrypted on a shared drive is the fact that decides it.

```tool report
{"tpl": "escalation", "title": "Escalation: ransomware on hr-pc07 and fs01", "text": "# Escalation: ransomware on hr-pc07 and fs01\n\n## The ask\n\nPlease open a critical incident and approve isolating hr-pc07 and taking the HR and Finance shares on fs01 read-only, by 10:05 UTC. Incident lead and IT operations, please call the SOC.\n\n## Severity and why\n\nCritical: files on fs01 are being encrypted (AL-2208), so business data is being lost right now.\n\n## What we know\n\n- 08:51 UTC: a fake invoice from kestrel-logistlcs.com reached 3 people (mail.log, message 4A1F21C02).\n- 09:02 UTC: priya.nair on hr-pc07 opened INV-30412.docm; Word started cmd.exe and a hidden PowerShell (process.csv).\n- 09:03 UTC: PowerShell downloaded s2.bin from cdn-update-check.net and started svchost-upd.exe from C:\\Users\\Public (proxy.log, process.csv).\n- 09:04 UTC: a new local administrator, support_svc, was created on hr-pc07 (AL-2210).\n- 09:41 to 09:50 UTC: files on \\\\fs01\\shared\\HR and \\Finance were renamed to .kestrel-locked (share_listing.txt).\n- 09:52 UTC: the helpdesk pulled the network cable on hr-pc07 (ticket 88213).\n\n## What we don't know\n\n- Whether the other two recipients opened the invoice.\n- Whether any data was copied out before the encryption.\n- Whether the attacker has access to any other host.\n\n## Impact so far\n\nHost hr-pc07 and user account priya.nair are compromised. 10 files on the HR and Finance shares are encrypted, including payroll and vendor bank details (personal data). Ops is not encrypted. The encryption stopped after the cable was pulled.\n\n## What I've done\n\n- 09:52 UTC: the helpdesk pulled the cable on hr-pc07 (not me; I have not changed anything on the host).\n- 09:55 UTC: I asked the proxy team to confirm kestrel-logistlcs.com and cdn-update-check.net are blocked.\n\n## Evidence\n\nSaved in the incident folder with SHA-256 hashes: alerts.json, mail.log, proxy.log, process.csv, share_listing.txt and invoice.eml. Ticket 88213 holds the helpdesk notes.\n", "n": 7, "blank": ["text"]}
```

?> How many files on the share were encrypted? :: 10

?> Which folder on the share was not encrypted? :: Ops
