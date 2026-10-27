# Interface, 2.2.a-access-log-analyzer (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(records: list[dict]) -> list[str]
```

## Input (`records`)
A list of dicts in chronological order, each with:
- `"id"` (str): unique event ID, e.g. `"E001"`
- `"time"` (int): Unix timestamp in whole seconds
- `"badge"` (str | None): badge ID swiped, or None if no swipe
- `"door"` (str): door identifier
- `"distance_from_prev"` (int | None): distance in meters from where this badge was last seen,
  or None if badge is None or first appearance
- `"sensor_count"` (int): number of bodies detected crossing the threshold (normally 1)

## Output (`result`)
A **sorted, de-duplicated** `list[str]` of flagged event IDs. Empty list if none.

## Detection rules
- **Rule 1, Impossible speed:** A record is flagged if `badge` is not None,
  `distance_from_prev` is not None, and
  `distance_from_prev / (time - prev_time_for_this_badge) > MAX_WALK_SPEED`.
  `MAX_WALK_SPEED = 2.0` (meters per second).
  Division by zero (same timestamp): always flag.
- **Rule 2, Sensor mismatch:** A record is flagged if `sensor_count >= 2` and
  `badge` is not None (a door with no swipe at all is a separate alarm; not in scope).

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Records are always in ascending time order.
- Output is sorted ascending and de-duplicated (an event matching both rules appears once).

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
