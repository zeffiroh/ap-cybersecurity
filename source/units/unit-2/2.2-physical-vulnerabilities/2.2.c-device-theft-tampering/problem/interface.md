# Interface, 2.2.c-incident-triage (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(data: list[dict]) -> dict[str, str]
```

## Input (`data`)
A list of dictionaries representing device incident reports. Each dictionary contains:
- `id` (str): Unique identifier for the incident.
- `type` (str): `"theft"` or `"tampering"` (other values default to `"LOW"`).
- `encrypted` (bool): Whether the device's storage was encrypted.
- `seal_intact` (bool): Whether the tamper-evident seal was intact when discovered.
- `contains_sensitive_data` (bool): Whether the device held sensitive data.
- `hours_since_check` (float/int): Hours since the device was last verified present/unaltered.

## Output (`result`)
A dictionary where keys are the `id` of each incident from the input and values are the risk
level: `"LOW"`, `"MEDIUM"`, or `"HIGH"`.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network.
- Standard library only.
- Rules by `type` (see prompt.md for full detail):
  1. `theft`: not `encrypted` -> `HIGH`; `encrypted` and `contains_sensitive_data` and
     `hours_since_check > 48` -> `MEDIUM`; else `LOW`.
  2. `tampering`: not `seal_intact` -> `HIGH`; `seal_intact` and `hours_since_check > 48` ->
     `MEDIUM`; else `LOW`.
  3. any other `type` -> `LOW`.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
