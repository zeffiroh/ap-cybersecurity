# Interface, 4.4.b-bruteforce-log-correlator (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(entries: list) -> list
```

## Input (`entries`)
A list of dicts, each an authentication log event:

| key | type | meaning |
|---|---|---|
| `ts` | int | timestamp in seconds (not guaranteed sorted across the list) |
| `user` | str | username the attempt was made against |
| `result` | str | `"SUCCESS"` or `"FAILED"` |

## Output (`result`)
A de-duplicated, alphabetically sorted list of `str` usernames flagged for a brute-force pattern.

## Detection rule
For each user, collect all `FAILED` timestamps and sort them ascending. The user is flagged if
any 5 consecutive timestamps in that sorted list (`t[i]` through `t[i+4]`) satisfy
`t[i+4] - t[i] <= 60`. A user needs at least 5 total failed attempts to be eligible; `SUCCESS`
entries are ignored entirely for this rule (they do not reset or interrupt a failure streak).

## Guarantees / rules
- Pure function, deterministic, no I/O, no network.
- Standard library only unless `blackbox.yaml: allow_deps` lists otherwise.
- Input order is not guaranteed; sort per-user failed timestamps before evaluating the rule.
- The 60-second window is inclusive (`<= 60`, not `< 60`).

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
