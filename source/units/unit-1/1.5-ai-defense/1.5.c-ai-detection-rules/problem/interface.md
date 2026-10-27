# Interface, 1.5.c-detection-rule-generator (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(logs: list[dict]) -> list[str]
```

## Input (`logs`)
A list of log-event dicts. Each dict has exactly these keys:

| Key    | Type | Description                                   |
|--------|------|-----------------------------------------------|
| `ts`   | int  | Unix timestamp (seconds, non-negative integer) |
| `src`  | str  | Source IP address string (e.g. `"10.0.0.1"`)  |
| `event`| str  | Event type string; `"login_fail"` is the only type that counts toward the brute-force rule |
| `ok`   | bool | `True` = success, `False` = failure (redundant with event, included for completeness) |

Example single entry:
```python
{"ts": 1000, "src": "10.0.0.5", "event": "login_fail", "ok": False}
```

## Output (`result`)
A **sorted** `list[str]` of detection-rule strings. One rule string is emitted per source IP
that triggers the brute-force condition. The exact rule string format is:

```
ALERT brute_force src=<IP> count=<N> window=60s
```

Where:
- `<IP>` is the source IP string exactly as it appears in the log entries.
- `<N>` is the integer count of `login_fail` events from that IP within any contiguous 60-second
  window (the maximum count observed across all possible 60-second windows for that IP).
- `window=60s` is the literal string (fixed).

The list is sorted lexicographically (Python default `str` sort on the full rule string).

## Brute-force detection rule
An IP triggers the rule when it produces **5 or more** `login_fail` events where all events fall
within a 60-second window (i.e., `max_ts - min_ts <= 59` for some subset of size >= 5 from that
IP's `login_fail` events).

Detection algorithm (reference implementation uses this):
1. Group all `login_fail` events by `src`.
2. For each source, sort events by `ts`.
3. Use a sliding window: for each event at index `i`, count how many subsequent events have
   `ts <= events[i].ts + 59` (inclusive). The window size is the length of that group.
4. If the maximum window size for that source is >= 5, emit the rule with `count=` set to that
   maximum window size.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network.
- Standard library only.
- `logs` is a list (may be empty); entries are dicts with the schema above.
- `ts` values are non-negative integers; multiple events can share the same `ts`.
- Other event types (e.g. `"login_ok"`, `"logout"`) are ignored.
- Output is always sorted ascending (lexicographic) and de-duplicated (at most one rule per IP).

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
