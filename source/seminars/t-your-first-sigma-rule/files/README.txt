Kestrel Logistics. Monday 2 and Tuesday 3 November 2026. All times are UTC (India is UTC+5:30).

web01                     the public web shop, Linux, SSH open to the internet
shop2                     a second web shop
hr-pc07.kestrel.lan       HR laptop, Windows 11 (the laptop that opened the fake invoice on 2 Nov)

The question for the whole seminar: did anyone guess an SSH password on web01, get in, and do something with it?

What you have:
  auth.log               web01 SSH and sudo log, 3 Nov
  access.log             web01 web server log, 3 Nov
  shop2_access.log       shop2 web server log, 3 Nov: an hour of normal shoppers, for testing false positives
  eventlogs/Security.jsonl   Windows Security log from hr-pc07, 2 Nov (one event per line)
