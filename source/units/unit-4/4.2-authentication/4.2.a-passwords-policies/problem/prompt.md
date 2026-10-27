# Coding problem, 4.2.a: Passwords and password policies

**Skill:** Mitigate Risk · **Maps to:** 4.2.A · **Language:** Python 3 (pytest)

## Problem
A system administrator has defined a password policy (minimum length, complexity requirements,
a banned/breached-password list, and a history of previously used passwords). Build the checker
that evaluates a candidate password against that policy and reports every rule it violates, so
the login form can show the user exactly what to fix.

## Function contract
Implement `validate_password(password: str, policy: dict) -> list[str]` in `starter.py`
(see `interface.md` / `blackbox.yaml`).

## Input
- `password`, a string, the candidate password.
- `policy`, a dict. Example:
  ```python
  policy = {
      "min_length": 12,
      "require_upper": True,
      "require_lower": True,
      "require_digit": True,
      "require_symbol": True,
      "banned_list": ["password123", "letmein", "qwerty123456"],
      "history": ["OldPass2023!", "OldPass2024!"],
  }
  ```
  Any key may be omitted; a missing key means that rule is not enforced (see `interface.md` for
  exact defaults).

## Output
A `list[str]` of violated rule names, in the fixed order defined in `interface.md`:
`too_short`, `no_upper`, `no_lower`, `no_digit`, `no_symbol`, `in_banned_list`,
`reused_password`. An empty list `[]` means the password is fully compliant.

## Examples
```
validate_password("abc", {"min_length": 12, "require_upper": True, "require_digit": True})
    -> ["too_short", "no_upper", "no_digit"]

validate_password("Password123", {"banned_list": ["password123"]})
    -> ["in_banned_list"]

validate_password(
    "Tr0ub4dor&3xtra!",
    {"min_length": 12, "require_upper": True, "require_lower": True,
     "require_digit": True, "require_symbol": True,
     "banned_list": ["password123"], "history": ["OldPass2023!"]},
) -> []
```

## Constraints
- Deterministic, offline, standard library only.
- Missing policy keys are treated as "not required" (see `interface.md` for exact defaults).
- Violated rule names must be returned in the fixed order given above, even when several rules
  are violated at once.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
