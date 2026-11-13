# Lecture script: Identity from both sides: AD, Entra and cloud IAM

Seminar 7 · about 300 minutes of lab work · the video runs about 6 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word, so a recording made with `./teach demo` already has subtitles.

## Opening

Welcome to Identity from both sides. Almost every serious breach goes through accounts: a password, a group, a saved login, a cloud key. Today you'll look at Nimbus Analytics twice. First as the auditor, reviewing who has what. Then as the attacker, who started with one helpdesk password on Tuesday morning and owned the domain and the cloud account by lunch. Then you'll close each door, and write rules that catch the next one.

## 1. Who's who

Start like an auditor, before any alert. Twelve accounts. Four without MFA, and two of those are service accounts, which can't use it, so they need other protection. Then the relationships: who's a member of what, who can reset whose password, who's an admin where, and who's signed in where. One line stands out: the helpdesk can reset the SQL service account's password.

On screen: the step text, the Linux cell.

## 2. Review access like an auditor

The review tab does the auditor's checklist. A contractor in Server Admins: critical. A salesperson nobody has seen since June: disable it. A former analyst, disabled but still in groups: clean it up. And the SQL service account is a server admin with a password nobody has changed. We decide, and write one line of why for each.

On screen: the step text, the tool with the model answer.

## 3. Walk it like an attacker

Now the attacker's view. From h.verma: member of Helpdesk, Helpdesk can reset svc-sql's password, svc-sql is a Server Admin, Server Admins are admins on app02, and on app02 the domain admin's login is saved because a scheduled task runs as her. Five hops from a helpdesk password to the whole domain. Breaking the saved login on app02 cuts the most.

On screen: the step text, the tool with the model answer.

## 4. The kerberoast in the logs

The attacker didn't need the password reset. Any user can ask for a service ticket, and with the old RC4 cipher it can be cracked offline. On the domain controller: six 4769 requests in ten seconds, all 0x17, RC4, from the helpdesk PC, for every service account. Everyone else's tickets are AES. Zeek's Kerberos log shows the same six. That's kerberoasting.

On screen: the step text, the Linux cell, the tool with the model answer.

## 5. From a service account to the domain

An hour later, svc-sql logs on to app02 from the helpdesk PC. It saves the SECURITY and SYSTEM hives: that's where the scheduled task keeps the domain admin's password. Then it searches the report scripts for an access key. At 11:40 adm.k.nair logs on to the DC from app02, and a minute later asks for replication: a DCSync. DC02 does that every two hours; a person never should.

On screen: the step text, the tool with the model answer.

## 6. The cloud side: one key in a script

The key was in a script. In the audit trail, from 198.51.100.200: who am I, list the buckets, download four client export files, then create a new user called ops-backup, give it a policy and a key. That's the way back in. The only thing stopped was turning off the audit trail, by the one guardrail they had. And all of it was allowed because the nightly upload job had a policy that said star on star.

On screen: the step text, the Linux cell.

## 7. Least privilege: the policy diff

Least privilege, tested. The upload job only ever puts files in the reports bucket, from the office. So that's all it gets. And a guardrail: nobody creates users or keys without MFA. Replay the audit log: zero attacker actions allowed, zero normal actions broken. Two lines of diff that a reviewer can check. Then the real fix: no key in a script at all.

On screen: the step text, the tool with the model answer.

## 8. Detections for next time

Two Sigma rules. Kerberoasting: service tickets with RC4 for service accounts. Six hits, no AES tickets. DCSync: the replication right, used by anything that isn't a domain controller. Without the filter it fires on DC02 every two hours; with it, only adm.k.nair. And one line each on how they'd be evaded, because a rule you think is perfect stops you looking.

On screen: the step text, the tool with the model answer.

## 9. The fix, hop by hop

Now the fix, in order. Stop the bleeding: kill the new cloud user and the stolen key. Rebuild trust in the domain: krbtgt twice, then every admin and service password. Then the causes: no saved admin logins on servers, no service accounts in admin groups, no RC4, no reset rights over service accounts, MFA, the policy diff, a role instead of a key, and the two rules.

On screen: the step text, the tool with the model answer.

## 10. Hand in

Hand in the notebook: the review, the attack path, the log findings, the policy diff, both rules and the report. The rubric is on screen.

On screen: the step text.

## Wrap-up

That's identity from both sides. The review flagged the risky accounts, the graph showed the path, and the logs showed the attacker walk it: a kerberoast, a saved admin login on a server, a DCSync, and a cloud key in a script. Each hop has a fix, and two rules now watch for the loudest steps. Next is seminar eight, where the cloud and the pipeline become the attack surface.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:32 1. Who's who
1:03 2. Review access like an auditor
1:33 3. Walk it like an attacker
2:03 4. The kerberoast in the logs
2:33 5. From a service account to the domain
3:06 6. The cloud side: one key in a script
3:43 7. Least privilege: the policy diff
4:15 8. Detections for next time
4:45 9. The fix, hop by hop
5:18 10. Hand in
5:34 Wrap-up
```
