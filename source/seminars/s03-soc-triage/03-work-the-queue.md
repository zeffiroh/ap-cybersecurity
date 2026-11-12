## 3. Work the queue

Now give all ten alerts a disposition and a one-line reason. **Exactly one** should be escalated: the one where a person must act in the next hour. Already-contained activity is "true positive: handled". A rule that fired on something harmless is "false positive".

- [ ] Every alert has a disposition
- [ ] One escalation
- [ ] Each reason points at evidence
- [ ] Write the notes for the next shift

> Hint: AL-3106 runs every day at 09:00 under an IT service account. Decode the command in the next step before you decide.

```tool alerts
{"file": "alerts-tuesday.json", "d": {"AL-3101": "handled", "AL-3102": "escalate", "AL-3103": "benign", "AL-3104": "benign", "AL-3105": "handled", "AL-3106": "false", "AL-3107": "handled", "AL-3108": "benign", "AL-3109": "false", "AL-3110": "handled"}, "n": 1, "blank": ["d"]}
```

?> Which alert is the one to escalate? :: AL-3102
