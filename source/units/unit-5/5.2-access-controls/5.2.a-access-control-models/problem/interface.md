# Interface, 5.2.a-access-decision (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(request: dict) -> dict
```

## Input (`request`)
`{"subject": dict, "object": dict, "action": str}`

- DAC object: `{"model": "dac", "owner": str, "grants": {action: [subject_name...]}}`;
  subject: `{"name": str}`.
- MAC object: `{"model": "mac", "classification": str}`; subject: `{"clearance": str}`.
  Levels low->high: `"public"`, `"confidential"`, `"secret"`, `"top_secret"`.
- RBAC object: `{"model": "rbac", "allowed_roles": {action: [role...]}}`;
  subject: `{"roles": [role...]}`.

## Output (`result`)
`{"allowed": bool, "reason": str}` where `reason` is one of `"owner"`, `"granted"`,
`"dac_denied"`, `"clearance_sufficient"`, `"clearance_insufficient"`, `"role_match"`,
`"rbac_denied"`, `"unknown_model"`.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- DAC: owner check takes priority over grants list.
- MAC: allowed when subject clearance level >= object classification level (equal is allowed).
- RBAC: allowed if any of the subject's roles appears in the object's allowed_roles for the action.
- Any `object.model` outside `{"dac","mac","rbac"}` -> `{"allowed": False, "reason": "unknown_model"}`.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
