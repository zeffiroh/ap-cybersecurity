# Interface, 1.1.a-tactic-detector (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(text: str) -> list[str]
```

## Input (`text`)
A single string: the message body and/or subject to analyze.

## Output (`result`)
A **sorted, de-duplicated** `list[str]` drawn from
`{"authority", "intimidation", "scarcity", "urgency"}`. Empty list if no tactic is present.

## Indicator phrase sets (case-insensitive substring match)
- **urgency:** `urgent`, `act now`, `immediately`, `right now`, `asap`, `expires`, `within 24 hours`,
  `24 hours`, `as soon as possible`, `don't delay`, `do not delay`
- **authority:** `it department`, `ceo`, `manager`, `administrator`, `irs`, `bank`, `police`,
  `official`, `help desk`, `human resources`, `hr department`
- **scarcity:** `limited`, `only`, `last chance`, `running out`, `few left`, `exclusive`,
  `while supplies last`, `act fast`
- **intimidation:** `legal action`, `account suspended`, `account will be locked`, `penalty`,
  `arrested`, `fired`, `terminated`, `lawsuit`, `consequences`, `reported`

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Matching is case-insensitive. Output always sorted ascending and de-duplicated.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
