# Coding problem, 1.5.c: Generate detection rules from a login log

**Skill:** Detect Attacks · **Maps to:** 1.5.A · **Language:** Python 3 (pytest)

## Problem
A SOC receives a stream of authentication log events. Your task is to implement a
brute-force detection engine: scan the log for source IPs that generate 5 or more
`login_fail` events within any 60-second window, and emit a structured detection-rule
string for each flagged IP.

This mirrors how an AI-assisted SIEM generates candidate detection rules from raw log data.

## Function contract
Implement `solve(logs: list[dict]) -> list[str]` in `starter.py`
(see `interface.md` / `blackbox.yaml`).

## Input
`logs`, a list of dicts, each with:
- `ts` (int): Unix timestamp in seconds
- `src` (str): source IP address
- `event` (str): event type; only `"login_fail"` counts toward brute-force detection
- `ok` (bool): True = success, False = failure

## Output
A **sorted** list of detection-rule strings. Format for each triggered IP:

```
ALERT brute_force src=<IP> count=<N> window=60s
```

where `<N>` is the maximum number of `login_fail` events from that IP found within any
contiguous 60-second window (i.e., events where `max_ts - min_ts <= 59`).
Rules are sorted lexicographically. At most one rule per IP.

## Examples
```python
logs = [
    {"ts": 0,  "src": "1.2.3.4", "event": "login_fail", "ok": False},
    {"ts": 10, "src": "1.2.3.4", "event": "login_fail", "ok": False},
    {"ts": 20, "src": "1.2.3.4", "event": "login_fail", "ok": False},
    {"ts": 30, "src": "1.2.3.4", "event": "login_fail", "ok": False},
    {"ts": 40, "src": "1.2.3.4", "event": "login_fail", "ok": False},
]
solve(logs) -> ["ALERT brute_force src=1.2.3.4 count=5 window=60s"]

logs = [
    {"ts": 0,  "src": "9.9.9.9", "event": "login_fail", "ok": False},
    {"ts": 10, "src": "9.9.9.9", "event": "login_fail", "ok": False},
]
solve(logs) -> []   # only 2 failures — below threshold

solve([]) -> []     # empty log
```

## Algorithm (sliding window)
1. Collect all `login_fail` events and group by `src`.
2. Sort each group by `ts`.
3. For each group, slide a window: for each event at position `i`, count how many
   events starting at `i` have `ts <= events[i].ts + 59`.
4. If the maximum window count for any source is >= 5, emit its rule string.
5. Return the list sorted lexicographically.

## Constraints
- Deterministic, offline, standard library only.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
