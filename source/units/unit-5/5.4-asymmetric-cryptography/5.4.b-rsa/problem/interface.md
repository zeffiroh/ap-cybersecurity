# Interface, 5.4.b-rsa-encrypt-decrypt (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry points
```python
def egcd(a: int, b: int) -> tuple[int, int, int]
def mod_inverse(e: int, phi_n: int) -> int
def rsa_keygen(p: int, q: int, e: int) -> dict
def encrypt(m: int, e: int, n: int) -> int
def decrypt(c: int, d: int, n: int) -> int
def solve(data: dict) -> dict
```

`solve()` is the blackbox entry point; the other functions are the underlying primitives it is
built on and are tested directly as well.

## Input
- `egcd(a, b)`: non-negative integers.
- `mod_inverse(e, phi_n)`: `e` and `phi_n` are positive integers.
- `rsa_keygen(p, q, e)`: `p`, `q` are prime integers; `e` is the candidate public exponent.
- `encrypt(m, e, n)`: `m`, `e`, `n` are non-negative integers; `m` must satisfy `0 <= m < n`.
- `decrypt(c, d, n)`: `c`, `d`, `n` are non-negative integers.
- `solve(data)`: `data` is a `dict` with `"op"` equal to one of `"keygen"`, `"encrypt"`,
  `"decrypt"`, `"roundtrip"`.
  - `"keygen"`: `{"op": "keygen", "p": int, "q": int, "e": int}`
  - `"encrypt"`: `{"op": "encrypt", "m": int, "e": int, "n": int}`
  - `"decrypt"`: `{"op": "decrypt", "c": int, "d": int, "n": int}`
  - `"roundtrip"`: `{"op": "roundtrip", "p": int, "q": int, "e": int, "m": int}`

## Output (`result`)
- `egcd(a, b)` returns `(g, x, y)` with `a*x + b*y == g == gcd(a, b)`.
- `mod_inverse(e, phi_n)` returns the integer `d` with `(e * d) % phi_n == 1`.
- `rsa_keygen(p, q, e)` returns `{"n": int, "phi_n": int, "e": int, "d": int}`.
- `encrypt(m, e, n)` returns the ciphertext `int` (`m^e mod n`).
- `decrypt(c, d, n)` returns the plaintext `int` (`c^d mod n`).
- `solve(...)` returns:
  - `"keygen"` -> `{"n": int, "phi_n": int, "e": int, "d": int}`
  - `"encrypt"` -> `{"c": int}`
  - `"decrypt"` -> `{"m": int}`
  - `"roundtrip"` -> `{"n": int, "phi_n": int, "d": int, "c": int, "m_decrypted": int}`

## Guarantees / rules
- Pure functions, deterministic, no I/O, no network. Standard library only (`pow()` may be used
  for modular exponentiation; the extended Euclidean algorithm must be implemented directly, not
  imported from a crypto library).
- `mod_inverse` and `rsa_keygen` raise `ValueError` when no valid inverse/exponent exists
  (`gcd(e, phi_n) != 1`, or `e` outside `1 < e < phi_n`).
- `encrypt` raises `ValueError` when `m` is not in `0 <= m < n`.
- For any valid key pair, `decrypt(encrypt(m, e, n), d, n) == m` for every `m` in `0 <= m < n`.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
