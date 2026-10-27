# Interface, 3.1.a-ip-spoofing-detector (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(data) -> result
```

## Input (`data`)
`list[dict]` of packet logs. Each dict represents a packet and has the following keys:
- `"src_ip"` (str), e.g. `"10.0.1.55"`
- `"dst_ip"` (str), e.g. `"10.0.1.1"`
- `"expected_subnet"` (str), e.g. `"10.0.1.0/24"`

## Output (`result`)
`list[int]`, A sorted list of zero-based integer indices of the suspicious (spoofed) packets where the `src_ip` does not belong to the `expected_subnet`.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network.
- Standard library only.
- A packet is flagged if the IP address in `"src_ip"` falls outside the CIDR range in `"expected_subnet"`. If format validation fails, it should also be flagged.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
