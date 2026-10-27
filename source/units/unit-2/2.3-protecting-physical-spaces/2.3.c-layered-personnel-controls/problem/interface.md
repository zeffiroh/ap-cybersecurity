# Interface, 2.3.c-defense-in-depth-scorer (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(layers: list[dict]) -> dict
```

## Input (`layers`)
`list[dict]` where each dict has:
- `"name"`: `str`, free-text label for the layer (not used in scoring logic, informational only)
- `"category"`: `str`, one of the five valid categories `"perimeter"`, `"personnel"`,
  `"electronic"`, `"barrier"`, `"monitoring"`, or an invalid string that must be ignored.

## Output (`result`)
A `dict` with exactly these keys:
- `"depth_score"`: `int`, number of distinct valid categories present.
- `"categories_present"`: `list[str]`, sorted ascending, distinct valid categories present.
- `"redundant_categories"`: `dict[str, int]`, for each valid category with more than one layer,
  the count of layers *beyond the first* in that category. Categories with exactly one layer are
  not included. Categories with zero layers are not included.
- `"recommendation"`: `str`, `"STRONG"` if `depth_score >= 5`, `"ADEQUATE"` if `depth_score` is 3
  or 4, `"WEAK"` if `depth_score` is 0, 1, or 2.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- `layers` may be given in any order; category counts are order-independent.
- Invalid category strings (not one of the five valid categories) are ignored completely: they do
  not affect `depth_score`, `categories_present`, or `redundant_categories`.
- `categories_present` is always sorted ascending (alphabetical).

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
