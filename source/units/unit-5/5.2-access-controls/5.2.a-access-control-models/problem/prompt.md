# Coding problem, 5.2.a: RBAC / DAC / MAC access decision

**Skill:** Mitigate Risk · **Maps to:** 5.2.A · **Language:** Python 3 (pytest)

## Problem
Build the access-decision function a policy engine would run for a fictional file system that
supports all three access control models. Given a request (subject, object, action, and the
object's model), decide whether the request is ALLOWed or DENYed.

## Rules by model
- **`"dac"`**, allowed if the subject is the object's `owner`, OR the subject appears in the
  object's `grants` list for that action (e.g., `grants: {"read": ["bob"], "write": []}`).
- **`"mac"`**, allowed only if the subject's clearance level is `>=` the object's classification
  level. Levels (low to high): `"public"` < `"confidential"` < `"secret"` < `"top_secret"`.
- **`"rbac"`**, allowed if any of the subject's `roles` is present in the object's
  `allowed_roles` list for the requested action (e.g.,
  `allowed_roles: {"read": ["nurse","admin"], "write": ["admin"]}`).

If the object's `model` is not one of `"dac"`, `"mac"`, `"rbac"`, deny with reason `"unknown_model"`.

## Function contract
Implement `solve(request: dict) -> dict` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
`request`: a dict with keys `"subject"` (dict) and `"object"` (dict) and `"action"` (str).
See `interface.md` for the exact shape per model.

## Output
`{"allowed": bool, "reason": str}` where reason is one of
`"owner"`, `"granted"`, `"dac_denied"`, `"clearance_sufficient"`, `"clearance_insufficient"`,
`"role_match"`, `"rbac_denied"`, `"unknown_model"`.

## Examples
```
DAC owner:
  {"subject":{"name":"alice"},"object":{"model":"dac","owner":"alice","grants":{}},"action":"read"}
  -> {"allowed": True, "reason": "owner"}

MAC insufficient clearance:
  {"subject":{"clearance":"confidential"},"object":{"model":"mac","classification":"secret"},"action":"read"}
  -> {"allowed": False, "reason": "clearance_insufficient"}

RBAC role match:
  {"subject":{"roles":["nurse"]},"object":{"model":"rbac","allowed_roles":{"read":["nurse","admin"]}},"action":"read"}
  -> {"allowed": True, "reason": "role_match"}
```

## Constraints
- Deterministic, offline, standard library only.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
