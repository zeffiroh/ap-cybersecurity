Nimbus Analytics, Hyderabad. Tuesday 10 November 2026. All times UTC (India is UTC+5:30).

Active Directory domain NIMBUS (nimbus.lan)        Cloud account nimbus-prod (office egress 203.0.113.60)
dc01      10.60.1.10    domain controller
app02     10.60.1.22    reporting server: runs SQL reports and the "Nightly KPI export" task
hd-pc04   10.60.2.31    helpdesk PC, used by h.verma

What happened, as far as we know at 13:00: h.verma's password was phished on Monday. On Tuesday someone used it from hd-pc04
(remote control tool left running), and by lunchtime the cloud audit trail showed a new user nobody created.

What you have:
  identity/users.csv, identity/ad_edges.csv   directory export and the relationship graph (who can control what)
  eventlogs/dc01-Security.jsonl, eventlogs/app02-Security.jsonl
  captured/zeek-kerberos.log                  Zeek's Kerberos log from the server network sensor
  captured/app02-sync-ps1.txt                 the script with the cloud key
  cloud/policies.json, cloud/audit.json        the cloud account's identities and audit trail
