Saffron Pharma Distributors, a medicine wholesaler in Ahmedabad. Tuesday 10 November 2026. All times are UTC (India is UTC+5:30).
Proxy times are Unix epoch seconds; turn them into UTC before you write them down.

acct-lt04    10.30.0.21   Accounts laptop (meera.shah)
sales-lt11   10.30.0.33   Sales laptop (arjun.rao)
fs02                      file server with the Accounts, Purchase and Warehouse shares
vpn01                     the remote access VPN
mail                      the company mail server

10:12  A fake courier email about a held shipment reaches three people.
10:31  The report-phish button opens helpdesk ticket 55120.
11:14  The helpdesk unplugs acct-lt04 from the network.

What you have:
  ticket-55120.txt      the helpdesk ticket
  handover-night.txt    last night's handover
  alerts.json           the eleven alerts from the SIEM that morning
  mail.log, courier.eml the delivery log and the reported message
  proxy.log             web proxy log (epoch times)
  process.csv           EDR process list from acct-lt04 and sales-lt11
  share_listing.txt     the file server shares, listed at 11:20 after the laptop was unplugged
