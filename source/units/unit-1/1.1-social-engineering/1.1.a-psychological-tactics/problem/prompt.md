# Coding problem, 1.1.a: Detect psychological pressure tactics

**Skill:** Analyze Risk · **Maps to:** 1.1.A, 1.1.B · **Language:** Python 3 (pytest)

## Problem
Build the detector a phishing-awareness tool would use. Given the raw text of a message, return
which of the four psychological pressure tactics it employs:

- `"urgency"`, manufactured time pressure
- `"authority"`, borrowed legitimacy (boss, IT, government, bank)
- `"scarcity"`, limited availability / fear of missing out
- `"intimidation"`, threats / fear

A message may use zero, one, or several tactics.

## Function contract
Implement `solve(text: str) -> list[str]` in `starter.py` (see `interface.md` / `blackbox.yaml`).
Return the detected tactic labels as a **sorted, de-duplicated** list. Matching is
case-insensitive. Detection is by the indicator phrase sets defined in `interface.md`.

## Input
A single string, the message body (and/or subject) to analyze.

## Output
A sorted list of unique tactic labels from the set above (empty list if none).

## Examples
```
"Your account will be locked in 24 hours. Act now."        -> ["urgency"]
"This is the IT department. Limited spots — last chance."  -> ["authority", "scarcity"]
"Pay the penalty or we will take legal action immediately" -> ["intimidation", "urgency"]
"Lunch is in the kitchen, help yourself."                  -> []
```

## Constraints
- Deterministic, offline, standard library only.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
