# Coding problem, 2.1.a: CIA Triad Classifier

**Skill:** Analyze Risk · **Maps to:** 2.1.A · **Language:** Python 3 (pytest)

## Problem
In cybersecurity, classifying incidents according to the CIA triad helps organizations prioritize response and apply correct controls. You are tasked with implementing a rule-based classifier that scans incident descriptions for keywords indicating violations of **Confidentiality**, **Integrity**, or **Availability**.

Implement `solve(data)` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
A list of dictionaries containing `"id"` and `"description"` of the security incidents:
```python
[
    {"id": "INC-01", "description": "Attacker intercepted the unencrypted credentials."},
    {"id": "INC-02", "description": "A script corrupted the production database records."}
]
```

## Output
A dictionary mapping each incident ID to a sorted list of violated pillars:
```python
{
    "INC-01": ["Confidentiality"],
    "INC-02": ["Integrity"]
}
```

## Rules
A pillar is violated if the incident's description contains (case-insensitively) any of these keywords:
- **Confidentiality**: `leak`, `expose`, `disclose`, `intercept`, `steal`, `stole`, `read`, `password`, `credential`
- **Integrity**: `modify`, `alter`, `change`, `corrupt`, `tamper`, `edit`, `forge`, `spoof`
- **Availability**: `down`, `offline`, `unavailable`, `flood`, `crash`, `lock`, `ransomware`, `denial`

The output list of pillars for each incident ID must be sorted alphabetically.

## How to run
```bash
cd problem && python -m pytest tests.py -q
```
