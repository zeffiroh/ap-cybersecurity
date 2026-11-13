## 6. Rank every finding

Forty findings and one team: what first? The register gives each finding a CVSS vector and two facts that matter more than the score: is it reachable from the internet, and is it being exploited? The CVSS tool scores each vector and ranks the register.

```tool patch
{"vec": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H", "n": 10, "blank": ["vec"]}
```

- [ ] Score F-01's vector in the calculator, then rank the whole register
- [ ] Which findings are "patch now"? Why those?
- [ ] Is anything ranked high that you'd move down, or the other way? Say why
- [ ] Add an owner and a date to every row

> Hint: The leaked key and the public invoices bucket are both internet-facing **and** already exploited. That beats a higher CVSS score on something nobody can reach.

?> Which finding ID should be fixed first? :: F-01
