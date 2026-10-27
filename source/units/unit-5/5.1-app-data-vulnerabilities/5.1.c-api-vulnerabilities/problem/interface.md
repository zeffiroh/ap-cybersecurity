# Interface, 5.1.c-bola-check (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(request: dict, ownership: dict) -> dict
```

## Input
- `request`: `{"user_id": str, "role": str, "object_id": str}`, the authenticated caller and the
  object they are requesting.
- `ownership`: `dict[str, str]` mapping `object_id -> owner user_id`.

## Output (`result`)
`{"allowed": bool, "reason": str}` where `reason` is exactly one of:
- `"owner"`, caller's `user_id` matches the object's owner.
- `"admin"`, caller's `role` is `"admin"` (allowed regardless of ownership).
- `"not_owner"`, object exists but caller neither owns it nor is admin.
- `"not_found"`, `object_id` is not a key in `ownership`.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Ownership check takes priority: if the caller owns the object, reason is `"owner"` even if role
  is also `"admin"`.
- `"not_found"` is checked independently of role/ownership, a missing object is always denied.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
