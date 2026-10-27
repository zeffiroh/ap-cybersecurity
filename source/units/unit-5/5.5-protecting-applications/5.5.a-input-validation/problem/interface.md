# Interface, 5.5.a-field-validator (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(submissions: list) -> list
```

## Input (`submissions`)
`list[dict]`, each `{"field": str, "type": str, "value": str}`. `type` is one of `"zip"`,
`"email"`, `"quantity"`, `"username"`.

## Output (`result`)
`list[str]`, the `value` of every submission that is **BLOCKED**, in the same order as the
input. A submission is blocked if either condition holds:
1. Its `value` fails the allowlist pattern for its `type` (server-side shape check).
2. Its `value` matches a known injection meta-character/keyword signature (checked
   independently of `type`, a value can match the type's shape and still be blocked).

## Allowlist rules
- `zip`: exactly 5 digits.
- `email`: `local@domain.tld` shape (letters/digits/`._+-` local part, dotted domain).
- `quantity`: integer string from `1` to `99` inclusive (no leading zero, no `0`, no `100+`).
- `username`: 3-20 characters, letters/digits/underscore only.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Injection signatures include (case-insensitive): `--`, `;`, `<script`, `UNION SELECT`,
  `OR 1=1`, `' OR '`, `DROP TABLE`, `../` path traversal, and URL-encoded `%3B`/`%2F`.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
