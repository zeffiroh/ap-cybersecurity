# Coding problem, 5.5.c: Static-analysis scanner (SAST)

**Skill:** Detect Attacks, Mitigate Risk · **Maps to:** 5.5.B, 5.5.C · **Language:** Python 3 (pytest)

## Problem
Build a miniature SAST rule engine. Given the source lines of a file (as a list of strings, one
per line, 1-indexed), scan each line for known dangerous patterns and return a list of findings, exactly what a real static-analysis tool's rule engine does before a human triages the results.

Detect these categories:
- `"sql-injection-risk"`, a SQL keyword (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) combined with
  string concatenation (`+`) or an f-string/`.format(`/`%` on the same line (i.e., the query is
  being built dynamically instead of parameterized).
- `"eval-use"`, the line calls `eval(` or `exec(`.
- `"hardcoded-secret"`, the line assigns a literal string to a variable whose name contains
  `password`, `secret`, `api_key`, or `token` (case-insensitive), e.g. `password = "hunter2"`.
  An assignment that reads from an environment variable or config object (no literal string on the
  right-hand side) is NOT a finding.

## Function contract
Implement `solve(lines: list) -> list` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
- `lines`: `list[str]`, source code lines, in file order. Line numbers are 1-indexed (the first
  element of the list is line 1).

## Output
A `list[dict]`, each `{"line": int, "category": str}`, **sorted by line number ascending**, then by
category name ascending for findings on the same line. If a line matches more than one category,
emit one finding per matching category. If no lines match, return `[]`.

## Examples
```
lines = [
  'query = "SELECT * FROM users WHERE name = \'" + user_input + "\'"',
  'password = "hunter2"',
  'eval(user_expr)',
]
solve(lines) -> [
  {"line": 1, "category": "sql-injection-risk"},
  {"line": 2, "category": "hardcoded-secret"},
  {"line": 3, "category": "eval-use"},
]
```

```
lines = ['password = os.environ["DB_PASSWORD"]', 'db.query(stmt, params)']
solve(lines) -> []
```

## Constraints
- Deterministic, offline, standard library only.
- Findings are sorted by `line`, then `category` (both ascending).
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
