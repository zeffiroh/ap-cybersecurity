# Interface, 5.1.a-parameterized-login

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def authenticate(users: list[tuple[str, str, str]], username: str, password: str) -> str | None
```

## Input
- `users`: a list of `(username, role, password)` rows to load into an in-memory table.
- `username`, `password`: the submitted login credentials (untrusted input).

## Output
- The matching user's `role` (a string) when a row's username AND password both equal the
  submitted values.
- `None` when no row matches, including every injection attempt.

## Guarantees / rules
- Deterministic, no network. Standard library only (`sqlite3`).
- The username/password comparison must be performed **by a SQL query**, using a
  parameterized statement with `?` placeholders and the values bound separately.
- No input filtering, blocklisting, or Python-side list comparison.

## Acceptance
`python -m pytest tests.py -q` passes, including the injection cases, which succeed only when
the query is parameterized rather than built by string concatenation.
