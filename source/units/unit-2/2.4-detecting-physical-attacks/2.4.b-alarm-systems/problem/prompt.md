# Coding problem, 2.4.b: Alarm event classifier

**Skill:** Detect Attacks · **Maps to:** 2.4.B · **Language:** Python 3 (pytest)

## Problem
You are building the triage logic for an alarm control panel at Crestfield Analytics. Given a
timestamp-ordered stream of sensor events (one per zone trip), classify each event using the
arm-state, exit-delay, and cross-zone verification rules taught in the lesson:

- **SUPPRESSED**, the system was `"DISARMED"` when the event occurred (does not apply to panic
  buttons, see below).
- **FALSE_ALARM**, the event's sensor is `"contact"` or `"glass_break"`, the system was armed,
  and the event happened less than `exit_delay_sec` seconds after the zone was armed (still inside
  the exit-delay grace period).
- **LOCAL_ONLY**, a real trip (armed, past the exit delay) that has no corroborating trip in a
  *different* zone within `verify_window_sec` seconds. Only the local siren sounds.
- **DISPATCH**, either (a) the sensor is `"panic"` (a panic/duress button always dispatches,
  regardless of arm state or timing), or (b) a real trip that has a corroborating real trip in a
  different zone within `verify_window_sec` seconds (cross-zone verification).

## Function contract
Implement `solve(events, exit_delay_sec=45, verify_window_sec=120)` in `starter.py` (see
`interface.md` / `blackbox.yaml`).

## Input
- `events`: `list[dict]`, each with:
  - `"ts"`: `int`, Unix timestamp (seconds) the event occurred
  - `"zone"`: `str`, zone/door identifier, e.g. `"front-door"`
  - `"sensor"`: `str`, one of `"contact"`, `"glass_break"`, `"panic"`
  - `"arm_state"`: `str`, one of `"DISARMED"`, `"ARMED_AWAY"`, `"ARMED_STAY"`
  - `"since_armed_sec"`: `int`, seconds elapsed between arming and this event (ignored for
    `"panic"` and when `arm_state == "DISARMED"`)
- `exit_delay_sec`: `int`, default `45`, grace period after arming.
- `verify_window_sec`: `int`, default `120`, max gap (in `ts`) between two different-zone real
  trips for cross-zone verification to apply.

## Output
A `list[str]` of classifications, **one per input event, in the same order as the input**. Each
entry is one of `"SUPPRESSED"`, `"FALSE_ALARM"`, `"LOCAL_ONLY"`, `"DISPATCH"`.

## Examples
```python
events = [
    {"ts": 1000, "zone": "front-door", "sensor": "contact",
     "arm_state": "ARMED_AWAY", "since_armed_sec": 10},
]
solve(events)  ->  ["FALSE_ALARM"]

events2 = [
    {"ts": 1000, "zone": "z1", "sensor": "panic",
     "arm_state": "DISARMED", "since_armed_sec": 0},
]
solve(events2)  ->  ["DISPATCH"]

events3 = [
    {"ts": 1000, "zone": "z1", "sensor": "contact",
     "arm_state": "ARMED_AWAY", "since_armed_sec": 300},
    {"ts": 1050, "zone": "z2", "sensor": "glass_break",
     "arm_state": "ARMED_AWAY", "since_armed_sec": 305},
]
solve(events3)  ->  ["DISPATCH", "DISPATCH"]
```

## Constraints
- Deterministic, offline, standard library only.
- Events may be given in any timestamp order in the list; the output order must match the
  **input** order (do not re-sort the output).
- Cross-zone verification: two real trips (armed, past exit delay) in **different** zones with
  `abs(ts_a - ts_b) <= verify_window_sec` corroborate each other. A real trip may be corroborated
  by more than one other zone; any single qualifying pair is enough to promote it to `DISPATCH`.
  Same-zone repeats never corroborate each other.
- `since_armed_sec >= exit_delay_sec` counts as past the exit delay (boundary is inclusive on the
  "past delay" side, i.e. exactly `exit_delay_sec` is a real trip, not a false alarm).
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
