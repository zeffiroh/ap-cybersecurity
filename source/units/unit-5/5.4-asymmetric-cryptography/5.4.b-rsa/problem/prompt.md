# Coding problem, 5.4.b: RSA algorithm

**Skill:** Mitigate Risk · **Maps to:** 5.4.A, 5.4.B · **Language:** Python 3 (pytest)

## Problem
A small internal tool needs to demonstrate RSA end to end on textbook-scale numbers: derive a
key pair from two primes and a chosen public exponent, encrypt a small integer message with the
public key, and decrypt it back with the private key. Implement the key derivation and the
modular-exponentiation encrypt/decrypt operations directly, you may use Python's built-in
`pow(base, exp, mod)` for the modular exponentiation itself, but the extended Euclidean
algorithm used to derive the private exponent `d` must be implemented by hand.

## Function contract
Implement, in `starter.py`:
- `egcd(a: int, b: int) -> tuple[int, int, int]`, extended Euclidean algorithm; returns
  `(g, x, y)` such that `a*x + b*y == g == gcd(a, b)`.
- `mod_inverse(e: int, phi_n: int) -> int`, the modular inverse `d` of `e` mod `phi_n`, i.e.
  `(e * d) % phi_n == 1`. Raises `ValueError` if no inverse exists (`gcd(e, phi_n) != 1`).
- `rsa_keygen(p: int, q: int, e: int) -> dict`, derives `n`, `phi_n`, and `d` from primes `p`,
  `q` and public exponent `e`. Returns `{"n": n, "phi_n": phi_n, "e": e, "d": d}`. Raises
  `ValueError` if `e` does not satisfy `1 < e < phi_n`.
- `encrypt(m: int, e: int, n: int) -> int`, RSA encrypt: `c = m^e mod n`. Raises `ValueError`
  if `m` is not in `0 <= m < n`.
- `decrypt(c: int, d: int, n: int) -> int`, RSA decrypt: `m = c^d mod n`.
- `solve(data: dict) -> dict`, the blackbox entry point that dispatches to the functions above
  (see `interface.md` / `blackbox.yaml`).

## Input / Output
- `rsa_keygen(p, q, e)`: `p`, `q` are (small, in this atom's tests) prime integers; `e` is the
  chosen public exponent -> `{"n": int, "phi_n": int, "e": int, "d": int}`.
- `encrypt(m, e, n)`: `m: int`, `e: int`, `n: int` -> ciphertext `int`.
- `decrypt(c, d, n)`: `c: int`, `d: int`, `n: int` -> plaintext `int`.
- `solve(data)`:
  - `{"op": "keygen", "p": int, "q": int, "e": int}` -> `{"n": int, "phi_n": int, "e": int, "d": int}`
  - `{"op": "encrypt", "m": int, "e": int, "n": int}` -> `{"c": int}`
  - `{"op": "decrypt", "c": int, "d": int, "n": int}` -> `{"m": int}`
  - `{"op": "roundtrip", "p": int, "q": int, "e": int, "m": int}` ->
    `{"n": int, "phi_n": int, "d": int, "c": int, "m_decrypted": int}`

## Examples
```
rsa_keygen(3, 11, 7)          -> {"n": 33, "phi_n": 20, "e": 7, "d": 3}
encrypt(5, 7, 33)             -> 14
decrypt(14, 3, 33)            -> 5

solve({"op": "roundtrip", "p": 3, "q": 11, "e": 7, "m": 5})
  -> {"n": 33, "phi_n": 20, "d": 3, "c": 14, "m_decrypted": 5}
```

## Constraints
- Deterministic, offline, standard library only (`pow()` for modular exponentiation is allowed
  and expected; do not import any external crypto library, the extended Euclidean algorithm
  and key derivation must be your own code).
- Must pass all cases in `tests.py` (visible + hidden), including edge cases such as `m = 0`,
  `m` at or beyond `n` (rejected), and `e` values that are not coprime with `phi_n` (rejected).

## How to run
```
cd problem && python -m pytest tests.py -q
```
