# Coding problem, 5.1.c: Detect broken object-level authorization (BOLA)

**Skill:** Analyze Risk · **Maps to:** 5.1.B · **Language:** Python 3 (pytest)

## Problem
Build the server-side authorization check an API gateway should run before returning an object.
Given the authenticated caller's user id, the id of the object they are requesting, an
object-ownership map, and the caller's role, decide whether the request is allowed.

Rules:
- A request is **allowed** if the caller owns the requested object (the object's `owner` equals
  the caller's `user_id`), OR the caller's `role` is `"admin"`.
- A request is **denied** (a BOLA violation) if the object exists but the caller neither owns it
  nor is an admin.
- A request for an object id that does not exist in the ownership map is **denied** with reason
  `"not_found"`.

## Function contract
Implement `solve(request: dict, ownership: dict) -> dict` in `starter.py` (see `interface.md` /
`blackbox.yaml`).

## Input
- `request`: `{"user_id": str, "role": str, "object_id": str}`
- `ownership`: `dict` mapping `object_id -> owner user_id` (e.g. `{"482": "u1", "483": "u2"}`)

## Output
A dict: `{"allowed": bool, "reason": str}` where `reason` is one of
`"owner"`, `"admin"`, `"not_owner"`, `"not_found"`.

## Examples
```
request={"user_id":"u1","role":"user","object_id":"482"}, ownership={"482":"u1"}
    -> {"allowed": True, "reason": "owner"}

request={"user_id":"u1","role":"user","object_id":"483"}, ownership={"483":"u2"}
    -> {"allowed": False, "reason": "not_owner"}

request={"user_id":"u9","role":"admin","object_id":"483"}, ownership={"483":"u2"}
    -> {"allowed": True, "reason": "admin"}

request={"user_id":"u1","role":"user","object_id":"999"}, ownership={"483":"u2"}
    -> {"allowed": False, "reason": "not_found"}
```

## Constraints
- Deterministic, offline, standard library only.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
