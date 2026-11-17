# Lecture script: Identity from both sides: AD, Entra and cloud IAM

Seminar 7 · about 300 minutes of lab work · about 21 minutes of narration

This is what `python tools/teach.py demo s07-identity` plays and captions, word for word, and what the voice studio
(`python tools/teach.py voice s07-identity`) shows you to read. Edit the words in seminar.json, then run
`python tools/teach.py script s07-identity` to refresh this file.

## Opening

Hello, and welcome to Identity from both sides. Almost every serious breach goes through an account: a password, a group, a saved login, a cloud key. Nimbus Analytics, a data firm in Hyderabad, has a Windows domain for its office and a cloud account for client data. On Monday the ninth of November 2026, Harsh Verma, a helpdesk analyst, typed their password into a phishing page. On Tuesday someone used it from that same helpdesk PC, through a remote control tool that had been left running. In about three hours they had every password in the domain, four files of client data from the cloud, and a cloud user of their own to come back with. We'll look at Nimbus twice. First as the auditor, reviewing who has what. Then as the attacker, walking the same directory from one helpdesk password to the top. Then we'll follow the footprints in the logs and close every door. One thing before we start: every time in this case is UTC, as most logs are. Hyderabad is five and a half hours ahead, so 09:12 in the logs is 14:42 on the office clock.

## 1. Who's who

Step one: who's who. Start like an auditor, before you read a single alert. An attacker who gets into a network doesn't start with exploits. They start by reading the directory: who exists, which groups they're in, and who can control whom. So we read it first. users.csv is the export of every account: name, department, title, whether it's active, MFA, last logon and groups. ad_edges.csv is the relationship graph: each line is one thing that one account or group can do to another. The Linux cell prints both, counts the lines, and lists the accounts whose MFA column says no.

*After it runs:*

The count says thirteen, but there are twelve accounts: the first line is the header. Always check what a count includes. Four accounts have no MFA: h.verma on the helpdesk, a.khan in Sales, and two service accounts, svc-sql and svc-backup. Service accounts are used by programs, not people, so they can't answer a prompt on a phone; they need other protection, and we'll come to what. Now the powerful groups. Domain-Admins has one member, adm.k.nair, the separate admin account of Kavya Nair, the infrastructure lead. Server-Admins has three members: svc-sql, n.ali, a systems engineer, and t.mehta, a contractor data engineer in Analytics. Backup-Operators has svc-backup. Then read the edges. Most are what you'd expect. One isn't: Helpdesk, ForceChangePassword, svc-sql. The helpdesk can reset the SQL service account's password, and the note says that right was inherited on the Service Accounts folder in 2023. Nobody decided it; nobody ever took it away. One more line deserves a second look: adm.k.nair, HasSessionOn, app02. A domain admin's login is saved on a reporting server, because a scheduled task called Nightly KPI export runs as that account. Answer the questions: twelve, and four.

On screen: the step text, the Linux cell.

## 2. Review access like an auditor

Step two: review access like an auditor. An access review is one of the most boring controls in security, and one of the most effective. Every few months, someone looks at every account and asks three questions. Does this person still need it? Does this account have more than it needs? Is it protected well enough for what it can do? The Access review tab asks those questions for us and flags the classic problems. Our job is the part a tool can't do: a decision for each flagged account, keep, reduce, disable or delete, with one line of why.

*After it runs:*

The worst first. t.mehta is a contractor in Server-Admins, with a contract that ends on the thirty-first of December. That's the one critical finding. A data engineer needs the data, not admin rights on every server, so: reduce. s.rao in Sales last logged on on the twenty-second of June, a hundred and forty days ago. Disable, don't delete: if it turns out to be long leave, the account can be switched back on in a second. p.das left at the end of September. The account is disabled but still in two groups, one of them Repo-All-Read. A disabled account in groups is a loaded spring: one mistaken re-enable and everything comes back. The leaving is confirmed, so: delete. svc-sql is a service account in Server-Admins. A program that runs reports doesn't need to be an administrator on every server, so: reduce. a.khan and h.verma have no MFA. They keep their accounts, and the reason line says MFA this week. And for the service accounts, what replaces MFA is a long random password that nobody types, ideally a managed service account, where Windows changes the password by itself, and a rule that the account can never log on interactively. Which finding would you fix first? Most people say the contractor, because it's marked critical. Keep that answer in mind. Answer the question: t.mehta.

On screen: the step text, the identity tool with the model answer.

## 3. Walk it like an attacker

