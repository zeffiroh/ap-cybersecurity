# Coding problem, 2.3.a: Physical access controls (locks, badges, biometrics, mantraps)

**Skill:** Mitigate Risk · **Maps to:** 2.3.A · **Language:** Python 3 (pytest)

## Problem
In physical security auditing, we look at the combination of active controls to identify vulnerabilities or gaps in a layered defense. You are tasked with implementing a function that takes a description of a facility's physical security inventory and returns all identified security gaps based on audit rules.

Implement `solve(data: dict[str, bool]) -> list[str]` in `starter.py`.

## Input
A dictionary containing the following keys (each mapping to a boolean representing presence of that control):
- `keyed_lock`
- `badge_reader`
- `biometric_reader`
- `mantrap`
- `cctv`
- `security_guard`

Example:
```python
{
    "keyed_lock": True,
    "badge_reader": True,
    "biometric_reader": False,
    "mantrap": False,
    "cctv": True,
    "security_guard": False
}
```

## Output
A list of strings representing the detected security gaps, sorted alphabetically:
- `no_key_control`: triggered if both `keyed_lock` and `badge_reader` are absent.
- `no_electronic_access`: triggered if both `badge_reader` and `biometric_reader` are absent.
- `no_tailgating_prevention`: triggered if `mantrap` is absent.
- `no_visual_monitoring`: triggered if `cctv` is absent.
- `no_identity_verification`: triggered if both `security_guard` and `biometric_reader` are absent.

## Examples
```python
{
    "keyed_lock": True,
    "badge_reader": True,
    "biometric_reader": False,
    "mantrap": False,
    "cctv": True,
    "security_guard": False
}
# returns ["no_identity_verification", "no_tailgating_prevention"]

{
    "keyed_lock": False,
    "badge_reader": False,
    "biometric_reader": False,
    "mantrap": True,
    "cctv": False,
    "security_guard": True
}
# returns ["no_electronic_access", "no_key_control", "no_visual_monitoring"]
```

## Constraints
- Deterministic, offline, standard library only.
- Must pass all cases in `tests.py`.

## How to run
```
cd problem && python -m pytest tests.py -q
```
