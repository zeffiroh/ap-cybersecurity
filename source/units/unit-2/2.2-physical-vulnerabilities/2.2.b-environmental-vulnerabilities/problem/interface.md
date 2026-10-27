# Interface, 2.2.b-sensor-triage (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(data: list[dict]) -> dict[str, str]
```

## Input (`data`)
A list of dictionaries representing sensor readings. Each dictionary contains:
- `id` (str): Unique identifier for the reading.
- `room` (str): Room/zone identifier the sensor is located in.
- `type` (str): One of `"power"`, `"temperature"`, `"humidity"`, `"smoke"`, `"water"`.
- `value` (float/int): The sensor's numeric reading (see prompt.md for units per type).

## Output (`result`)
A dictionary where keys are the `id` of each reading from the input and values are the severity
string: `"NORMAL"`, `"WARNING"`, or `"CRITICAL"`.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network.
- Standard library only.
- Per-type thresholds (see prompt.md for full detail):
  1. `power`: outage (`0`) or `<90` or `>110` -> `CRITICAL`; `[90,95)` or `(105,110]` -> `WARNING`; else `NORMAL`.
  2. `temperature`: `>30` -> `CRITICAL`; `(27,30]` or `<15` -> `WARNING`; else `NORMAL`.
  3. `humidity`: `>70` or `<20` -> `CRITICAL`; `(60,70]` or `[20,40)` -> `WARNING`; else `NORMAL`.
  4. `smoke`/`water`: any positive value -> `CRITICAL`; `0` -> `NORMAL`.
  5. Combined-signal escalation: within the same `room`, if a `temperature` reading is
     `WARNING`/`CRITICAL` AND a `humidity` reading is `WARNING`/`CRITICAL`, escalate both of
     those two readings to `CRITICAL` (only temperature and humidity readings are affected).

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
