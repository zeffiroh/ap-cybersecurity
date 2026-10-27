# Interface, 3.5.c-ir-phase-sorter (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(actions: list[dict]) -> list[str]
```

## Input

### `actions`, list of action record dicts, in arbitrary order
Each dict has:
- `"action"` (str): description of the response action
- `"phase"` (str): one of the six canonical NIST IR phase names, spelled exactly:
  `"Preparation"`, `"Identification"`, `"Containment"`, `"Eradication"`, `"Recovery"`,
  `"Lessons Learned"`

## Canonical phase order
```
1. Preparation
2. Identification
3. Containment
4. Eradication
5. Recovery
6. Lessons Learned
```

## Output (`result`)
`list[str]` of the `"action"` text values from the input, reordered so actions belonging to an
earlier phase (per the canonical order) precede actions from a later phase. Actions within the
same phase retain their relative order from the input (stable sort).

## Errors
- If any action's `"phase"` is not one of the six canonical names exactly, raise `ValueError`.

## Guarantees / rules
- Pure function; deterministic; no I/O; no network access.
- `actions` is not mutated by `solve`.
- Standard library only.

## Acceptance
`python -m pytest tests.py -q` passes all visible and hidden cases.
