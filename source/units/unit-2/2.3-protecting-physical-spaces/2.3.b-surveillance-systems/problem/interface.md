# Interface, 2.3.b-camera-event-log-detector (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(events: list[dict]) -> list[str]
```

## Input (`events`)
`list[dict]`, sorted ascending by `"ts"`, where each dict has:
- `"camera_id"`: `str`, camera identifier, e.g. `"CAM-01"`
- `"ts"`: `int`, Unix timestamp in seconds (UTC)
- `"motion"`: `bool`, whether the camera's motion sensor triggered
- `"person_detected"`: `bool`, whether analytics confirmed a person in frame
- `"area"`: `str`, the monitored area name, e.g. `"lobby"`, `"server_room"`
- `"authorized_hours"`: `tuple[int, int]`, `(start_hour, end_hour)` UTC hours during which a
  person detection at this camera is authorized; authorized iff `start <= hour < end`

## Output (`result`)
A **sorted, de-duplicated** `list[str]` of alert strings. Empty list if no alerts.

## Alert rules
- **AFTER_HOURS:\<camera_id\>**, flag if any event on that camera has `person_detected == True`
  and its timestamp's UTC hour (`(ts % 86400) // 3600`) falls outside `authorized_hours`.
- **GHOST_MOTION:\<camera_id\>**, flag if that camera has 3 or more consecutive events (in
  timestamp order) with `motion == True` and `person_detected == False`. Any event with
  `motion == False` or `person_detected == True` resets the streak to 0.
- **CROWD_SERVER_ROOM**, flag once (globally, not per-camera) if more than 2 events anywhere have
  `person_detected == True` and `area == "server_room"` within any 60-second sliding window.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Output always sorted ascending and de-duplicated (a `set` internally, then `sorted(...)`).
- Empty `events` input returns `[]`.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
