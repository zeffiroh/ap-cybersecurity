## 2. Scope it from the logs

Regulators will ask three questions first: what happened, how much, and to whom. Answer the first two from the API log. The log's times are in IST, so convert them before you write anything down.

- [ ] How many requests came from 198.51.100.66? How many different customer IDs?
- [ ] When was the first and the last one (IST, then UTC)?
- [ ] What does a normal app request look like, for comparison?

> Hint: `grep -o '/customers/[0-9]*' | sort -u | wc -l` counts different IDs. `head -1` and `tail -1` give the first and last line.

?> How many different customer records did 198.51.100.66 receive? :: 2060

?> At what time (UTC, HH:MM) did the scraping start? :: 03:10