Step three: walk it like an attacker. Defenders think in lists: accounts, groups, settings. Attackers think in graphs: from where I am, what can I reach? The Attack paths tab draws ad_edges.csv as a graph. Start from h.verma, the account that was phished, and ask for paths to Domain-Admins. Every arrow is one thing the attacker can do with what they already have. No exploit needed.

*After it runs:*

Here's the path, one arrow at a time. h.verma is a member of Helpdesk. Helpdesk can force a password change on svc-sql, so the attacker can set svc-sql's password to anything they like. svc-sql is a member of Server-Admins. Server-Admins are administrators on app02 and sql01. On app02, adm.k.nair has a session: the Nightly KPI export runs every night as adm.k.nair with a saved password, and any administrator on app02 can take that saved password. adm.k.nair is in Domain-Admins, and Domain-Admins are administrators on dc01, the domain controller. From one helpdesk password to the whole domain, and the only password the attacker had to steal was the first one. Now the questions that make this useful. Who else can walk the path from Server-Admins onwards? t.mehta and n.ali. Phish either of them and you skip the first two hops. And look at one more line: svc-backup is in Backup-Operators, and Backup-Operators can back up dc01, which means reading the domain database. That's a second road to the same place. Which single change breaks the most paths? Not the contractor. It's the saved admin login on app02. Remove it, and every path through Server-Admins ends at a reporting server instead of the domain. That's why we don't fix findings in the order a tool scores them. We fix the ones that cut the graph. Answer the questions: svc-sql, and app02.

On screen: the step text, the identity tool with the model answer.

## 4. The kerberoast in the logs

Step four: the kerberoast in the logs. Here's the twist: the attacker didn't need the password reset at all. In Kerberos, any domain user can ask the domain controller for a service ticket for any account that has a service name, an SPN. Part of that ticket is encrypted with a key made from the service account's password. If the ticket uses the old RC4 cipher, the attacker can take it away and guess passwords against it offline, and the domain never sees a single failed login. That's kerberoasting. The Event viewer opens dc01's Security log, filtered to event 4769, a Kerberos service ticket was requested, and to encryption type 0x17. Then the Linux cell reads Zeek's Kerberos log from the network sensor in front of the servers.

*After it runs:*

At 09:12:04, h.verma gets a ticket-granting ticket from hd-pc04, 10.60.2.31. That's event 4768, and it's AES: normal. Two and a half minutes later, from 09:14:31 to 09:14:41, come six service tickets, two seconds apart: svc-sql, svc-backup, svc-web, svc-report, svc-crm and svc-etl. Every service account in the domain, and every ticket encryption type 0x17, RC4-HMAC. Now look at normal: people ask for the servers they work on, a few times an hour, and every one of those tickets is 0x12, AES-256. Nobody asks for six service accounts in ten seconds, and no modern computer picks RC4 when it can use AES. A cracking tool asks for RC4 on purpose. Zeek tells the same story from the wire. Count the cipher column: twenty-seven AES tickets and six rc4-hmac, all six from 10.60.2.31, all six for h.verma. Two sources that agree are worth far more than one. And notice svc-backup in that list: the second road from step three just got its ticket too. Answer the questions: six, and rc4-hmac.

On screen: the step text, the Linux cell, the events tool with the model answer.

## 5. From a service account to the domain

Step five: from a service account to the domain. At 10:05, svc-sql starts doing things. How did the attacker get its password? dc01's log has no 4724, the event for a password reset, so the likelier answer is the cracked ticket. That tells you something too: svc-sql's password was weak enough to guess. Follow svc-sql on app02 first, through events 4624, a logon, 4672, special privileges, and 4688, a new process. Then go to the domain controller and event 4662, an operation was performed on an object. That's where a DCSync shows up.

*After it runs:*

