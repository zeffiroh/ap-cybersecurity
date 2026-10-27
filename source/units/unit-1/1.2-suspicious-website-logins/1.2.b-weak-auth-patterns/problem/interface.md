# Interface, 1.2.b-password-weakness-reporter (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(password: str) -> dict
```

## Input (`password`)
A single `str`, the candidate password. May be empty or contain any Unicode.

## Output (`result`)
A `dict` with exactly these keys:
- `"weak"` (`bool`), `True` if any rule below is triggered; `False` if all rules pass.
- `"reasons"` (`list[str]`), sorted list of triggered rule labels (see below). Empty if no rules triggered.

## Rules (all must be checked; collect all failures)

### Rule 1: `"too_short"`
Triggered when `len(password) < 12`.

### Rule 2: `"in_dictionary"`
Triggered when `password.lower()` is a member of the COMMON_WORDS set below.
```
COMMON_WORDS = {
    "password", "password1", "password123", "123456", "123456789", "12345678",
    "qwerty", "qwerty123", "letmein", "iloveyou", "admin", "welcome",
    "monkey", "dragon", "master", "abc123", "sunshine", "princess",
    "shadow", "superman", "football", "baseball", "login", "passw0rd",
    "pa$$word", "access", "mustang", "1234567890", "starwars", "hello",
}
```

### Rule 3: `"only_lowercase"`
Triggered when the password contains ONLY lowercase ASCII letters (`a`-`z`), i.e.,
`password.isalpha() and password == password.lower()`.
Note: an empty string does NOT trigger this rule (it has no lowercase letters either).

### Rule 4: `"sequential_or_repeated"`
Triggered when the password contains:
- A run of 3 or more consecutive ASCII characters in ascending order
  (e.g. `abc`, `bcd`, `xyz`, `123`, `234`, `789`), OR
- A run of 3 or more identical characters (e.g. `aaa`, `111`, `   `)

Detection algorithm:
For each window of 3 consecutive characters at position i:
- Repeated: `c[i] == c[i+1] == c[i+2]`
- Sequential ascending: `ord(c[i+1]) - ord(c[i]) == 1` AND `ord(c[i+2]) - ord(c[i+1]) == 1`

If any window matches either condition, the rule is triggered.

## Output contract
- `"reasons"` is always sorted ascending (alphabetical order of the label strings).
- `"weak"` equals `len(reasons) > 0`.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- The COMMON_WORDS set above is the exact set used by tests.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
