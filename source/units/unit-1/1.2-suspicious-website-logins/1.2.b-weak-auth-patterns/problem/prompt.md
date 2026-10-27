# Coding problem, 1.2.b: Password weakness reporter

**Skill:** Analyze Risk · **Maps to:** 1.2.B · **Language:** Python 3 (pytest)

## Problem
Build the password-weakness checker an authentication backend would use to give users actionable
feedback when they choose a new password. Given a password string, return a report dict
identifying whether the password is weak and which specific rules it violates.

## Function contract
Implement `solve(password: str) -> dict` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
A single string, the candidate password. May be empty.

## Output
A dict with exactly two keys:
- `"weak"` (`bool`), `True` if the password fails ANY rule; `False` only if it passes all rules.
- `"reasons"` (`list[str]`), sorted list of rule-labels for each rule the password fails.
  Empty list if the password passes all rules.

Possible reason labels (exact strings, lowercase):
- `"too_short"`, length < 12 characters
- `"in_dictionary"`, password (lowercased) is in the built-in common wordlist
- `"only_lowercase"`, contains no uppercase letters, digits, or non-alphabetic characters
- `"sequential_or_repeated"`, contains a sequential run of 3+ characters (e.g. `abc`, `123`,
  `xyz`) OR a repeated run of 3+ identical characters (e.g. `aaa`, `111`)

## Examples
```
solve("password")
-> {"weak": True, "reasons": ["in_dictionary", "only_lowercase", "too_short"]}

solve("P@ssword!2024")
-> {"weak": True, "reasons": ["in_dictionary"]}

solve("Tr0ub4dor&3abcde")
-> {"weak": True, "reasons": ["sequential_or_repeated"]}

solve("mXk9#vLq2@nP")
-> {"weak": False, "reasons": []}
```

## Constraints
- Deterministic, offline, standard library only.
- The common wordlist is defined in `interface.md` and must be embedded in your solution.
- Reasons list is always sorted ascending.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
