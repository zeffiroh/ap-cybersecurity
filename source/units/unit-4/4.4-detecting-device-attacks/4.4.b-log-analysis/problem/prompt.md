# Coding problem, 4.4.b: Brute-force log correlator

**Skill:** Detect Attacks · **Maps to:** 4.4.B · **Language:** Python 3 (pytest)

## Problem
An authentication log records every login attempt as an event with a username, a timestamp (in
seconds), and a result (`"SUCCESS"` or `"FAILED"`). A brute-force attack shows up as a cluster of
failed attempts for the same user, tightly packed in time. Build the correlator that scans the
log and flags every username showing this pattern.

## Function contract
Implement `def solve(entries: list) -> list` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
A list of dicts, each with keys `ts` (int, seconds since some reference point), `user` (str),
`result` (str, `"SUCCESS"` or `"FAILED"`). Entries are not guaranteed to already be sorted by
timestamp.

## Output
A sorted list of usernames (str) flagged for a brute-force pattern.

## Detection rule
A user is flagged if there exist **5 or more `"FAILED"` entries for that user** where the time
span from the earliest to the latest of those 5 (or more) entries is **at most 60 seconds**
(inclusive). In other words: sort that user's failed-attempt timestamps ascending; if any 5
consecutive failed timestamps (in that sorted order) span 60 seconds or less
(`timestamps[i+4] - timestamps[i] <= 60`), the user is flagged. `SUCCESS` entries do not count
toward the failure count and do not reset or break a streak of failures, only `FAILED` entries
matter for this rule.

## Examples
```
[{"ts": 0, "user": "jsmith", "result": "FAILED"},
 {"ts": 13, "user": "jsmith", "result": "FAILED"},
 {"ts": 21, "user": "jsmith", "result": "FAILED"},
 {"ts": 30, "user": "jsmith", "result": "FAILED"},
 {"ts": 38, "user": "jsmith", "result": "FAILED"},
 {"ts": 46, "user": "jsmith", "result": "SUCCESS"},
 {"ts": 100, "user": "agarcia", "result": "FAILED"},
 {"ts": 1662, "user": "agarcia", "result": "FAILED"}]
    -> ["jsmith"]
```
*(jsmith has 5 failures spanning 0-38s = 38s <= 60s -> flagged. agarcia has only 2 failures,
1562s apart -> not flagged.)*

## Constraints
- Deterministic, offline, standard library only.
- Input entries may arrive out of timestamp order; sort within your implementation.
- Return a de-duplicated, alphabetically sorted list of usernames.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
