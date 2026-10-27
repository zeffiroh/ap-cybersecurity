# Coding problem, 5.1.d: Score data breach severity

**Skill:** Analyze Risk · **Maps to:** 5.1.C · **Language:** Python 3 (pytest)

## Problem
Build the severity scorer a security team's intake triage tool would run on each incoming breach
report. Given the categories of data exposed, the number of records affected, and how many days
it took to detect the breach, compute a total severity score and a label.

## Scoring rubric
Start at `score = 0`.

**Data category points** (sum over all categories present in the report, each counted once):
- `"pii"` (personally identifiable information): +40
- `"financial"`: +40
- `"health"`: +40
- `"auth_plaintext"` (plaintext passwords/secrets): +40
- `"auth_hashed"` (hashed/salted passwords): +15
- `"email"`: +10
- `"public"`: +0

**Scale points** (based on `record_count`):
- `< 100`: +0
- `100`-`9,999`: +10
- `10,000`-`999,999`: +20
- `>= 1,000,000`: +30

**Detection-speed points** (based on `days_to_detect`):
- `<= 1`: +0
- `2`-`30`: +10
- `> 30`: +20

## Label thresholds (applied to the total score)
- `score >= 80` -> `"critical"`
- `score >= 50` -> `"high"`
- `score >= 20` -> `"medium"`
- else -> `"low"`

## Function contract
Implement `solve(report: dict) -> dict` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
`report`: `{"categories": list[str], "record_count": int, "days_to_detect": int}`

## Output
`{"score": int, "label": str}`

## Examples
```
{"categories": ["public"], "record_count": 50, "days_to_detect": 1}
    -> {"score": 0, "label": "low"}

{"categories": ["pii", "auth_plaintext"], "record_count": 500000, "days_to_detect": 45}
    -> {"score": 40 + 40 + 20 + 20, "label": "critical"}   # = 120

{"categories": ["email"], "record_count": 200, "days_to_detect": 5}
    -> {"score": 10 + 10 + 10, "label": "medium"}          # = 30
```

## Constraints
- Deterministic, offline, standard library only.
- Multiple categories are additive; unknown category strings contribute 0 points.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
