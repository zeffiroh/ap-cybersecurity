# Coding problem, 2.3.b: Camera event log anomaly detector

**Skill:** Detect Attacks · **Maps to:** 2.3.A · **Language:** Python 3 (pytest)

## Problem
You are building the alerting logic for the IP camera network at Crestfield Analytics. Each
camera emits a stream of motion/detection events. Given the full event log (already sorted
ascending by timestamp), identify every alert condition described below and return a sorted,
de-duplicated list of alert strings.

This mirrors the lesson's monitoring concepts: active monitoring depends on software correctly
surfacing anomalies (after-hours presence, a person lingering where they shouldn't, a "ghost
motion" pattern consistent with a camera fault or someone deliberately avoiding facial capture)
so a human operator or SIEM can act on them.

## Alert rules
- **AFTER_HOURS:\<camera_id\>**, a person was detected (`person_detected: True`) at a camera
  outside that event's `authorized_hours` window. `authorized_hours` is a `(start, end)` tuple of
  UTC hours; an hour `h` is authorized if `start <= h < end`. The hour of an event is derived from
  its Unix timestamp: `hour = (ts % 86400) // 3600`.
- **GHOST_MOTION:\<camera_id\>**, 3 or more **consecutive** events on the same camera (in
  timestamp order) where `motion` is `True` but `person_detected` is `False`. Any event that
  breaks the pattern (`motion` is `False`, or `person_detected` is `True`) resets the streak count
  to zero. "Ghost motion" describes a camera repeatedly reporting motion with nothing confirmed
  human, often a maintenance issue (foliage, a loose mount) or a deliberate attempt to trigger
  false fatigue in an operator.
- **CROWD_SERVER_ROOM**, more than 2 `person_detected: True` events occur in `area ==
  "server_room"` within any 60-second sliding window (across any cameras). This is a single global
  alert, not per-camera.

## Function contract
Implement `solve(events)` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
`events`: `list[dict]`, sorted ascending by `"ts"`, each dict has:
- `"camera_id"`: `str`
- `"ts"`: `int`, Unix timestamp (seconds, UTC)
- `"motion"`: `bool`
- `"person_detected"`: `bool`
- `"area"`: `str`
- `"authorized_hours"`: `tuple[int, int]`, `(start_hour, end_hour)`, both in `0..24`

## Output
A **sorted, de-duplicated** `list[str]` of alert strings, e.g. `"AFTER_HOURS:CAM-01"`,
`"GHOST_MOTION:CAM-02"`, `"CROWD_SERVER_ROOM"`. Empty list if no alerts.

## Examples
```python
events = [
    {"camera_id": "CAM-01", "ts": 1700000000, "motion": True, "person_detected": True,
     "area": "lobby", "authorized_hours": (8, 18)},   # hour 22 -> outside (8,18)
]
solve(events)  ->  ["AFTER_HOURS:CAM-01"]

events2 = [
    {"camera_id": "CAM-02", "ts": 1700035200, "motion": True, "person_detected": False,
     "area": "hallway", "authorized_hours": (8, 18)},
    {"camera_id": "CAM-02", "ts": 1700035260, "motion": True, "person_detected": False,
     "area": "hallway", "authorized_hours": (8, 18)},
    {"camera_id": "CAM-02", "ts": 1700035320, "motion": True, "person_detected": False,
     "area": "hallway", "authorized_hours": (8, 18)},
]
solve(events2)  ->  ["GHOST_MOTION:CAM-02"]
```

## Constraints
- Deterministic, offline, standard library only.
- Timestamps within one camera's stream may be assumed to arrive in ascending order in the input;
  do not assume any ordering relationship *between* different cameras.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
