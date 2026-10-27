# Interface, 2.3.d-facility-control-compliance (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(zones: list[dict], policy: dict) -> list[str]
```

## Input (`zones`)
`list[dict]` where each dict has:
- `"name"`: `str`, zone identifier
- `"room_type"`: `str`, key into `policy`
- `"has_ups"`: `bool`
- `"hvac_redundancy"`: `int`, count of extra HVAC units beyond the single minimum (0 = no redundancy)
- `"suppression"`: `str`, one of `"water"`, `"clean_agent"`, `"none"`
- `"has_leak_sensor"`: `bool`

## Input (`policy`)
`dict[str, dict]` mapping `room_type` -> a requirements dict with any subset of:
- `"require_ups"`: `bool`
- `"min_hvac_redundancy"`: `int`
- `"allowed_suppression"`: `list[str]`
- `"require_leak_sensor"`: `bool`

A room type absent from `policy` has no requirements.
A requirement key absent from a room type's entry is not enforced for that room type.

## Output (`result`)
A **sorted, de-duplicated** `list[str]` of zone name strings that fail one or more applicable
requirements. Empty list if every zone is compliant.

## Compliance rules
- `require_ups: True` -> zone fails if `has_ups` is not `True`.
- `min_hvac_redundancy: N` -> zone fails if `hvac_redundancy < N`.
- `allowed_suppression: [...]` -> zone fails if `suppression` is not in the list.
- `require_leak_sensor: True` -> zone fails if `has_leak_sensor` is not `True`.
- A zone fails (is non-compliant) if it fails ANY one applicable rule.
- A zone whose `room_type` has no entry in `policy` is always compliant.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Zones may be given in any order.
- Output always sorted ascending and de-duplicated.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
