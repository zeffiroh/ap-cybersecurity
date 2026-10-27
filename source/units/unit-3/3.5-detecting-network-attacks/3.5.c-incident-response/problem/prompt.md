# Coding problem, 3.5.c: Incident response phase sorter

**Skill:** Detect Attacks, Collaborate · **Maps to:** 3.5.C · **Language:** Python 3 (pytest)

## Problem
The NIST SP 800-61 incident response lifecycle has six phases, in this canonical order:

```
1. Preparation
2. Identification
3. Containment
4. Eradication
5. Recovery
6. Lessons Learned
```

You will implement a function that takes a list of response-action records, each tagged with the
phase it belongs to, but given in shuffled order, and returns the actions sorted into correct
lifecycle order. Actions within the same phase keep their original relative order (a stable sort).

An **action record** is a dict with:
- `"action"`, string description of the action
- `"phase"`, string, one of the six canonical phase names exactly as spelled above

## Function contract
Implement `solve(actions)` in `starter.py` (see `interface.md` / `blackbox.yaml`).

- `actions`, list of action record dicts, in arbitrary order

Return a `list[str]` of the `"action"` text values, reordered so that all actions from an earlier
phase (per the canonical order above) come before all actions from a later phase. Within the same
phase, preserve the original input order (stable sort). If an action's `"phase"` value is not one
of the six canonical names, raise `ValueError`.

## Examples
```python
actions = [
    {"action": "Rebuild the server from a clean backup", "phase": "Recovery"},
    {"action": "Write the incident response plan", "phase": "Preparation"},
    {"action": "Isolate the infected host from the network", "phase": "Containment"},
    {"action": "Confirm the IDS alert is a real compromise", "phase": "Identification"},
]
solve(actions) == [
    "Write the incident response plan",
    "Confirm the IDS alert is a real compromise",
    "Isolate the infected host from the network",
    "Rebuild the server from a clean backup",
]
```

```python
actions = [
    {"action": "Bogus phase", "phase": "Investigation"},
]
solve(actions)  # raises ValueError
```

## Constraints
- Deterministic, offline, standard library only.
- Must pass all cases in `tests.py` (visible + hidden).
- Sort is stable within a phase.

## How to run
```
cd problem && python -m pytest tests.py -q
```
