# Interface, 5.6.a-brute-force-detector (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(entries: list, threshold: int, window_seconds: int) -> list
```

## Input
- `entries`: `list[dict]`, each `{"ip": str, "ts": int, "status": int}`. `ts` is seconds since
  the start of the log (non-negative int, not necessarily sorted). `status` is an HTTP status
  code; only `401` entries count toward brute-force detection.
- `threshold`: `int`, minimum number of 401 events within the window to flag the IP.
- `window_seconds`: `int`, inclusive rolling window size, in seconds.

## Output (`result`)
Sorted, de-duplicated `list[str]` of IP addresses for which some window
`[start, start + window_seconds]` (with `start` equal to one of that IP's 401 timestamps)
contains `>= threshold` 401 events.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Only entries with `status == 401` count; other status codes are ignored for detection.
- The window bounds are inclusive: an event with `ts == start + window_seconds` counts.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
