# Interface, 3.3.b-zero-trust-proxy (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(requests: list, policy: dict) -> list
```

## Input (`requests`, `policy`)
- `requests`: `list[dict]`, List of connection requests. Each request is a dictionary with:
  - `id`: `str`, Unique request identifier.
  - `user`: `str`, Username.
  - `role`: `str`, User role (e.g., "doctor", "guest", "admin").
  - `resource`: `str`, Destination resource name.
  - `ip`: `str`, Source IP address.
  - `device_posture`: `dict[str, bool]`, Key-value pairs of health posture checks.
- `policy`: `dict`, Zero-trust access policy specification containing:
  - `allowed_roles`: `dict[str, list[str]]`, Resource name mapped to list of allowed roles.
  - `requires_internal`: `list[str]`, List of resources requiring an internal IP address.
  - `requires_posture`: `list[str]`, List of resources requiring full device posture compliance.
  - `internal_prefixes`: `list[str]`, List of IP address prefix strings considered internal.

## Output (`result`)
`list[str]`, List of `id`s of the requests that are **allowed**, preserving their original order.

## Policy Rules
For a connection request to be allowed, it must satisfy all of the following:
1. **Role Authorization:** The request's `role` must be in the `allowed_roles` list for the requested `resource`. If the resource is not in `allowed_roles`, it is automatically denied.
2. **Network Isolation:** If the `resource` is in the `requires_internal` list, the request's `ip` must start with one of the prefixes in the `internal_prefixes` list.
3. **Posture Check:** If the `resource` is in the `requires_posture` list, all checks within the request's `device_posture` dictionary must be `True`. If `device_posture` has no checks, it is considered compliant.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network.
- Standard library only.
- Output list preserves the relative order of allowed request IDs from the input.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
