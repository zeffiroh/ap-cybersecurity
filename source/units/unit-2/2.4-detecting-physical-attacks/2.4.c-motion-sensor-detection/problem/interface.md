# Interface, 2.4.c-motion-sensor-classifier (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(events: list[dict], false_positive_causes: set[str]) -> list[str]
```

## Input (`events`)
`list[dict]` where each dict represents one motion-sensor trigger event and has:
- `"id"`: `str`, unique event identifier string
- `"sensor_type"`: `str`, one of `"pir"`, `"microwave"`, `"ultrasonic"`, `"dual-tech"`
- For `sensor_type` in `{"pir", "microwave", "ultrasonic"}` (single-technology sensors):
  - `"cause"`: `str`, the tag describing what triggered the sensor (e.g. `"person"`,
    `"sunlight"`, `"hvac_airflow"`, `"pet"`, `"insect"`, `"vibration"`, `"foliage"`)
- For `sensor_type == "dual-tech"`:
  - `"cause_pir"`: `str`, the cause tag reported by the PIR element
  - `"cause_mw"`: `str`, the cause tag reported by the microwave element

## Input (`false_positive_causes`)
`set[str]`, the set of cause tags that are known false-positive causes (e.g.
`{"sunlight", "hvac_airflow", "pet", "insect", "vibration", "foliage"}`). Any cause tag NOT in
this set is treated as a genuine, person-consistent cause.

## Output (`result`)
A **sorted, de-duplicated** `list[str]` of event IDs that classify as **TRUE_DETECTION**. Events
that classify as FALSE_POSITIVE are simply omitted from the result. Empty list if none.

## Classification rules
- **Single-technology sensor** (`pir`, `microwave`, or `ultrasonic`): the event is a
  TRUE_DETECTION if and only if `"cause"` is NOT in `false_positive_causes`.
- **Dual-technology sensor** (`dual-tech`): AND-logic. The event is a TRUE_DETECTION if and only
  if BOTH `"cause_pir"` and `"cause_mw"` are NOT in `false_positive_causes`. If either element's
  cause is a known false-positive cause, the whole event is a FALSE_POSITIVE, even if the other
  element's cause is genuine.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Every event dict has a well-formed `"id"` and `"sensor_type"` plus the cause field(s) required
  for that sensor type, per the input spec above.
- Event IDs are unique within a single call.
- Output is always sorted ascending and de-duplicated.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
