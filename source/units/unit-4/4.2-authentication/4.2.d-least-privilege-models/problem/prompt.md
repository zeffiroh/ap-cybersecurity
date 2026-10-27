# Coding problem, 4.2.d: Access-request auditor

**Skill:** Mitigate Risk · **Maps to:** 4.2.B, 4.2.C · **Language:** Python 3 (pytest)

## Problem
A security team reviews access requests before granting them. Each request either has a business
justification attached or it does not; the requester's access may or may not have been reviewed
recently; and the requested access may be scoped to a temporary time window or be standing
(permanent). Build the auditor function that applies the least-privilege triage rules to a single
request and returns the decision.

## Function contract
Implement `def solve(request: dict) -> str` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
A dict with keys `current_role` (str), `requested_access` (str), `justification_present` (bool),
`time_bound` (bool or None), `last_reviewed_days_ago` (int). Optional keys default as documented
in `interface.md` (missing `justification_present` defaults to `False`; missing `time_bound`
defaults to `False`; missing `last_reviewed_days_ago` defaults to `0`).

## Output
One of the strings: `"approve"`, `"deny_no_justification"`, `"flag_privilege_creep"`,
`"approve_time_bound"`.

## Decision rule (apply in this exact order, first match wins)
1. No justification (`justification_present` is `False`) → `"deny_no_justification"`.
2. Else, stale review (`last_reviewed_days_ago > 365`) → `"flag_privilege_creep"`.
3. Else, time-bound request (`time_bound` is `True`) → `"approve_time_bound"`.
4. Else → `"approve"`.

Rule 1 is checked before rule 2, a request with no justification is denied even if it is also
years overdue for review or time-bound. The staleness threshold is 365 days, strictly greater
than (365 itself is still considered current).

## Examples
```
{"current_role": "Marketing Intern", "requested_access": "prod-db-write",
 "justification_present": False, "time_bound": False, "last_reviewed_days_ago": 10}
    -> "deny_no_justification"

{"current_role": "HR Analyst", "requested_access": "payroll-admin",
 "justification_present": True, "time_bound": False, "last_reviewed_days_ago": 800}
    -> "flag_privilege_creep"

{"current_role": "On-call Engineer", "requested_access": "prod-ssh",
 "justification_present": True, "time_bound": True, "last_reviewed_days_ago": 5}
    -> "approve_time_bound"

{"current_role": "Analyst", "requested_access": "reporting-read",
 "justification_present": True, "time_bound": False, "last_reviewed_days_ago": 30}
    -> "approve"
```

## Constraints
- Deterministic, offline, standard library only.
- Missing optional keys must not raise, use the documented defaults.
- Exactly one label returned (string, not list).
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