10:05:12: svc-sql logs on to app02 over the network, logon type 3, from 10.60.2.31, the helpdesk PC again. In the same second, 4672: special privileges, including SeBackupPrivilege and SeDebugPrivilege. At 10:09:40 and 10:09:44, reg.exe saves two parts of the registry into C:\Windows\Temp: HKLM\SECURITY as sec.hiv, and HKLM\SYSTEM as sys.hiv. Why those two? The SECURITY hive holds what Windows calls LSA secrets, including the saved password the Nightly KPI task uses, and the SYSTEM hive holds the key that unlocks them. Take both away and you can read the password on your own machine. Now look at the very first line of app02's log: at 02:00:01, adm.k.nair logged on with logon type 4, a batch logon. That's the scheduled task, running every night, and keeping the domain admin's password on this server. At 10:31:02, findstr searches every PowerShell script under C:\Reports for the word AccessKey. The attacker is looking for a way into the cloud. Now the domain controller. At 11:40:18, adm.k.nair logs on to dc01 over the network from 10.60.1.22. That's app02, not 10.60.2.11, where k.nair normally works. At 11:41:02 and 11:41:03 come two 4662 events by adm.k.nair on the domain object itself, with two property GUIDs. 1131f6aa is Replicating Directory Changes, and 1131f6ad is Replicating Directory Changes All. Together they mean: send me every password hash, the way one domain controller asks another. That's a DCSync. Now the trap. There are other 4662s with the same right, at 09:15, 11:15 and 13:15, by DC02 dollar. DC02 is the second domain controller, replicating every two hours, exactly as it should. Names ending in a dollar sign are computer accounts. A person should never appear here. Answer the questions: adm.k.nair, and 10.60.1.22.

On screen: the step text, the events tool with the model answer.

## 6. The cloud side: one key in a script

Step six: the cloud side, one key in a script. The findstr found what it was looking for. C:\Reports\sync.ps1 has an access key and its secret written straight into the script, so the nightly job can upload the KPI file. Now read the cloud audit trail: every call to the cloud account, who made it, from which address, and whether it worked. The Linux cell pulls out the identity, the action and the source address of every call, and counts each combination.

*After it runs:*

Start with normal, so the abnormal stands out. Every night at 02:05:10, reporting-sync puts one KPI file into nimbus-reports, from 203.0.113.60, the office, with the user agent nimbus-sync. Then, at 12:02:04: reporting-sync, the same key, from 198.51.100.200, with a different program, stratus-cli. Its first call is GetCallerIdentity: who am I? That's the first thing anyone does with a stolen key, find out whose it is. At 12:02:30, ListBuckets. Between 12:04:02 and 12:04:29, four GetObject calls: client-01 to client-04, parquet files from client-exports, October 2026. That's client data leaving. Then at 12:09:50 CreateUser ops-backup, at 12:10:03 AttachUserPolicy, and at 12:10:15 CreateAccessKey. A name chosen to look boring, with a key of its own. If Nimbus only revokes the stolen key, the attacker is still in. At 12:14:40, ops-backup lists the buckets: testing the new key. And at 12:15:02, ops-backup tries StopLogging on the main trail, to switch off the very log we're reading. Denied. The only thing that stopped them all day was one organisation guardrail, protect-audit-trail. Load policies.json into the Cloud IAM simulator and replay the audit log as it is: every attacker action is allowed except that one. Why? Because reporting-sync's policy is called reporting-full, and it says allow star on star. A job that uploads one file a night could do anything an administrator could. Answer the questions: 198.51.100.200, and ops-backup.

On screen: the step text, the Linux cell.

## 7. Least privilege: the policy diff

Step seven: least privilege, the policy diff. Least privilege sounds simple: give each identity what it needs and nothing more. The hard part is knowing what it needs, and the audit trail tells us. Rewrite the policies, then replay the log after every change. The simulator gives two numbers: attacker actions still allowed, and normal actions you broke. A policy that stops the attacker but breaks the nightly upload isn't a fix, it's an outage. Aim for zero and zero.

*After it runs:*

In three nights of logs, reporting-sync did exactly one thing: PutObject into nimbus-reports, from the office. So that's its whole policy now: allow PutObject on bucket nimbus-reports star, only when the source address is 203.0.113.60. Replay. Every call from 198.51.100.200 is denied, because the address doesn't match, so even if the key leaks again it's useless away from the office. Then a second line, for everyone: an organisation guardrail that denies CreateUser, CreateAccessKey and AttachUserPolicy unless the caller signed in with MFA. Why for everyone, and not just reporting-sync? Because next time the stolen key might be an admin's. Replay again, and watch the normal actions. At 08:03, k.nair created an access key. Still allowed, because that was done with MFA. Zero attacker actions allowed, zero normal actions broken. The diff is two lines a reviewer can check in a minute. But this is still the second-best fix. The best fix is no key in a script at all. app02 should get a role: short-lived credentials handed to the server and renewed automatically, so there's nothing for findstr to find. Answer the question: zero.

On screen: the step text, the cloudiam tool with the model answer.

## 8. Detections for next time

