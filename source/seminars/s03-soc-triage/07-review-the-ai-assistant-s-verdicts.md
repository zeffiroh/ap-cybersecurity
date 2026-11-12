## 7. Review the AI assistant's verdicts

The SOC's AI triage assistant gave a verdict on every alert. It is fast and usually right, but it only sees the alert text, not your evidence. Agree, or override it and say why. **Every override needs a fact** from the evidence.

- [ ] Read each verdict and its reason
- [ ] Agree or override
- [ ] For each override, the fact that proves it wrong
- [ ] Which kind of mistake does it make: too trusting, or too alarmed?

> Hint: Three verdicts are wrong. One trusted a display name. One was alarmed by encoding without decoding it. One didn't know about the VPN exit.

```tool aisec
{"file": "ai-verdicts.json", "marks": {"AL-3101": "agree", "AL-3102": "override", "AL-3103": "agree", "AL-3104": "agree", "AL-3105": "agree", "AL-3106": "override", "AL-3107": "agree", "AL-3108": "agree", "AL-3109": "override", "AL-3110": "agree"}, "n": 10, "blank": ["marks"]}
```

?> How many AI verdicts did you override? :: 3
