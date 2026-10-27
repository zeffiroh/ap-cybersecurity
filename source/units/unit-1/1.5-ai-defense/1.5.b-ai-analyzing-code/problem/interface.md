# Interface, 1.5.b-code-scanner (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(code: str) -> list[str]
```

## Input (`code`)
A single string containing Python source code to scan. May be multi-line. May be empty.

## Output (`result`)
A **sorted, de-duplicated** `list[str]` of vulnerability finding tags. Return `[]` if no
patterns are found.

## Pattern rule set (case-sensitive substring search unless noted)

| Tag returned                   | Trigger substring         | Vulnerability class                      |
|--------------------------------|--------------------------|------------------------------------------|
| `"vuln:eval"`                  | `eval(`                  | Code injection via eval                  |
| `"vuln:os_system"`             | `os.system(`             | OS command injection                     |
| `"vuln:subprocess_shell"`      | `shell=True`             | OS command injection via subprocess      |
| `"vuln:md5"`                   | `md5(`                   | Broken cryptographic hash (MD5)          |
| `"vuln:pickle_loads"`          | `pickle.loads(`          | Unsafe deserialization                   |
| `"vuln:hardcoded_password"`    | `password =`             | Hardcoded credential in source           |

Notes:
- `password =` matching is case-insensitive (matches `Password =`, `PASSWORD =`, etc.).
- All other patterns are case-sensitive (Python identifiers are case-sensitive).
- A single line may trigger multiple tags if multiple patterns are present.
- Comments are NOT excluded, a dangerous call inside a comment still triggers the tag.
  (In practice, AST-based tools skip comments; here we use substring scan for transparency.)

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Output always sorted ascending (lexicographic) and de-duplicated.
- `solve("")` returns `[]`.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
