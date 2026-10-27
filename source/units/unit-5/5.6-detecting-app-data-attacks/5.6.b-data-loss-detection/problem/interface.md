# Interface, 5.6.b-dlp-egress-rule (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(transfers: list, approved_destinations: list, volume_threshold_mb: int) -> list
```

## Input
- `transfers`: `list[dict]`, each `{"id": str, "bytes_mb": int, "destination": str}`. `id` is
  unique per transfer.
- `approved_destinations`: `list[str]` of destination names considered safe/sanctioned.
- `volume_threshold_mb`: `int`, a transfer must exceed this size (strictly greater than) to be
  eligible for flagging.

## Output (`result`)
Sorted `list[str]` of transfer `id`s that should be flagged: `bytes_mb > volume_threshold_mb`
AND `destination` is NOT in `approved_destinations`.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- The size comparison is strict (`>`, not `>=`): a transfer exactly at the threshold is not
  flagged.
- An empty `approved_destinations` list means every destination is treated as unapproved.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
