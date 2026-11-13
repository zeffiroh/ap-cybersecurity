## 9. File and notify

File with CERT-In, answer the inbox, and write the notification order. Remember who is the processor and who are the fiduciaries.

```tool certin
{"file": "certin-indigo.json", "form": {"name": "Chetan Iyer", "role": "Head of IT and security", "email": "security@indigoledger.example", "phone": "+91 20 6600 4000", "org": "Indigo Ledger Pvt Ltd", "sector": "IT services (payroll processing for client companies)", "occurred": "2027-11-29 02:58", "detected": "2027-11-29 05:35", "type": "Data breach", "systems": "VPN vpn01 (account intern.payroll); file server files01 (IT$ share); application server pay-app01 (10.80.1.40, Windows Server); cloud storage bucket payroll-exports.", "symptoms": "Password spray on the VPN from 198.51.100.150; one former intern's account without MFA got in; a script on a file share held a local admin password and a cloud key; payroll export files of four client companies (2,505 employees: names, salaries, bank accounts, PAN) were copied from pay-app01 and from cloud storage.", "indicators": "198.51.100.150; 203.0.113.230 and upload.drop-files.example (exfiltration); key SCKA9F2LQ7MX4TB1; C:\\Users\\Public\\t.ps1 and e.zip.", "actions": "VPN session cut 06:02; intern.payroll disabled; cloud key revoked; localadmin password reset on all servers; pay-app01 isolated; logs preserved.", "personal": "yes", "filed": "2027-11-29 09:10"}, "n": 0, "blank": ["form"]}
```

| # | Who | Why | Due (UTC) | Owner |
|---|---|---|---|---|
| 1 | CERT-In | Six hours from noticing; Indigo is a service provider | 29 Nov 11:35 | Head of IT and security |
| 2 | Each client (data fiduciary) | They must notify the Board and their employees; Indigo processes for them | At once, by 07:00 | CEO and account managers |
| 3 | Coral Small Finance Bank, first | It's RBI-regulated with its own six-hour clock from when it learns | At once | Head of IT and security |
| 4 | Clients' notices to the Data Protection Board and their employees | Their duty; Indigo supplies facts and a draft notice | Without delay | Each client's DPO, supported by Indigo |
| 5 | Fjord Design's EU parent | 12 EU staff: GDPR, 72 hours, their decision | Today | Account manager |
| 6 | Cyber insurer | Policy terms | Today | CFO |

?> Who must tell the affected employees: Indigo or its clients? (one word) :: clients
