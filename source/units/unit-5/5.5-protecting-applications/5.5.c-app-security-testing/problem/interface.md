# Interface, 5.5.c-sast-scanner (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(lines: list) -> list
```

## Input (`lines`)
`list[str]`, source-code lines, in file order (position 1 = first line, i.e. 1-indexed).

## Output (`result`)
`list[dict]`, each `{"line": int, "category": str}`, sorted by `line` ascending, then by
`category` ascending for findings on the same line. A single line may contribute more than one
finding if it matches more than one category.

## Categories
- `"sql-injection-risk"`, a SQL keyword (`SELECT`/`INSERT`/`UPDATE`/`DELETE`, case-insensitive)
  appears on a line that also builds the string dynamically (`+` concatenation, an f-string,
  `.format(`, or `%` formatting) rather than using a parameterized placeholder.
- `"eval-use"`, the line calls `eval(` or `exec(`.
- `"hardcoded-secret"`, the line assigns a quoted string literal to a variable whose name
  contains `password`, `secret`, `api_key`, or `token` (case-insensitive). An assignment that
  reads from an environment variable or config object (no literal string on the right-hand side)
  is NOT a finding.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Parameterized queries (e.g. `execute("... WHERE id = ?", (x))`) are NOT flagged.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
