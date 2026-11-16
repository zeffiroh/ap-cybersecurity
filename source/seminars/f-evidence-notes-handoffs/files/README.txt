Kestrel Logistics, a freight company. Monday 2 November 2026. All times are UTC (India is UTC+5:30).
Proxy times are Unix epoch seconds; turn them into UTC before you write them down.

hr-pc07      10.20.0.14   HR laptop (priya.nair)
fin-pc02     10.20.0.15   Finance laptop (dev.kapoor)
fs01                      file server with the HR, Finance and Ops shares
mail                      the company mail server

08:51  A fake invoice from kestrel-logistlcs.com (one letter off) reaches three people.
09:16  The report-phish button opens helpdesk ticket 88213.
09:52  The helpdesk pulls the network cable on hr-pc07.

What you have:
  ticket-88213.txt      the helpdesk ticket nobody can act on
  handover-night.txt    last night's "all quiet" handover
  alerts.json           the ten alerts from the SIEM that morning
  mail.log, invoice.eml the delivery log and the reported message
  proxy.log             web proxy log (epoch times)
  process.csv           EDR process list from hr-pc07 and fin-pc02
  share_listing.txt     the file server shares, listed at 09:58 after the cable was pulled
