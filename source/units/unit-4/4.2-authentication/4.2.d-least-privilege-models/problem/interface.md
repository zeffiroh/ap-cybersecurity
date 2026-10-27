# Interface, 4.2.d-access-request-auditor (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(request: dict) -> str
```

## Input (`request`)
A dict describing one access request:

| key | type | required | default if missing | meaning |
|---|---|---|---|---|
| `current_role` | str | no | `""` | the requester's current job role (informational; not used in the decision below, but always present in well-formed data) |
| `requested_access` | str | no | `""` | the resource/access level being requested (informational) |
| `justification_present` | bool | yes | `False` | whether a business justification was submitted with the request |
| `time_bound` | bool or None | no | `False` | whether the requested access is scoped to a fixed, temporary time window; `None` is treated the same as `False` |
| `last_reviewed_days_ago` | int | no | `0` | days since this requester's access was last reviewed/recertified |

Missing optional keys default as shown above. `justification_present` is required conceptually
(it drives the first rule) but if the key is absent, treat it as `False` (fail closed).

## Output (`result`)
Exactly one string from `{"approve", "deny_no_justification", "flag_privilege_creep",
"approve_time_bound"}`.

## Decision rule (exact priority order, evaluate top to bottom, return on first match)
1. If `justification_present` is `False` (or missing) → return `"deny_no_justification"`.
   This is checked FIRST and overrides every other condition, including privilege creep.
2. Else if `last_reviewed_days_ago > 365` → return `"flag_privilege_creep"`.
   A stale access review (more than 365 days since last review) takes priority over approving,
   even if the request is time-bound. The threshold is a strict greater-than: exactly `365` does
   NOT trigger this rule.
3. Else if `time_bound` is `True` → return `"approve_time_bound"`.
4. Else → return `"approve"`.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network.
- Standard library only unless `blackbox.yaml: allow_deps` lists otherwise.
- Missing optional keys use the defaults in the table above; do not raise on missing keys.
- `last_reviewed_days_ago == 365` is NOT stale (rule 2 requires strictly greater than 365).

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
