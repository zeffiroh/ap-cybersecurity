# Interface, 3.5.b-traffic-anomaly-detector (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(baseline: dict, flows: list[dict]) -> list[str]
```

## Input

### `baseline`, dict mapping host IP (str) -> profile dict
Each profile dict has:
- `"max_bytes"` (int): maximum normal total outbound bytes for this host in the window
- `"allowed_ports"` (list[int]): destination ports normally used by this host

### `flows`, list of observed flow record dicts (any order, possibly multiple per host)
Each flow dict has:
- `"host"` (str): source host IP
- `"dst_port"` (int): destination port
- `"bytes"` (int): bytes sent in this flow

## Output (`result`)
Sorted `list[str]` of host IPs flagged as anomalous, no duplicates.

## Flagging rules
A host is flagged if ANY of the following hold:
1. Host is not a key in `baseline` (unknown host, no profile to compare against).
2. The sum of `"bytes"` across all of that host's flow records exceeds `baseline[host]["max_bytes"]`.
3. Any single flow record for that host has a `"dst_port"` not in `baseline[host]["allowed_ports"]`.

## Guarantees / rules
- Pure function; deterministic; no I/O; no network access.
- `baseline` and `flows` are not mutated by `solve`.
- Standard library only.

## Acceptance
`python -m pytest tests.py -q` passes all visible and hidden cases.