Step eight: detections for next time. The review and the policy close today's doors. Detections are for the next attacker, who'll try a door we haven't thought of. We'll write two Sigma rules. Sigma is a shared format for writing a detection once and running it in any SIEM. We test both on dc01's log. A rule isn't finished when it matches the attack. It's finished when it matches the attack and stays quiet on a normal day.

*After it runs:*

The kerberoast rule: event 4769, ticket encryption type 0x17, and a service name that starts with svc dash. Run it: six matches, the six tickets from 09:14, and none of the AES tickets. It's tagged T1558.003 in ATT&CK, Kerberoasting. The DCSync rule: event 4662 with either replication GUID. Run it without the filter first. Five matches, three of them DC02 dollar. That rule would wake someone up every two hours, and within a week everyone would ignore it. Add the filter, which drops accounts ending in a dollar sign. Two matches, both adm.k.nair at 11:41. Level critical, tagged T1003.006. Now write one line on how each rule could be evaded, because a rule you think is perfect stops you looking. The kerberoast rule only sees RC4: an attacker who asks for AES tickets cracks more slowly but raises no alert, and a service account that isn't named svc dash is invisible to it. The DCSync rule trusts every name ending in a dollar: an attacker who gives the replication right to a computer account they control walks straight past the filter. The stronger filter is a list of your real domain controllers. Answer the question: two.

On screen: the step text, the sigma tool with the model answer.

## 9. The fix, hop by hop

Step nine: the fix, hop by hop. Now write it so someone can act on it tonight. The report builder has the incident template ready. The part that matters most is the order. Containment first, so the attacker can't use what they already have. Then rebuild trust in the domain, because after a DCSync you have to assume they have every password. Then the root causes, one for each link in the chain.

*After it runs:*

In order. One: disable ops-backup and revoke every reporting-sync key, in the same few minutes, so the attacker can't use one to rebuild the other. Two: reset krbtgt, twice. krbtgt is the account whose key signs every Kerberos ticket in the domain. The DCSync took it, so the attacker can forge a ticket for anyone, a golden ticket. The domain also accepts the previous krbtgt password, so one reset isn't enough. Between the two resets you normally wait for replication and for tickets to expire, ten hours by default. Then reset every admin and service account password. Three: remove the Nightly KPI task's saved admin login and run it as a managed service account. That one change cuts the path. Four: svc-sql out of Server-Admins, a thirty-character random password, and no RC4 for service accounts. Five: take away Helpdesk's reset rights on the Service Accounts folder. Six: MFA for every user account, starting with the helpdesk. Seven: the policy diff and the guardrail. Eight: a role for app02 instead of a key. Nine: deploy the two rules. Then the people. The CISO was told at 13:10. Under CERT-In's directions, an incident like this must be reported within six hours of noticing it. And four client data files left, so Nimbus must tell those clients as their contracts require. Read the last line of the report twice: the access review had already flagged three of the five links. Reviews only help if someone acts on them.

On screen: the step text, the report tool with the model answer.

## 10. Hand in

Step ten: hand in. The notebook carries everything you've done: the review decisions, the attack path, the log findings, the policy replay at zero and zero, both rules, and the report. Check the list, then press Hand in.

*After it runs:*

The rubric is on screen. The most points, five, go to the policy diff, because it's the hardest thing to get right: stopping every attacker action without breaking normal work. If you're short of time, don't skip the order of the fixes. In a real incident, that's the part people act on.

On screen: the step text.

## Wrap-up

That's identity from both sides. As the auditor, you found the risky accounts and made a decision for each. As the attacker, you saw that the most dangerous thing in the directory wasn't an account at all: it was a saved login on one reporting server. In the logs you watched the attacker walk it, from a kerberoast to a DCSync to a cloud key in a script. Then you closed it: two lines of policy, two rules, and nine fixes in the right order. The lesson to keep is that identity is a graph, not a list. Fix the links that cut the most paths, and give every account, person or program, only what its job needs. Next is seminar eight, Cloud and DevSecOps, where the pipeline itself becomes the attack surface. Thank you for watching.

## YouTube chapters (estimate; `python tools/teach.py demo s07-identity` writes the exact ones)

```
0:00 Opening
1:27 1. Who's who
3:27 2. Review access like an auditor
5:43 3. Walk it like an attacker
7:49 4. The kerberoast in the logs
9:54 5. From a service account to the domain
12:35 6. The cloud side: one key in a script
14:41 7. Least privilege: the policy diff
16:34 8. Detections for next time
18:35 9. The fix, hop by hop
20:49 10. Hand in
21:25 Wrap-up
```
