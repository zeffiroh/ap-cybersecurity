# Coding problem, 2.2.c: Device theft/tampering incident triage

**Skill:** Analyze Risk · **Maps to:** 2.2.B, 2.2.C · **Language:** Python 3 (pytest)

## Problem
The IT security team receives reports whenever a device is reported stolen or found to show signs
of tampering. Each report needs to be triaged into a risk level so the team knows what needs an
immediate incident response versus what can be logged and monitored.

Your task is to write a function `solve(data)` that takes a list of incident reports and returns a
dictionary mapping each incident's `id` to a risk level: `"LOW"`, `"MEDIUM"`, or `"HIGH"`.

### Rules, by incident `type`

**`type == "theft"`** (a device was physically taken):
1. `"HIGH"` if the device was **not** encrypted (`encrypted` is `False`), an unencrypted stolen
   device exposes its data with no cryptographic barrier.
2. `"MEDIUM"` if the device **was** encrypted, but `contains_sensitive_data` is `True` **and**
   `hours_since_check` is greater than `48`, encryption protects the data, but a long detection
   delay on a sensitive device still raises risk (e.g., the device may have been unlocked and
   in active use when taken).
3. `"LOW"` otherwise.

**`type == "tampering"`** (a device was found to show signs of covert alteration):
1. `"HIGH"` if the tamper-evident seal was **not** intact (`seal_intact` is `False`), physical
   evidence the enclosure was opened.
2. `"MEDIUM"` if the seal **was** intact but `hours_since_check` is greater than `48`, a long
   window since the last inventory check means tampering that does not require opening the
   enclosure (e.g., a rogue USB implant) could have gone unnoticed even with an intact seal.
3. `"LOW"` otherwise.

Any other `type` value should be treated as `"LOW"`.

## Function contract
Implement `solve(data: list[dict]) -> dict[str, str]` in `starter.py`.

## Input
A list of dictionaries, each representing one incident report:
```python
[
    {
        "id": "inc-1",
        "type": "theft",
        "encrypted": False,
        "seal_intact": True,
        "contains_sensitive_data": True,
        "hours_since_check": 10,
    },
    {
        "id": "inc-2",
        "type": "tampering",
        "encrypted": True,
        "seal_intact": False,
        "contains_sensitive_data": False,
        "hours_since_check": 5,
    },
]
```
Every report includes all five fields (`type`, `encrypted`, `seal_intact`,
`contains_sensitive_data`, `hours_since_check`), even if a field is not relevant to that report's
`type` (e.g., `seal_intact` is present but ignored for `type == "theft"`).

## Output
A dictionary mapping each incident's `"id"` to its risk level string:
```python
{
    "inc-1": "HIGH",
    "inc-2": "HIGH",
}
```

## Constraints
- `type` is `"theft"` or `"tampering"` (or, in hidden tests, possibly another string that must
  default to `"LOW"`).
- `encrypted`, `seal_intact`, `contains_sensitive_data` are booleans.
- `hours_since_check` is a non-negative number (int or float).
- Pure function, deterministic, standard library only.

## How to run
```bash
cd problem && python -m pytest tests.py -q
```
