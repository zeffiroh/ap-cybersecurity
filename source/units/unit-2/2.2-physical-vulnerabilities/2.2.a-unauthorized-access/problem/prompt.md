# Coding problem, 2.2.a: Detect unauthorized physical access in a badge log

**Skill:** Analyze Risk · **Maps to:** 2.2.A, 2.2.B · **Language:** Python 3 (pytest)

## Problem
A building security system writes one log record per door event. Your job is to implement the
analyst's first-pass filter: given a list of log records, return the event IDs of all records
that indicate a likely unauthorized physical access attempt, based on two detection rules:

**Rule 1, Impossible speed (tailgating / badge pass-back indicator).**
If the same badge ID appears at two different doors and the time between events is less than
the minimum walk time (distance_meters / MAX_WALK_SPEED), the second event is suspicious.
`MAX_WALK_SPEED = 2.0` meters per second.

**Rule 2, Sensor mismatch (tailgating indicator).**
If an event has `"sensor_count": 2` (or higher) but only one badge swipe was recorded (i.e.,
the event itself has `"badge": <a badge id>` and no second badge event at the same door within
1 second), that event is suspicious.

Return the list of flagged event IDs (strings), sorted ascending. An event may match both rules
but should appear only once.

## Function contract
Implement `solve(records: list[dict]) -> list[str]` in `starter.py`
(see `interface.md` / `blackbox.yaml`).

## Input
`records`, a list of dicts, each with keys:
- `"id"` (str): unique event identifier, e.g. `"E001"`
- `"time"` (int): Unix timestamp in seconds (integer)
- `"badge"` (str | None): badge ID that was swiped, or `None` if no swipe
- `"door"` (str): door identifier, e.g. `"D1"`
- `"distance_from_prev"` (int | None): meters from the previous door this badge was seen at,
  or `None` if this is the badge's first appearance or badge is None
- `"sensor_count"` (int): number of bodies the door sensor detected crossing (1 = normal)

Records are provided in chronological order (ascending `"time"`).

## Output
A sorted `list[str]` of flagged event IDs. Empty list if no violations found.

## Examples
```
[
  {"id":"E001","time":1000,"badge":"B-204","door":"D1","distance_from_prev":None,"sensor_count":1},
  {"id":"E002","time":1003,"badge":"B-204","door":"D2","distance_from_prev":50,"sensor_count":1},
  {"id":"E003","time":2000,"badge":"B-117","door":"D1","distance_from_prev":None,"sensor_count":2},
]
-> ["E002", "E003"]

E002: B-204 covers 50 m in 3 s = 16.7 m/s > 2.0 m/s  (Rule 1)
E003: sensor_count=2 with one swipe                    (Rule 2)
```

## Constraints
- Deterministic, offline, standard library only.
- MAX_WALK_SPEED = 2.0 m/s (defined in interface.md).
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
