# Interface, 5.4.a-key-pairs (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry points
```python
def rsa_params(p: int, q: int) -> tuple
def is_valid_keypair(e: int, d: int, phi_n: int) -> bool
def solve(data: dict) -> dict
```

`solve()` is the blackbox entry point; `rsa_params()` and `is_valid_keypair()` are the
underlying primitives it's built on and are tested directly as well.

## Input
- `rsa_params(p, q)`: `p` and `q` are (small, distinct) prime integers.
- `is_valid_keypair(e, d, phi_n)`: `e`, `d`, `phi_n` are all `int`.
- `solve(data)`: `data` is a `dict` with `"op"` equal to `"params"` or `"validate"`.
  - `"params"`: `{"op": "params", "p": <int>, "q": <int>}`
  - `"validate"`: `{"op": "validate", "e": <int>, "d": <int>, "phi_n": <int>}`

## Output (`result`)
- `rsa_params(p, q)` returns a 2-tuple `(n, phi_n)` where `n = p * q` and
  `phi_n = (p - 1) * (q - 1)`.
- `is_valid_keypair(e, d, phi_n)` returns `bool`: `True` iff `(e * d) % phi_n == 1`.
- `solve(...)` returns `{"n": <int>, "phi_n": <int>}` for op `"params"`, or
  `{"valid": <bool>}` for op `"validate"`.

## Guarantees / rules
- Pure functions, deterministic, no I/O, no network. Standard library only, no external
  crypto/bignum libraries; this is the from-scratch pedagogical RSA-parameter math
  described in atom.md (n = p*q, phi(n) = (p-1)(q-1), e*d ≡ 1 mod phi(n)).
- Inputs are small, textbook-scale integers (not cryptographically secure primes); no
  primality checking is required inside `rsa_params`, callers are trusted to pass primes.
- `is_valid_keypair` must work for any nonnegative `e`, `d`, `phi_n` combination, including
  cases where the pair is deliberately invalid (used to test rejection).

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
