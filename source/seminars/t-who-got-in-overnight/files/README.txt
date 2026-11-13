Tamarind Health, night of 5 to 6 November 2026. All times are UTC (India is UTC+5:30).

appt01       10.30.1.20   Ubuntu 22.04, the MediBook appointments server. SSH (port 22) is forwarded from the internet
                          so the software vendor can support it. Accounts: deploy (clinic IT, key only), vendor (the vendor).
rcp-pc03     10.30.2.33   Windows 11, reception PC at the Kothrud clinic. Shares D:\Scans (patient scans and referrals).
10.30.0.2                 DNS server        10.30.0.5   database        10.30.0.30  patient portal
10.30.0.15                IT admin PC       10.30.0.40  backup server

What you have:
  auth.log, ps.txt, crontab.txt         from appt01, saved by the IT contractor at 02:05
  recovered/m.sh                         the script found at /tmp/.m.sh on appt01
  capture.pcap                           the core switch mirror from 01:15 to 01:45
  zeek/conn.log                          the Zeek sensor's connection log, 01:00 to 02:00
  eventlogs/Security.jsonl               rcp-pc03's Security log, exported at 02:20

The IDS alert that started this, 01:20:11: "ET POLICY possible script download by Wget to external host" on appt01.
