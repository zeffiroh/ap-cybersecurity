# Interface, 2.4.b-alarm-event-classifier (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(events: list[dict], exit_delay_sec: int = 45, verify_window_sec: int = 120) -> list[str]
```

## Input (`events`)
`list[dict]` where each dict has:
- `"ts"`: `int`, Unix timestamp in seconds
- `"zone"`: `str`, zone/door identifier
- `"sensor"`: `str`, one of `"contact"`, `"glass_break"`, `"panic"`
- `"arm_state"`: `str`, one of `"DISARMED"`, `"ARMED_AWAY"`, `"ARMED_STAY"`
- `"since_armed_sec"`: `int`, seconds since the zone was armed when this event occurred (only
  meaningful when `arm_state != "DISARMED"` and `sensor != "panic"`)

## Input (other parameters)
- `exit_delay_sec`: `int`, default `45`, an armed contact/glass_break trip with
  `since_armed_sec < exit_delay_sec` is a false alarm.
- `verify_window_sec`: `int`, default `120`, max `ts` gap between two different-zone real trips
  for cross-zone verification.

## Output (`result`)
A `list[str]` the same length as `events`, in the **same order as the input**, where each element
is one of `"SUPPRESSED"`, `"FALSE_ALARM"`, `"LOCAL_ONLY"`, `"DISPATCH"`.

## Classification rules
1. **Panic override:** if `sensor == "panic"`, classification is always `"DISPATCH"`, regardless
   of `arm_state` or `since_armed_sec`.
2. **Suppressed:** else if `arm_state == "DISARMED"`, classification is `"SUPPRESSED"`.
3. **False alarm:** else if `since_armed_sec < exit_delay_sec`, classification is `"FALSE_ALARM"`.
4. **Real trip, verification:** otherwise the event is a "real trip" candidate. A real trip is
   promoted to `"DISPATCH"` if there exists at least one other real-trip event (per rules 1-4,
   excluding panic events) in a **different** `zone` with `abs(ts_i - ts_j) <= verify_window_sec`.
   Otherwise it is `"LOCAL_ONLY"`.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Output order matches input order exactly (do not sort by timestamp for output).
- Same-zone events never corroborate each other for cross-zone verification.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
