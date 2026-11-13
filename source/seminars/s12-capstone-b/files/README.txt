EXERCISE set in November 2027. Indigo Ledger Pvt Ltd, Pune: payroll processing for client companies. Monday 29 November 2027, times UTC.

Indigo processes its clients' employees' data (names, salaries, bank accounts, PAN) on their behalf. The clients decide why and how it's used.

vpn01      remote access VPN (MFA optional)              files01    10.80.1.15   file server (IT$ share for IT scripts)
pay-app01  10.80.1.40  Windows Server, the payroll application; exports go to D:\exports and to cloud storage
VPN pool   10.80.9.0/24      office egress 203.0.113.88

What you have: vpn.log, identity/users.csv, zeek/conn.log, zeek/smb_files.log, captured/backup-config.ps1.txt,
eventlogs/pay-app01-Security.jsonl, cloud/policies.json, cloud/audit.json, cloud/egress-alert.txt, clients.csv, certin-indigo.json

This capstone has no hints. Work it like the job.
