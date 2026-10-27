# Coding problem, 2.4.a: Access log anomaly detector

**Skill:** Detect Attacks · **Maps to:** 2.4.A · **Language:** Python 3 (pytest)

## Problem
You are building the detection engine for a physical access control monitoring system at Crestfield Analytics. Given a list of timestamped access log entries, identify every badge ID that triggers at least one of three alert rules:

- **Rule 0, Repeated denial burst:** 5 or more ACCESS DENIED events for the same badge within any 60-second sliding window.
- **Rule 1, After-hours valid access to a restricted door:** any GRANTED entry at a door whose name starts with `"restricted-"` between 22:00 and 05:59 (inclusive, using the entry's local time).
- **Rule 2, Location inconsistency:** the same badge granted at two different doors within a gap of 10 minutes (600 seconds) where those two doors are listed as geographically separated in a provided `far_pairs` set of frozensets.

## Function contract
Implement `solve(entries, far_pairs)` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
- `entries`: `list[dict]`, each dict has:
  - `"ts"`: `int`, Unix timestamp (seconds)
  - `"badge"`: `str`, badge identifier e.g. `"B-0101"`
  - `"door"`: `str`, door identifier e.g. `"restricted-server-room-A"`
  - `"outcome"`: `str`, `"GRANTED"` or `"DENIED"`
- `far_pairs`: `set[frozenset]`, each element is a frozenset of two door names that are geographically far apart.

## Output
A **sorted list of unique badge ID strings** that triggered one or more rules. Empty list if no alerts.

## Examples
```python
entries = [
    {"ts": 1710230400, "badge": "B-0101", "door": "lobby", "outcome": "DENIED"},
    {"ts": 1710230410, "badge": "B-0101", "door": "lobby", "outcome": "DENIED"},
    {"ts": 1710230420, "badge": "B-0101", "door": "lobby", "outcome": "DENIED"},
    {"ts": 1710230430, "badge": "B-0101", "door": "lobby", "outcome": "DENIED"},
    {"ts": 1710230440, "badge": "B-0101", "door": "lobby", "outcome": "DENIED"},
]
far_pairs = set()
solve(entries, far_pairs)  ->  ["B-0101"]

entries2 = [
    {"ts": 1710288001, "badge": "B-0202", "door": "restricted-vault", "outcome": "GRANTED"},
]
# ts 1710288001 = 2024-03-13 02:00:01 UTC  (after-hours)
far_pairs2 = set()
solve(entries2, far_pairs2)  ->  ["B-0202"]
```

## Constraints
- Deterministic, offline, standard library only.
- Treat all timestamps as UTC when checking hour for after-hours (hour in {22,23,0,1,2,3,4,5}).
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
