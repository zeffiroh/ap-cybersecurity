## 6. Defend it in layers

No single defence stops everything. Switch defences on one at a time and rerun the suite after each: which test does each one fix, and which does it miss? Aim for 0 failures **and** T7 still answered.

```tool aisec
{"file": "ai-tara-support.json", "on": {"input": true, "strict": true, "clean": true, "approve": true}, "n": 0, "blank": ["on"]}
```

| Layer | Stops | Misses |
|---|---|---|
| Input filter | T1 (direct override) | role-play, encoding, anything in documents |
| Output filter (plain) | T2, T4 (the code written plainly) | T3 (spelled out) |
| Strict output filter | T3 too | tool misuse |
| Clean retrieved documents | T4, T6 (instructions inside documents) | direct attacks |
| Approval gate | T5, T6 (risky tools wait for a person) | leaks |

- [ ] 0 failures
- [ ] T7 still answered
- [ ] One line: why not just rely on the input filter?

> Hint: Attackers only need one gap. Layers mean each attack has to beat several different checks.

?> Which defence stops the spelled-out code (T3)? (one word from its name) :: strict
