# Interface, 1.5.d-incident-triage-metrics (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(incidents: list[dict]) -> dict
```

## Input (`incidents`)
A list of incident dicts. Each dict has exactly these keys:

| Key           | Type  | Description                                                          |
|---------------|-------|----------------------------------------------------------------------|
| `id`          | str   | Unique incident identifier string (e.g. `"INC-001"`)                |
| `detected_at` | int   | Unix timestamp (seconds) when the incident was detected              |
| `resolved_at` | int   | Unix timestamp (seconds) when the incident was resolved; always > detected_at |
| `severity`    | str   | One of `"critical"`, `"high"`, `"medium"`, `"low"`                  |
| `auto`        | bool  | `True` if the incident was resolved automatically; `False` if human-resolved |

Example single entry:
```python
{"id": "INC-001", "detected_at": 1000, "resolved_at": 1120, "severity": "critical", "auto": False}
```

## Output (`result`)
A dict with exactly two keys:

| Key            | Type  | Description                                                           |
|----------------|-------|-----------------------------------------------------------------------|
| `"mttr"`       | float | Mean time to respond in seconds, averaged across ALL incidents.       |
| `"auto_resolved"` | int | Count of incidents where `auto == True`.                           |

`mttr` is computed as:
  `sum(resolved_at - detected_at for each incident) / len(incidents)`

If `incidents` is empty, return `{"mttr": 0.0, "auto_resolved": 0}`.

The `mttr` value is a Python `float` (may be a whole number like `120.0`).
The `auto_resolved` value is a Python `int`.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network.
- Standard library only.
- `incidents` is a list (may be empty).
- `resolved_at > detected_at` always; all timestamps are non-negative integers.
- `severity` is always one of the four valid strings; implementations need not validate it.
- No incident has a negative response time.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
