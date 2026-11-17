## 3. Work the queue

Give every alert a disposition and a reason. A reason is a log line or a fact you checked, not a feeling. Severity is yours to judge: the queue doesn't tell you.

- [ ] Every alert has a disposition
- [ ] Every reason points at evidence
- [ ] Alerts that belong to one intrusion say so
- [ ] Use "needs more information" only with a question someone can answer

> Hint: Five alerts are on acc-lt03. A program from a three-day-old domain at 00:03, a remote access tool at 00:04 and a new program in ProgramData at 00:13 on the same laptop are not a coincidence.

```tool alerts
{"file": "alerts-night.json", "d": {"AL-8401": "escalate", "AL-8402": "benign", "AL-8403": "escalate", "AL-8404": "escalate", "AL-8405": "benign", "AL-8406": "escalate", "AL-8407": "benign", "AL-8408": "escalate", "AL-8409": "benign", "AL-8410": "benign", "AL-8411": "benign", "AL-8412": "more"}, "n": 5, "blank": ["d"]}
```

?> Which host do the related alerts share? :: acc-lt03
