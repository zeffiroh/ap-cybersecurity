# Interface, 5.1.d-breach-severity-scorer (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(report: dict) -> dict
```

## Input (`report`)
`{"categories": list[str], "record_count": int, "days_to_detect": int}`

- `categories`: zero or more of `{"pii", "financial", "health", "auth_plaintext", "auth_hashed",
  "email", "public"}`. Unknown strings are ignored (contribute 0 points).
- `record_count`: non-negative int.
- `days_to_detect`: non-negative int.

## Output (`result`)
`{"score": int, "label": str}` where `label` is one of `"low"`, `"medium"`, `"high"`, `"critical"`.

## Rubric
- Category points (sum, each category counted once): pii=40, financial=40, health=40,
  auth_plaintext=40, auth_hashed=15, email=10, public=0, unknown=0.
- Scale points: `<100`->0, `100-9999`->10, `10000-999999`->20, `>=1000000`->30.
- Detection points: `<=1`->0, `2-30`->10, `>30`->20.
- Label thresholds on total score: `>=80`->critical, `>=50`->high, `>=20`->medium, else low.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Categories with duplicates in the input list are only counted once.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
