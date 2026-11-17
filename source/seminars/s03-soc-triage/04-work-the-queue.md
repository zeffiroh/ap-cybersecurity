## 4. Work the queue

Now give all ten alerts a disposition and a one-line reason. **Exactly one** should be escalated: the one where a person must act in the next few hours. Already-contained activity is "true positive: handled". Normal activity that a rule noticed is "benign". A rule that fired on something it was never meant to catch is "false positive".

- [ ] Every alert has a disposition
- [ ] One escalation
- [ ] Each reason points at evidence (a log line, a header, a file)
- [ ] Write the notes for the next shift

> Hint: AL-4106 runs every night at 21:30 UTC under an IT service account. Decode the command in the next step before you decide. For AL-4109, open travel.csv.

```tool alerts
{"file": "alerts-wednesday.json", "d": {"AL-4101": "handled", "AL-4102": "escalate", "AL-4103": "handled", "AL-4104": "benign", "AL-4105": "benign", "AL-4106": "false", "AL-4107": "handled", "AL-4108": "benign", "AL-4109": "benign", "AL-4110": "handled"}, "n": 1, "blank": ["d"]}
```

?> Which alert is the one to escalate? :: AL-4102
