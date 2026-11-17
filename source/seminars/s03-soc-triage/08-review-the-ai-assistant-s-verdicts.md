## 8. Review the AI assistant's verdicts

The SOC's AI triage assistant gave a verdict on every alert. It is fast and usually right, but it only sees the alert text, not your evidence, and it reads **everything** in that text, including words an attacker wrote. Agree, or override it and say why. **Every override needs a fact** from the evidence.

- [ ] Read each verdict and its reason
- [ ] Agree or override
- [ ] For each override, the fact that proves it wrong
- [ ] For each override, the kind of mistake: too trusting, too alarmed, missing context, or obeying text an attacker wrote

> Hint: Four verdicts are wrong. One trusted a display name. One believed a sentence inside the email that was written for it. One was alarmed by encoding without decoding it. One didn't know about the trade show.

```tool aisec
{"file": "ai-verdicts.json", "marks": {"AL-4101": "agree", "AL-4102": "override", "AL-4103": "override", "AL-4104": "agree", "AL-4105": "agree", "AL-4106": "override", "AL-4107": "agree", "AL-4108": "agree", "AL-4109": "override", "AL-4110": "agree"}, "n": 10, "blank": ["marks"]}
```

?> How many AI verdicts did you override? :: 4
