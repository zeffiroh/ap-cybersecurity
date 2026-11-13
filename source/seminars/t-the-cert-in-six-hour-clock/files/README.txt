EXERCISE. Kaveri Microfinance Ltd, Bengaluru. Tuesday 8 June 2027. All times UTC unless marked IST (UTC+5:30).

This is a rehearsal set after the Digital Personal Data Protection Rules' breach duties start on 13 May 2027.
Check the current text of every rule before a real incident; this exercise follows the tool's summary of each clock.

Kaveri is a non-banking finance company regulated by the Reserve Bank of India. Its loan app "Kaveri" has 141,200 customers.
"Kaveri Remit" lets customers who live abroad (UAE, Germany, Ireland) repay loans for family members in India.

Systems:  api.kaveri.example  the app's API (/v2/...), behind a web application firewall (WAF)
People:   CISO Meenal Rao  ·  DPO Arvind Shetty  ·  CEO  ·  Board (meets on call)  ·  Head of compliance (RBI reporting)

What you have:
  waf_alert.txt              the SOC analyst's note that started this
  api_access.log             the API's access log for the morning (nginx format, times in IST)
  affected_customers.csv     the records the scraper received, from the API's own response log
  certin-kaveri.json         the CERT-In filing exercise (the tool reads it)
  tabletop-kaveri-clocks.json  the decisions you'll face
