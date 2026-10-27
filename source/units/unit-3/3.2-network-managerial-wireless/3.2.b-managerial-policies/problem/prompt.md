# Coding problem, 3.2.b: Control-type classifier

**Skill:** Mitigate Risk · **Maps to:** 3.2.A, 3.2.B · **Language:** Python 3 (pytest)

## Problem
You are building a control matrix tool for Crestfield Analytics' security program. Given a list of
implemented security scenarios, classify each one by control family: `"managerial"`,
`"technical"`, or `"physical"`, based on how the control is actually implemented (its
`"mechanism"`), not on what risk it happens to address.

## Function contract
Implement `classify_controls(scenarios)` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
- `scenarios`: `list[dict]`, each with:
  - `"id"`: `str`, a scenario identifier
  - `"description"`: `str`, flavor text describing the scenario (not used for classification)
  - `"mechanism"`: `str`, one of `"policy_document"`, `"training_program"`,
    `"access_review_process"`, `"software_or_hardware_enforcement"`, `"physical_barrier"`

## Output
A `list[str]` of classifications, **one per input scenario, in the same order as the input**. Each
entry is one of `"managerial"`, `"technical"`, `"physical"`.

## Examples
```python
scenarios = [
    {"id": "s1", "description": "New hires sign a document listing allowed and prohibited use of company laptops.",
     "mechanism": "policy_document"},
    {"id": "s2", "description": "The office network blocks known-malicious IP ranges automatically.",
     "mechanism": "software_or_hardware_enforcement"},
    {"id": "s3", "description": "The server room door requires a badge to open.",
     "mechanism": "physical_barrier"},
]
classify_controls(scenarios)  ->  ["managerial", "technical", "physical"]
```

## Constraints
- Deterministic, offline, standard library only.
- Classification depends only on `"mechanism"`, never on `"description"` text.
- Mapping: `"policy_document"`, `"training_program"`, and `"access_review_process"` are all
  `"managerial"`; `"software_or_hardware_enforcement"` is `"technical"`; `"physical_barrier"` is
  `"physical"`.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
