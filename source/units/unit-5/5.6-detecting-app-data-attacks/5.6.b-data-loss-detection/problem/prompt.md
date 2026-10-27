# Coding problem, 5.6.b: DLP egress rule

**Skill:** Detect Attacks · **Maps to:** 5.6.B · **Language:** Python 3 (pytest)

## Problem
Implement the volume/behavior-based DLP rule described in the lesson: given a list of outbound
transfer events, flag the ones that exceed a size threshold AND go to a destination that is not
on the organization's approved-destination list, a classic egress-monitoring rule.

## Function contract
Implement `solve(transfers: list, approved_destinations: list, volume_threshold_mb: int) -> list`
in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
- `transfers`: `list[dict]`, each `{"id": str, "bytes_mb": int, "destination": str}`.
- `approved_destinations`: `list[str]` of known-good destination names.
- `volume_threshold_mb`: `int`, transfer must exceed this size to be eligible for flagging.

## Output
Sorted `list[str]` of flagged transfer `id`s.

## Examples
```
transfers = [{"id":"t1","bytes_mb":500,"destination":"unknown-cloud.example"}]
solve(transfers, ["corp-backup.internal"], volume_threshold_mb=100) -> ["t1"]
```

```
transfers = [{"id":"t2","bytes_mb":500,"destination":"corp-backup.internal"}]
solve(transfers, ["corp-backup.internal"], volume_threshold_mb=100) -> []   # approved destination
```

## Constraints
- Deterministic, offline, standard library only.
- The size comparison is strict (`bytes_mb > volume_threshold_mb`).
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
