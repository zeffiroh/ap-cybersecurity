# Interface, 1.2.a-brute-force-detector (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(events: list[dict]) -> list[str]
```

## Input (`events`)
A `list[dict]`. Each dict is one authentication event with exactly these keys:
- `ts`   (`int`), Unix timestamp in whole seconds
- `user` (`str`), username targeted by the attempt
- `ok`   (`bool`), `True` = login succeeded, `False` = login failed

The list may be empty. Events may appear in any order (unsorted by timestamp).

## Output (`result`)
A **sorted, de-duplicated** `list[str]` of usernames that are flagged as brute-force targets.

## Detection rule (precise)
A username is flagged if and only if there exist at least 5 events for that user where:
1. `ok == False` (failed logins only; successes do NOT count toward the threshold)
2. `max(ts) - min(ts) < 60` across those 5 (or more) events (strict less-than; the window is
   open on the right, spans of exactly 60 seconds are NOT within the window)

Algorithm: for each username, collect all timestamps where `ok == False`, sort them, then use a
sliding window: for each position `i`, check if `ts[i+4] - ts[i] < 60`; if so, flag the user.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Output always sorted ascending and de-duplicated.
- Empty input returns `[]`.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
