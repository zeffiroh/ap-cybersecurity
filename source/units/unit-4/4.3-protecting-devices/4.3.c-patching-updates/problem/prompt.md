# Coding problem, 4.3.c: Patch-prioritization engine

**Skill:** Mitigate Risk · **Maps to:** 4.3.B, 4.3.C · **Language:** Python 3 (pytest)

## Problem
A patch-management team needs to triage a queue of pending vulnerabilities and decide how
urgently each must be addressed. Each vulnerability has a CVSS severity score, a flag for
whether it is being actively exploited in the wild, a flag for whether the affected asset is
internet-facing, and a flag for whether the affected software is end-of-life (no patch will ever
be released). Build the triage engine that assigns one urgency label to each vulnerability.

## Function contract
Implement `def solve(vulns: list) -> list` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
A list of dicts, each with keys: `id` (str), `cvss` (float, 0.0-10.0), `exploited_in_wild`
(bool), `internet_facing` (bool), `end_of_life` (bool).

## Output
A list of dicts, one per input vulnerability (same order as input), each with keys `id` (str,
copied from input) and `urgency` (str), where `urgency` is one of: `"emergency"`,
`"scheduled"`, `"routine"`, `"compensate"`.

## Decision rule (apply in this exact order, first match wins, per vulnerability)
1. `end_of_life` is `True` → `"compensate"` (no patch will ever exist; patching is not an
   option regardless of severity or exploitation status).
2. Else, `exploited_in_wild` is `True` AND `internet_facing` is `True` → `"emergency"`.
3. Else, `cvss >= 9.0` AND `internet_facing` is `True` → `"emergency"` (a working exploit is
   likely imminent for a critical, internet-facing flaw even without confirmed in-the-wild
   activity).
4. Else, `cvss >= 9.0` → `"scheduled"` (critical severity but not internet-facing).
5. Else, `cvss >= 7.0` AND `internet_facing` is `True` → `"scheduled"`.
6. Else → `"routine"`.

Rule order matters: `end_of_life` is checked first and overrides every other condition, an
end-of-life system is never `"emergency"` or `"scheduled"` even at CVSS 10.0, because patching is
not a valid remediation at all.

## Examples
```
[{"id": "V1", "cvss": 9.1, "exploited_in_wild": True, "internet_facing": True, "end_of_life": False}]
    -> [{"id": "V1", "urgency": "emergency"}]

[{"id": "V2", "cvss": 8.8, "exploited_in_wild": False, "internet_facing": False, "end_of_life": True}]
    -> [{"id": "V2", "urgency": "compensate"}]

[{"id": "V3", "cvss": 4.2, "exploited_in_wild": False, "internet_facing": False, "end_of_life": False}]
    -> [{"id": "V3", "urgency": "routine"}]
```

## Constraints
- Deterministic, offline, standard library only.
- Preserve input order in the output list.
- Exactly one urgency label per vulnerability.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
