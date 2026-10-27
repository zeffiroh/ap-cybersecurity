# Coding problem, 5.2.c: Detect lateral movement in an authentication log

**Skill:** Mitigate Risk, Detect Attacks · **Maps to:** 5.2.B, 5.2.C · **Language:** Python 3 (pytest)

## Problem
Build the detector a security team's SIEM rule would run over authentication events. Given a list
of authentication events (account, destination host, timestamp in minutes), flag any account that
authenticated to **at least `threshold` distinct hosts** within any rolling **`window_minutes`**
window, a classic lateral-movement signal.

## Function contract
Implement `solve(events: list, threshold: int, window_minutes: int) -> list` in `starter.py`
(see `interface.md` / `blackbox.yaml`).

## Input
- `events`: `list[dict]`, each `{"account": str, "host": str, "ts": int}` (`ts` = minutes since
  start of log, non-negative integer, not necessarily sorted).
- `threshold`: `int`, minimum number of **distinct** hosts within the window to flag the account.
- `window_minutes`: `int`, size of the rolling time window, in minutes (inclusive on both ends).

## Output
A **sorted, de-duplicated** `list[str]` of account names that hit the threshold at any point.

## Examples
```
events = [
  {"account":"mkt_dana","host":"h1","ts":0},
  {"account":"mkt_dana","host":"h2","ts":2},
  {"account":"mkt_dana","host":"h3","ts":4},
  {"account":"svc_backup","host":"h9","ts":0},
]
solve(events, threshold=3, window_minutes=5) -> ["mkt_dana"]
```

```
events = [
  {"account":"alice","host":"h1","ts":0},
  {"account":"alice","host":"h2","ts":100},
]
solve(events, threshold=2, window_minutes=5) -> []   # too far apart for the window
```

## Constraints
- Deterministic, offline, standard library only.
- A window `[t, t + window_minutes]` counts an event if its `ts` falls within that inclusive range;
  consider every event's `ts` as a possible window start.
- Repeated authentications to the SAME host do not add distinct-host count.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
