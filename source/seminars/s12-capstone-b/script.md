# Lecture script: Capstone B: a breach across teams

Seminar 12 · about 480 minutes of lab work · the video runs about 7 minutes

Read it aloud while the demo plays (add `&demo=1` to the lab link), or record your own screen with the Teaching Desk. The demo's captions are this text, word for word, so a recording made with `./teach demo` already has subtitles.

## Opening

Welcome to Capstone B. This is the whole job in one day, with no hints. It's an exercise set in November 2027. Indigo Ledger runs payroll for other companies, so the data at risk isn't even theirs: it's their clients' employees' salaries and bank accounts. The cloud team saw something odd at dawn. The trail runs through the VPN, the network, a Windows server and the cloud account. You'll rebuild it, scope it, contain it, file and notify on time, leave detections behind, and brief the board. Take your time; work like a team of one.

## 1. Brief, custody, plan

No hints today. Read the brief and the alert, hash every file, and write a plan before you open a log. The clock starts at 05:35, when the on-call analyst acknowledged the alert. Everything else follows from that.

On screen: the step text, the Linux cell.

## 2. How they got in

The VPN log shows a spray: one guess each against 18 accounts, half a minute apart, from one address. Seventeen fail because MFA is on. One gets in: the summer intern's account, left active four months after the internship ended, with no MFA. The directory export confirms it, and shows it can still read the IT scripts share.

On screen: the step text, the Linux cell.

## 3. Across the network

Inside, the VPN address sweeps port 445 across 44 addresses in two minutes. Most refuse. On files01 it opens the IT scripts share and reads backup-config dot ps1. That script holds two secrets: the local administrator password used on every app server, and the cloud key for the backup uploads. One file, two doors.

On screen: the step text, the Linux cell.

## 4. On the application server

On pay-app01: localadmin logs on over the network with NTLM from the VPN address, using the password from the script. A PowerShell script runs, the payroll exports are zipped, and curl uploads the zip to a file-drop site. Then the files are deleted and the Security log is cleared, event 1102. But Zeek still saw 182 megabytes leave for 203.0.113.230.

On screen: the step text, the tool with the model answer.

## 5. In the cloud

The cloud key from the same script is used from the attacker's address at 04:20: who am I, list the bucket, then 12 downloads, three months of payroll for four clients. An attempt to make the bucket public is denied, only because the key's policy happened not to include bucket policies. Lucky, not designed.

On screen: the step text, the Linux cell.

## 6. One timeline

One clock. 02:58 the intern's account gets in. 03:15 the scan. 03:40 the script. 04:05 the app server. 04:20 the cloud key. 04:31 the zip, 04:52 the upload, 05:02 the log is cleared. 05:20 the alert, 05:35 someone looks. Two routes out for the same data, and about an hour between the theft and anyone looking.

On screen: the step text, the tool with the model answer.

## 7. Scope: whose data, how much

Whose data: four clients' employees, 2,505 people, with salaries, bank accounts and PAN. One client is a bank regulated by the RBI, with its own six-hour clock, so it needs facts from us within the hour. One has staff on secondment from the EU. And here's the key point: Indigo is the processor. The clients decide what the data is for, so they're the ones who must tell their employees and the Board, and we must tell them at once.

On screen: the step text, the Linux cell.

## 8. Contain and fix

Contain in order: cut the session, disable the account, block the addresses. Revoke the key, reset every local admin password, uniquely per server. Isolate the app server and image it. Then the causes: secrets out of scripts, MFA on every VPN account, leavers disabled on their last day, and a backup key that can only upload from the office. Replay: zero and zero.

On screen: the step text, the tool with the model answer.

## 9. File and notify

File with CERT-In inside six hours: data breach, with the entry, the systems, the indicators and what's done. Then the order that's special here: Indigo is a processor. The clients are the fiduciaries, so they notify the Board and their employees, and we tell them at once with facts and a draft notice. The regulated bank goes first because its own clock starts when it hears from us.

On screen: the step text, the tool with the model answer.

## 10. Leave detections behind

Two detections. A search for VPN failures grouped by source: one address with 17 failures across as many accounts, at 02:51, nearly three hours before anyone noticed. And a Sigma rule for a local admin logging on over the network, which should never happen: it fires at 04:05.

On screen: the step text, the tool with the model answer.

## 11. Brief the board, report to the team

Two documents. The board briefing asks for three decisions first: tell all four clients now, MFA and same-day leaver removal this week, and an outside firm to confirm scope. Then what we know and don't, in plain words. The technical report carries everything else, and every time in it matches the timeline.

On screen: the step text, the tool with the model answer.

## 12. Hand in

Hand in the notebook. Your teacher grades it against the rubric, and your Capstone B certificate is issued once it's graded.

On screen: the step text.

## Wrap-up

That's a breach across every team, handled by one person. A sprayed VPN password on an account that should have been closed, a scan, a script holding two secrets, a local admin password reused, salary files out by two routes, every clock met, two detections left behind, and a board briefing that asks for three decisions. That's the end of the seminar series. Your certificate comes after your teacher grades this hand-in.

## YouTube chapters (estimate; `./teach demo` writes the exact ones)

```
0:00 Opening
0:41 1. Brief, custody, plan
1:02 2. How they got in
1:31 3. Across the network
1:59 4. On the application server
2:29 5. In the cloud
2:57 6. One timeline
3:25 7. Scope: whose data, how much
4:03 8. Contain and fix
4:34 9. File and notify
5:07 10. Leave detections behind
5:33 11. Brief the board, report to the team
5:59 12. Hand in
6:14 Wrap-up
```
