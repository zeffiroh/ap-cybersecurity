# Coding problem, 2.4.c: Motion-sensor event classifier

**Skill:** Detect Attacks · **Maps to:** 2.4.B, 2.4.C · **Language:** Python 3 (pytest)

## Problem
You are building the automated triage logic for a facility's motion-sensor monitoring system at
Crestfield Analytics. Given a list of motion-sensor trigger events, classify each one as a
**TRUE_DETECTION** (a real person likely caused it) or a **FALSE_POSITIVE** (a known nuisance
cause, sunlight, HVAC airflow, a pet, an insect, vibration, or foliage, likely caused it), and
return the IDs of the events that are true detections.

Single-technology sensors (`pir`, `microwave`, `ultrasonic`) report one cause tag. A
**dual-technology** sensor reports two independent cause tags, one from its PIR element, one
from its microwave element, and only counts as a true detection when **both** elements agree the
cause is genuine (AND-logic). This mirrors the lesson: a dual-tech sensor exists specifically to
suppress the false-positive causes that fool a single technology, so if *either* element's cause
is a known false-positive cause, the whole event is a false positive.

## Function contract
Implement `solve(events, false_positive_causes)` in `starter.py` (see `interface.md` /
`blackbox.yaml`).

## Input
- `events`: `list[dict]`, each dict has:
  - `"id"`: `str`, event identifier, e.g. `"EVT-001"`
  - `"sensor_type"`: `str`, `"pir"`, `"microwave"`, `"ultrasonic"`, or `"dual-tech"`
  - single-tech events also have `"cause"`: `str`
  - dual-tech events instead have `"cause_pir"`: `str` and `"cause_mw"`: `str`
- `false_positive_causes`: `set[str]`, known false-positive cause tags, e.g.
  `{"sunlight", "hvac_airflow", "pet", "insect", "vibration", "foliage"}`

## Output
A **sorted list of unique event ID strings** that classify as TRUE_DETECTION. Empty list if none.

## Examples
```python
events = [
    {"id": "EVT-001", "sensor_type": "pir", "cause": "person"},
    {"id": "EVT-002", "sensor_type": "pir", "cause": "sunlight"},
]
fp = {"sunlight", "hvac_airflow", "pet", "insect", "vibration", "foliage"}
solve(events, fp)  ->  ["EVT-001"]

events2 = [
    {"id": "EVT-010", "sensor_type": "dual-tech", "cause_pir": "person", "cause_mw": "person"},
    {"id": "EVT-011", "sensor_type": "dual-tech", "cause_pir": "hvac_airflow", "cause_mw": "person"},
]
solve(events2, fp)  ->  ["EVT-010"]
```

## Constraints
- Deterministic, offline, standard library only.
- Every event has the fields required for its `sensor_type` as described in `interface.md`.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
