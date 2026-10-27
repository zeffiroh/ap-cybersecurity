# Interface, 5.3.a-salted-hashing (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(action: str, password: str, param: str) -> Union[str, bool]
```

## Input
- `action`: A string, either `"hash"` or `"verify"`.
- `password`: A string, the plaintext password to hash or verify.
- `param`: 
  - If `action` is `"hash"`: this is the salt (string) to be prepended to the password.
  - If `action` is `"verify"`: this is the stored hash (string) of format `salt$digest` to verify against.

## Output
- If `action` is `"hash"`: returns `salt$digest` where `digest` is the hex-encoded SHA-256 hash of `salt + password`.
- If `action` is `"verify"`: returns a boolean (`True` if matches, `False` otherwise).

## Guarantees / rules
- Pure function, deterministic, no I/O, no network.
- Standard library only.
- Safe verification should use a constant-time comparison helper like `hmac.compare_digest`.
