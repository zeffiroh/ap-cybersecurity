# Coding problem, 2.3.d: Facility control-compliance checker

**Skill:** Mitigate Risk · **Maps to:** 2.3.C · **Language:** Python 3 (pytest)

## Problem
You are auditing environmental controls across a facility's zones (rooms) for Crestfield
Analytics. Each zone has a room type and a set of installed controls (UPS presence, HVAC
redundancy level, fire suppression type, and floor-level leak sensor presence). The facility's
control policy specifies, per room type, the minimum controls required. Given a list of zones
and the policy, identify every zone that is **non-compliant**, missing one or more controls
required for its room type.

This mirrors real facility audits: a server room without a UPS or with water-sprinkler
suppression is a serious finding, while a general office is held to a much lighter standard.

## Function contract
Implement `solve(zones, policy)` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
- `zones`: `list[dict]`, each dict has:
  - `"name"`: `str`, zone identifier, e.g. `"server-room-a"`
  - `"room_type"`: `str`, key into `policy`, e.g. `"server"`, `"closet"`, `"office"`
  - `"has_ups"`: `bool`
  - `"hvac_redundancy"`: `int`, number of *extra* HVAC units beyond the minimum needed (0 means no redundancy, a single unit)
  - `"suppression"`: `str`, one of `"water"`, `"clean_agent"`, `"none"`
  - `"has_leak_sensor"`: `bool`
- `policy`: `dict[str, dict]`, maps a `room_type` string to a requirements dict, which may
  contain any subset of these keys (a missing key means that control is not required for that
  room type):
  - `"require_ups"`: `bool`, if `True`, zone must have `has_ups == True`
  - `"min_hvac_redundancy"`: `int`, zone's `hvac_redundancy` must be `>=` this value
  - `"allowed_suppression"`: `list[str]`, zone's `suppression` must be in this list
  - `"require_leak_sensor"`: `bool`, if `True`, zone must have `has_leak_sensor == True`
  - A zone whose `room_type` is not a key in `policy` has **no requirements** and is always compliant.

## Output
A **sorted list of unique zone name strings** that fail at least one applicable requirement.
Empty list if every zone is compliant.

## Examples
```python
policy = {
    "server": {
        "require_ups": True,
        "min_hvac_redundancy": 1,
        "allowed_suppression": ["clean_agent"],
        "require_leak_sensor": True,
    },
    "office": {
        "allowed_suppression": ["water", "clean_agent"],
    },
}

zones = [
    {"name": "server-room-a", "room_type": "server", "has_ups": True,
     "hvac_redundancy": 1, "suppression": "clean_agent", "has_leak_sensor": True},
    {"name": "server-room-b", "room_type": "server", "has_ups": False,
     "hvac_redundancy": 1, "suppression": "clean_agent", "has_leak_sensor": True},
    {"name": "office-1", "room_type": "office", "has_ups": False,
     "hvac_redundancy": 0, "suppression": "water", "has_leak_sensor": False},
]

solve(zones, policy)  ->  ["server-room-b"]
# server-room-a meets every requirement for "server".
# server-room-b fails require_ups (has_ups is False).
# office-1 has no UPS/HVAC/leak-sensor requirements for "office", and water is an allowed
#   suppression type for office, so it is compliant.
```

## Constraints
- Deterministic, offline, standard library only.
- A room type not present in `policy` has no requirements (always compliant).
- A zone is non-compliant if it fails ANY applicable requirement key present in its room type's
  policy entry.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
