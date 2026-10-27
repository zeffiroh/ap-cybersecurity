# Interface, 5.2.b-least-privilege-audit (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(roles: dict, user_roles: dict, job_requirements: dict) -> dict
```

## Input
- `roles`: `dict[str, list[str]]`, role name -> permissions it grants.
- `user_roles`: `dict[str, list[str]]`, user name -> assigned role names.
- `job_requirements`: `dict[str, list[str]]`, user name -> permissions their job requires. A user
  absent from this dict requires no permissions (empty set).

## Output (`result`)
`dict[str, list[str]]` mapping each user who has at least one excess permission to the **sorted**
list of their excess permissions (permissions granted by their roles but not in their job
requirements). Users with zero excess permissions are omitted entirely from the result.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Permissions from multiple assigned roles are unioned (deduplicated) before comparing against
  job requirements.
- Unknown role names in `user_roles` (not present in `roles`) contribute no permissions.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
