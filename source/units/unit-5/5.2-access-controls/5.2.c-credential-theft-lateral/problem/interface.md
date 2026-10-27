# Interface, 5.2.c-lateral-movement-detector (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(events: list, threshold: int, window_minutes: int) -> list
```

## Input
- `events`: `list[dict]`, each `{"account": str, "host": str, "ts": int}`. Not necessarily sorted
  by `ts`. `ts` is minutes since the start of the log (non-negative int).
- `threshold`: `int`, minimum number of distinct hosts within a window to flag the account.
- `window_minutes`: `int`, inclusive window size in minutes.

## Output (`result`)
Sorted, de-duplicated `list[str]` of account names for which some window
`[start, start + window_minutes]` (with `start` equal to some event's `ts` for that account)
contains events touching `>= threshold` distinct hosts.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- The window bounds are inclusive: an event with `ts == start + window_minutes` counts.
- Repeated events to the same host within a window count once toward distinct-host count.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
