# Interface, 1.3.a-adversary-classifier (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(adversary: dict) -> str
```

## Input (`adversary`)
A dict describing one adversary. Keys and types:

| Key | Type | Description |
|-----|------|-------------|
| `uses_zero_day` | bool | Does the adversary exploit an unpublished vulnerability? |
| `custom_tooling` | bool | Does the adversary write or substantially modify their own tools? |
| `targets_specific_victim` | bool | Does the adversary select a specific high-value target? |
| `off_the_shelf_only` | bool | Does the adversary rely solely on public tools without modification? |
| `adapts_to_defenses` | bool | Does the adversary change tactics when initial attempts fail? |

All five keys are always present and are booleans.

## Output (`result`)
A single string: either `"low"` or `"high"`.

## Classification rules (deterministic)
Apply in order; first matching rule wins:

1. If `uses_zero_day` is `True` OR `custom_tooling` is `True` -> return `"high"`.
2. If `targets_specific_victim` is `True` AND `adapts_to_defenses` is `True` -> return `"high"`.
3. Otherwise -> return `"low"`.

Rationale: zero-day capability and custom tooling are unambiguous high-skill markers. An adversary
that both selects specific targets AND adapts to defenses exhibits sustained, directed capability
that also places them in the high tier.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Input dict always contains exactly the five keys listed above.
- Output is always exactly the string `"low"` or `"high"` (lowercase).

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
