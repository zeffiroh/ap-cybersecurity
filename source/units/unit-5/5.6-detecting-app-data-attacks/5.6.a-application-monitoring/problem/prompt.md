# Coding problem, 5.6.a: Brute-force detector (SIEM alert rule)

**Skill:** Detect Attacks · **Maps to:** 5.6.A · **Language:** Python 3 (pytest)

## Problem
Implement the SIEM alert rule described in the lesson: given a list of parsed application log
entries, return every IP address whose failed-login (`401`) count exceeds a threshold within a
rolling time window, a classic brute-force signal.

## Function contract
Implement `solve(entries: list, threshold: int, window_seconds: int) -> list` in `starter.py`
(see `interface.md` / `blackbox.yaml`).

## Input
- `entries`: `list[dict]`, each `{"ip": str, "ts": int, "status": int}` (`ts` = seconds since
  start of log, not necessarily sorted).
- `threshold`: `int`, minimum number of `401` events within the window to flag the IP.
- `window_seconds`: `int`, rolling window size, in seconds (inclusive on both ends).

## Output
A **sorted, de-duplicated** `list[str]` of flagged IP addresses.

## Examples
```
entries = [
  {"ip":"10.0.0.1","ts":0,"status":401},
  {"ip":"10.0.0.1","ts":10,"status":401},
  {"ip":"10.0.0.1","ts":20,"status":401},
]
solve(entries, threshold=3, window_seconds=60) -> ["10.0.0.1"]
```

```
entries = [{"ip":"10.0.0.2","ts":0,"status":200}]
solve(entries, threshold=1, window_seconds=60) -> []   # success responses never count
```

## Constraints
- Deterministic, offline, standard library only.
- Only `status == 401` entries count toward the brute-force count; other codes are ignored.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
