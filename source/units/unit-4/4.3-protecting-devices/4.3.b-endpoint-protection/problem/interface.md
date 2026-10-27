# Interface, 4.3.b-endpoint-protection (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(data: dict) -> list[int]
```

## Input (`data`)
A dictionary containing:
- `"signatures"`: list of strings (MD5 hashes of known malware)
- `"behavioral_rules"`: dict with keys:
  - `"max_file_modifications"` (int)
  - `"max_network_connections"` (int)
- `"processes"`: list of dicts, where each dict has:
  - `"pid"` (int)
  - `"name"` (string)
  - `"hash"` (string)
  - `"file_modifications"` (int)
  - `"network_connections"` (int)

## Output (`result`)
A list of integers representing the PIDs of flagged processes.
A process is flagged if:
1. Its hash is in the `"signatures"` list.
2. Its `"file_modifications"` is strictly greater than `"max_file_modifications"`.
3. Its `"network_connections"` is strictly greater than `"max_network_connections"`.

The output list of PIDs must be sorted in ascending order. If no processes are flagged, returns `[]`.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network.
- Standard library only.
- Case-insensitivity: MD5 hash comparisons should be case-insensitive (e.g., `"A1B2"` matches `"a1b2"`).

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
