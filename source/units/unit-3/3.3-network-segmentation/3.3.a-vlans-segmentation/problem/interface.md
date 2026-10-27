# Interface, 3.3.a-vlan-flow-filter (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(vlan_map: dict, flows: list) -> list
```

## Input (`vlan_map`, `flows`)
- `vlan_map`: `dict[str, int]`, host name to VLAN ID.
- `flows`: `list[tuple[str, str]]`, list of (src_host, dst_host) pairs.

## Output (`result`)
`list[tuple[str, str]]`, the subset of `flows` that are **blocked**, preserving input order.

## Policy rules (applied in order)
1. If `vlan_map[src] == vlan_map[dst]`, **allowed** (same VLAN).
2. If `vlan_map[src] == 20` and `vlan_map[dst] == 30`, **allowed** (Employee -> Server exception).
3. All other cases, **blocked**.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- All hosts in `flows` are guaranteed to exist in `vlan_map`.
- Output list preserves the relative order of blocked flows from the input.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
