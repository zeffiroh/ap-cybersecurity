Chandni Textiles, Surat: fabric and sarees, sold in two shops and online. Monday 9 November 2026.
All times are UTC (India is UTC+5:30, so 19:00 UTC is 00:30 IST on Tuesday).

shop01                        the online shop, Linux. SSH is open to the internet so the photo studio can upload.
lookbook                      the lookbook and blog site (www), a separate server
accts-pc02.chandni.lan        the accounts PC, Windows 11 (Hetal Desai, accounts)
10.30.0.30                    the photo studio PC; it logs in to shop01 as catalog to upload product photos
10.30.0.12                    Ravi, who looks after the servers

The question for the whole seminar: did anyone get into shop01, how did they do it, and what did they take?
On Monday the accounts PC also opened a spreadsheet from an email; IT collected its Windows log.

What you have:
  auth.log                   shop01 SSH and sudo log, 9 Nov
  access.log                 shop01 web server log, 9 Nov
  lookbook_access.log        the lookbook site's web log, 9 Nov 10:00 to 11:00: an hour of normal visitors, for testing false positives
  eventlogs/Security.jsonl   Windows Security log from accts-pc02, 9 Nov (one event per line)
