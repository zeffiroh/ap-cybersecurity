# Coding problem, 5.2.b: Detect least-privilege violations

**Skill:** Mitigate Risk · **Maps to:** 5.2.A, 5.2.B · **Language:** Python 3 (pytest)

## Problem
Build the audit function a security reviewer would run over a company's role assignments. Given a
map of roles to the permissions they grant, a map of users to their assigned roles, and a map of
users to the minimum permission set their job function actually requires, find every user who
holds at least one permission (via their assigned roles) that is NOT in their job function's
required set.

## Function contract
Implement `solve(roles: dict, user_roles: dict, job_requirements: dict) -> dict` in `starter.py`
(see `interface.md` / `blackbox.yaml`).

## Input
- `roles`: `dict[str, list[str]]`, role name -> list of permissions it grants.
- `user_roles`: `dict[str, list[str]]`, user name -> list of role names assigned to them.
- `job_requirements`: `dict[str, list[str]]`, user name -> list of permissions their job function
  actually requires.

## Output
A dict mapping each violating user to the **sorted** list of their excess (unauthorized)
permissions. Users with no excess permissions are omitted entirely from the result.

## Examples
```
roles = {"support": ["read_ticket", "write_ticket_reply"], "billing": ["read_invoice", "issue_refund"]}
user_roles = {"dana": ["support", "billing"]}
job_requirements = {"dana": ["read_ticket", "write_ticket_reply"]}

solve(roles, user_roles, job_requirements)
-> {"dana": ["issue_refund", "read_invoice"]}
```

```
roles = {"support": ["read_ticket"]}
user_roles = {"sam": ["support"]}
job_requirements = {"sam": ["read_ticket"]}

solve(roles, user_roles, job_requirements)
-> {}
```

## Constraints
- Deterministic, offline, standard library only.
- A user with roles granting no permissions beyond their job requirements is omitted from the
  output entirely (not included with an empty list).
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
