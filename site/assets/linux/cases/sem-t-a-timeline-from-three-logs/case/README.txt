Garnet Precision Engineering, Chakan. Night of Friday 6 to Saturday 7 November 2026. All times are UTC (India is UTC+5:30).

vpn01        10.50.0.1    remote access VPN. MFA is optional; staff enrol themselves.
eng-ws14     10.50.2.14   Windows 11, design workstation in the engineering bay (normally used by s.kale)
fs02         10.50.1.12   Windows Server 2022, file server; D:\Shares\Engineering and D:\Shares\Quality
dc01         10.50.1.10   domain controller (GARNET)
VPN pool     10.50.9.0/24

00:12  Helpdesk ticket: "CAD files won't open, every folder has RESTORE-FILES.txt"
00:31  Incident team called. 00:58 the VPN session was cut by IT. fs02 and eng-ws14 were isolated at 01:10.

What you have:
  vpn.log, hr_note.txt, backups.txt, share_listing.txt
  eventlogs/eng-ws14-Security.jsonl, eventlogs/eng-ws14-Sysmon.jsonl, eventlogs/fs02-Security.jsonl, eventlogs/fs02-System.jsonl
  process.csv                       EDR process export from both machines
  captured/volatility-eng-ws14.txt  Volatility 3 run on the eng-ws14 memory image (taken 01:14)
  captured/hayabusa-fs02.csv        Hayabusa run on fs02's event logs
  captured/velociraptor-fs02-services.csv   Velociraptor service listing from fs02
  suspect/RESTORE-FILES.txt, suspect/locker.strings.txt
  tabletop-garnet-ransomware.json   the decisions you'll face next
