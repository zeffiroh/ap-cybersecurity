## 1. How the alert queue works

Before you triage, learn the program. An alert queue (the triage console of a SOC) takes alerts from many sources, the mail gateway, the proxy, antivirus, sign-in logs and staff who press **Report phishing**, and lines them up for a person to decide.

Every alert carries the same fields: an **ID**, the **time**, the **rule** that fired, the **host** and **user** it is about, a **detail** line, and the **evidence** files to open next. The queue doesn't decide anything. You give each alert one **disposition**:

| Disposition | Meaning |
|---|---|
| True positive: escalate | Real, and a person must act now |
| True positive: handled | Real, and already contained (blocked, removed, quarantined) |
| Benign: expected activity | The rule worked, but what it saw is normal here |
| False positive: rule fired wrongly | The rule matched something it was never meant to catch |
| Needs more information | You can't decide yet: write the question and who can answer it |

The Linux cell shows the raw queue file, so you can see that the program is only reading JSON. The queue below is the one you will work today, at **Lotus Lake Hotels** in Udaipur. Don't set any dispositions yet: just open it and look around. Read `README.txt` first.

- [ ] Compare the raw JSON with how the queue shows the same alert
- [ ] Open one alert's evidence list
- [ ] Find the summary line that counts dispositions

> Hint: The difference between "handled" and "benign" is whether anything bad happened. A blocked phishing click is handled; a scanner doing its job is benign.

```tool alerts
{"file": "alerts-wednesday.json", "d": {}, "n": 0, "blank": ["d"]}
```

?> Which field of an alert lists the files to open next? :: evidence

?> How many dispositions can you choose from? :: 5
