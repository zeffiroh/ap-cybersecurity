# Interface, 2.3.a-physical-access-controls (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(data: dict[str, bool]) -> list[str]
```

## Input (`data`)
A dictionary mapping physical access control elements to boolean values indicating their presence (`True` if present, `False` if absent):
- `keyed_lock`: bool
- `badge_reader`: bool
- `biometric_reader`: bool
- `mantrap`: bool
- `cctv`: bool
- `security_guard`: bool

## Output (`result`)
A sorted list of string identifiers representing the security gaps discovered in the facility:
- `no_key_control`
- `no_electronic_access`
- `no_tailgating_prevention`
- `no_visual_monitoring`
- `no_identity_verification`

## Guarantees / rules
- Pure function, deterministic, no I/O, no network.
- Standard library only.
- The rules for gaps are:
  - If `keyed_lock` is False AND `badge_reader` is False: gap `"no_key_control"`
  - If `badge_reader` is False AND `biometric_reader` is False: gap `"no_electronic_access"`
  - If `mantrap` is False: gap `"no_tailgating_prevention"`
  - If `cctv` is False: gap `"no_visual_monitoring"`
  - If `security_guard` is False AND `biometric_reader` is False: gap `"no_identity_verification"`
- The resulting list of gaps must be sorted alphabetically.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
