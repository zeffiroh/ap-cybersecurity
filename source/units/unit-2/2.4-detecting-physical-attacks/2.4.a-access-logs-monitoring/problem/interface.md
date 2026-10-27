# Interface, 2.4.a-access-log-detector (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(entries: list[dict], far_pairs: set[frozenset]) -> list[str]
```

## Input (`entries`)
`list[dict]` where each dict has:
- `"ts"`: `int`, Unix timestamp in seconds (UTC)
- `"badge"`: `str`, badge identifier string
- `"door"`: `str`, door/reader name string
- `"outcome"`: `str`, either `"GRANTED"` or `"DENIED"`

## Input (`far_pairs`)
`set[frozenset]`, each frozenset contains exactly two door name strings that are geographically
far apart (i.e., the same badge appearing at both within 600 seconds is a location inconsistency).

## Output (`result`)
A **sorted, de-duplicated** `list[str]` of badge IDs that triggered one or more alert rules.
Empty list if no alerts.

## Alert rules
- **Rule 0, Repeated denial burst:** count DENIED events per badge in any 60-second sliding
  window. Flag the badge if count >= 5.
- **Rule 1, After-hours restricted access:** flag a badge if it has any GRANTED entry at a door
  whose name starts with `"restricted-"` and whose timestamp UTC hour is in {22,23,0,1,2,3,4,5}.
- **Rule 2, Location inconsistency:** for each badge, scan GRANTED entries in timestamp order.
  If two consecutive GRANTED entries at different doors occur within 600 seconds AND that door pair
  is in `far_pairs`, flag the badge.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Entries may be given in any order; sort by `"ts"` internally as needed.
- Output always sorted ascending and de-duplicated.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
