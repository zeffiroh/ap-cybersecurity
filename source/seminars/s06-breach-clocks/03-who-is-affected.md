## 3. Who is affected

The third question: to whom. The response log lists every record the scraper received and the country each customer lives in. The countries decide which clocks apply: everyone is covered by India's rules, and residents of the EU may bring in GDPR.

- [ ] Count the records by country
- [ ] Which fields were exposed? Which are the most sensitive?
- [ ] How many affected customers live in the EU?

> Hint: `cut -d, -f2 | sort | uniq -c` counts by the second column. Skip the header line with `tail -n +2`. Germany is DE, Ireland IE; the UAE (AE) is not in the EU.

?> How many affected customers live in the EU? :: 64
