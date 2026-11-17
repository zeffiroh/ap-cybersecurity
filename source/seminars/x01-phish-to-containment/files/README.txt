Kestrel Logistics, a freight company. Monday 2 November 2026. All times are UTC (India is UTC+5:30).
Proxy times are Unix epoch seconds; turn them into UTC before you write them down.

hr-pc07      10.20.0.14   HR laptop (priya.nair)
fin-pc02     10.20.0.15   Finance laptop (dev.kapoor)
acct-pc03    10.20.0.16   Accounts laptop
fs01         10.20.1.10   file server with the HR, Finance and Ops shares
mail         10.20.1.5    the company mail server
proxy        10.20.1.3    the web proxy every laptop uses

It is 09:16. Dev Kapoor in Finance has just pressed Report phishing on an email about an overdue invoice.
Helpdesk ticket 88213 opened by itself. Nobody has looked at it yet.

What you have:
  invoice.eml           the reported message (it's in Mail too)
  mail.log              the mail server's delivery log
  proxy.log             the web proxy log (epoch times)
  process.csv           the EDR process list from hr-pc07 and fin-pc02
  eventlogs/Security.jsonl  the Windows Security log from hr-pc07
  alerts.json           the SIEM alerts so far (they're in Tickets too)
  ticket-88213.txt      the helpdesk ticket
