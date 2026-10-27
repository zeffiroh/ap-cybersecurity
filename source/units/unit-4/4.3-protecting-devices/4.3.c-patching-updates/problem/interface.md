# Interface, 4.3.c-patch-prioritization-engine (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(vulns: list) -> list
```

## Input (`vulns`)
A list of dicts, each describing one vulnerability:

| key | type | meaning |
|---|---|---|
| `id` | str | vulnerability identifier, echoed unchanged into the output |
| `cvss` | float | CVSS severity score, 0.0-10.0 |
| `exploited_in_wild` | bool | whether the vulnerability is confirmed being actively exploited |
| `internet_facing` | bool | whether the affected asset is reachable from the public internet |
| `end_of_life` | bool | whether the affected software is end-of-life (no patch will ever ship) |

## Output (`result`)
A list of dicts, same length and same order as the input, each with:
- `"id"`: the same id string from the corresponding input entry
- `"urgency"`: one of `"emergency"`, `"scheduled"`, `"routine"`, `"compensate"`

## Decision rule (exact priority order, evaluate top to bottom per vulnerability, return on
first match)
1. If `end_of_life` is `True` → `"compensate"`. This overrides everything else, no CVSS score
   or exploitation status changes this, because patching an end-of-life product is not possible.
2. Else if `exploited_in_wild` is `True` and `internet_facing` is `True` → `"emergency"`.
3. Else if `cvss >= 9.0` and `internet_facing` is `True` → `"emergency"`.
4. Else if `cvss >= 9.0` → `"scheduled"`.
5. Else if `cvss >= 7.0` and `internet_facing` is `True` → `"scheduled"`.
6. Else → `"routine"`.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network.
- Standard library only unless `blackbox.yaml: allow_deps` lists otherwise.
- CVSS thresholds are inclusive (`>=`), not strict.
- Input order is preserved in the output.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
