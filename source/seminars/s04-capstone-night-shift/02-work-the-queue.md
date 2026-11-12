## 2. Work the queue

Give every alert a disposition and a reason. A reason is a log line or a fact you checked, not a feeling. Severity is yours to judge: the queue doesn't tell you.

- [ ] Every alert has a disposition
- [ ] Every reason points at evidence
- [ ] Alerts that belong to one intrusion say so
- [ ] Use "needs more information" only with a question someone can answer

> Hint: Five alerts are on fin-lt04 or about it. A program downloaded at 11:02 and a scheduled task at 11:04 on the same laptop are not a coincidence.

```tool alerts
{"file": "alerts-night.json", "d": {"AL-7301": "escalate", "AL-7302": "benign", "AL-7303": "escalate", "AL-7304": "escalate", "AL-7305": "benign", "AL-7306": "escalate", "AL-7307": "benign", "AL-7308": "escalate", "AL-7309": "benign", "AL-7310": "benign", "AL-7311": "benign", "AL-7312": "more"}, "n": 5, "blank": ["d"]}
```

?> Which host do the related alerts share? :: fin-lt04
