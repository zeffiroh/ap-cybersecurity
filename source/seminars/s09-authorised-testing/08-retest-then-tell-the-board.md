## 8. Retest, then tell the board

Retest each fix the same way you proved it: the same request should now fail. Then write the board note: no SQL, no CVSS, just what could have happened to the business, what it costs to fix, and what you need them to decide.

```tool report
{"tpl": "escalation", "title": "Note to the board: what the security test found", "text": "# Note to the board: what the security test found\n\n## The ask\n\nPlease approve a one-week fix sprint starting Monday 23 November, and make a retest before any release a standing rule.\n\n## Severity and why\n\nHigh. Today, anyone on the internet could log in to the shop as its administrator, read other customers' orders, and impersonate any user on our test system.\n\n## What we know\n\n- The tester proved each problem with one request, using only a demo account; no customer data left the test.\n- Each problem has a clear, small fix: about two days of developer time in total.\n\n## What we don't know\n\n- Whether anyone found these before us. The logs from before 16 November should be checked for the same requests.\n\n## Impact so far\n\nNone known. If exploited: changed prices and orders, customers' addresses exposed (a personal data breach to report), and loss of trust in the shop.\n\n## What I've done\n\nShared the findings with Engineering on 20 November; the login fix is already in testing.\n\n## Evidence\n\nThe findings report and rules of engagement, 20 November 2026; retest booked for 25 November.\n", "n": 7, "blank": ["text"]}
```

- [ ] The ask is the first line
- [ ] Impact in business words: money, customers, regulators
- [ ] What you don't know (has anyone else found these?)

> Hint: Boards decide on money, time and risk. "Two days of developer time to close three ways in" is a decision they can make.
