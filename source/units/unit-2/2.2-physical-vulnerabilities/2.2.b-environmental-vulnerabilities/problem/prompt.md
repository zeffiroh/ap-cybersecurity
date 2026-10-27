# Coding problem, 2.2.b: Environmental sensor triage

**Skill:** Analyze Risk · **Maps to:** 2.2.A · **Language:** Python 3 (pytest)

## Problem
A data center streams readings from environmental sensors placed around each server room:
power (voltage as a percent of nominal), temperature (Celsius), humidity (percent relative
humidity), smoke detectors, and water/flood detectors. Facilities staff need every reading
automatically triaged into a severity level so a human only has to look at what matters.

Your task is to write a function `solve(data)` that takes a list of sensor readings and returns
a dictionary mapping each reading's `id` to a severity string: `"NORMAL"`, `"WARNING"`, or
`"CRITICAL"`.

### Per-reading thresholds (by `type`)

**`power`** (`value` = supply voltage as a percent of nominal, 100 = nominal):
- `CRITICAL` if `value == 0` (total outage) or `value < 90` or `value > 110`
- `WARNING` if `90 <= value < 95` or `105 < value <= 110`
- `NORMAL` otherwise (`95 <= value <= 105`)

**`temperature`** (`value` = degrees Celsius):
- `CRITICAL` if `value > 30`
- `WARNING` if `27 < value <= 30` or `value < 15`
- `NORMAL` otherwise (`15 <= value <= 27`)

**`humidity`** (`value` = percent relative humidity):
- `CRITICAL` if `value > 70` or `value < 20`
- `WARNING` if `60 < value <= 70` or `20 <= value < 40`
- `NORMAL` otherwise (`40 <= value <= 60`)

**`smoke`** (`value` = detector reading, `0` = clear, any positive value = smoke detected):
- `CRITICAL` if `value > 0`
- `NORMAL` otherwise

**`water`** (`value` = detector reading, `0` = dry, any positive value = moisture detected):
- `CRITICAL` if `value > 0`
- `NORMAL` otherwise

### Combined-signal escalation (cooling-failure pattern)
After computing each reading's per-reading severity above, apply one escalation rule: for
readings that share the same `room`, if there is **both** a `temperature` reading rated
`WARNING` or `CRITICAL` **and** a `humidity` reading rated `WARNING` or `CRITICAL` in that same
room, escalate *both* of those specific readings (temperature and humidity only) to
`CRITICAL`. This models a failing HVAC unit, where rising temperature and drifting humidity
together are a stronger signal than either alone. Other reading types in the room (power, smoke,
water) are not affected by this rule, and a room where only one of the two (temperature or
humidity) is elevated is not escalated.

## Function contract
Implement `solve(data: list[dict]) -> dict[str, str]` in `starter.py`.

## Input
A list of dictionaries, each representing one sensor reading:
```python
[
    {"id": "s1", "room": "server-room-a", "type": "temperature", "value": 29},
    {"id": "s2", "room": "server-room-a", "type": "humidity", "value": 65},
    {"id": "s3", "room": "server-room-b", "type": "power", "value": 100},
]
```

## Output
A dictionary mapping each reading's `"id"` to its severity string:
```python
{
    "s1": "CRITICAL",   # escalated: room also had a humidity WARNING/CRITICAL
    "s2": "CRITICAL",   # escalated: room also had a temperature WARNING/CRITICAL
    "s3": "NORMAL",
}
```

## Constraints
- `type` is one of `"power"`, `"temperature"`, `"humidity"`, `"smoke"`, `"water"`.
- `value` is a non-negative number (float or int) except `power`, which may be `0` (outage).
- Pure function, deterministic, standard library only.

## How to run
```bash
cd problem && python -m pytest tests.py -q
```
