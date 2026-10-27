# Interface, 4.2.a-password-validator (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def validate_password(password: str, policy: dict) -> list[str]
```

## Input (`password`, `policy`)
- `password`, a string, the candidate password. May be empty.
- `policy`, a dict describing the policy. All keys are optional; a missing key is treated as
  "not required" / empty. Recognized keys and defaults:
  - `min_length` (int, default `0`), minimum required length.
  - `require_upper` (bool, default `False`), require at least one uppercase letter (`str.isupper()`).
  - `require_lower` (bool, default `False`), require at least one lowercase letter (`str.islower()`).
  - `require_digit` (bool, default `False`), require at least one digit (`str.isdigit()`).
  - `require_symbol` (bool, default `False`), require at least one character that is not
    alphanumeric (`not c.isalnum()`, e.g. `! @ # $ % - _ space`).
  - `banned_list` (list[str], default `[]`), forbidden/breached passwords. Matched
    case-insensitively against `password` (e.g. `"Password1"` matches a banned entry `"password1"`).
  - `history` (list[str], default `[]`), previously used passwords for this account. Matched
    case-sensitively, exact string equality, against `password`.

## Output (`result`)
A `list[str]` of violated rule names. Only rules that are actually violated appear in the list.
The list MUST be built by checking rules in this exact fixed order, and any violated rule name
is appended in that order (this order is part of the contract, tests assert exact list equality):

1. `"too_short"`, `len(password) < policy["min_length"]`
2. `"no_upper"`, `require_upper` is true and no character in `password` is uppercase
3. `"no_lower"`, `require_lower` is true and no character in `password` is lowercase
4. `"no_digit"`, `require_digit` is true and no character in `password` is a digit
5. `"no_symbol"`, `require_symbol` is true and no character in `password` is a non-alphanumeric symbol
6. `"in_banned_list"`, `password.lower()` equals (case-insensitively) any entry in `banned_list`
7. `"reused_password"`, `password` exactly matches (case-sensitive) any entry in `history`

If none of the above are violated, return `[]` (fully compliant password).

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- `policy` may omit any subset of keys; missing keys use the defaults above.
- An empty `password` (`""`) is valid input and is evaluated normally against the rules
  (it will violate `too_short` whenever `min_length > 0`, and any `require_*` rule that is on,
  since an empty string contains no uppercase/lowercase/digit/symbol characters).
- Rule checks are independent, a password can violate multiple rules simultaneously, and all
  violated rules are reported (not just the first).
- Returns a `list[str]`, never `None`, never a set or tuple.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
