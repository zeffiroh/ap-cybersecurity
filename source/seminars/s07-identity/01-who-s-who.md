## 1. Who's who

Start like an auditor: read the directory before you read any alert. users.csv lists every account with its groups, MFA and last logon. ad_edges.csv lists **relationships**: who is a member of what, who can reset whose password, who is an admin where, and who is signed in where.

- [ ] How many accounts? How many without MFA?
- [ ] Which accounts are in powerful groups (Domain-Admins, Server-Admins, Backup-Operators)?
- [ ] Which relationship in ad_edges.csv surprises you?

> Hint: `grep -c` counts lines; `awk -F, '$7=="no"'` keeps accounts whose mfa column says no.

?> How many accounts are in users.csv? :: 12

?> How many accounts have no MFA? :: 4
