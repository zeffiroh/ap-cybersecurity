# Coding problem, 1.2.a: Detect brute-force login attempts

**Skill:** Detect Attacks · **Maps to:** 1.2.A · **Language:** Python 3 (pytest)

## Problem
Build the detector a login-monitoring system would use. Given a list of authentication events,
return every username that has five or more failed login attempts within any 60-second window.

This is the core algorithm behind real intrusion-detection rules (e.g., fail2ban's default
policy). The defender's goal is to catch automated password-guessing tools before they succeed.

## Function contract
Implement `solve(events: list[dict]) -> list[str]` in `starter.py` (see `interface.md` /
`blackbox.yaml`). Return the sorted, de-duplicated list of usernames flagged as brute-force
targets.

## Input
A list of event dicts. Each dict has:
- `ts` (`int`), Unix timestamp in seconds of the login attempt
- `user` (`str`), the username targeted
- `ok` (`bool`), `True` if the login succeeded, `False` if it failed

Events may arrive in any order (do not assume sorted by timestamp).

## Output
A sorted `list[str]` of unique usernames that triggered the brute-force threshold: 5 or more
**failed** logins (where `ok == False`) within any 60-second window. A window is valid when
`max_ts - min_ts < 60` (strict less-than, so exactly 60 is NOT within the window). Successes
are ignored for counting purposes.

## Examples
```
events = [
    {"ts": 1000, "user": "alice", "ok": False},
    {"ts": 1010, "user": "alice", "ok": False},
    {"ts": 1020, "user": "alice", "ok": False},
    {"ts": 1030, "user": "alice", "ok": False},
    {"ts": 1040, "user": "alice", "ok": False},  # 5 failures in 40s -> flagged
    {"ts": 1000, "user": "bob",   "ok": False},
    {"ts": 1100, "user": "bob",   "ok": False},  # 2 failures, not enough -> not flagged
]
solve(events) -> ["alice"]
```

```
solve([]) -> []
```

```
# Four failures in window: below threshold
events = [{"ts": i*10, "user": "carol", "ok": False} for i in range(4)]
solve(events) -> []
```

## Constraints
- Deterministic, offline, standard library only.
- Events may be unsorted; your solution must handle any ordering.
- The 60-second window: at least 5 failures where `max_ts - min_ts < 60`.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
