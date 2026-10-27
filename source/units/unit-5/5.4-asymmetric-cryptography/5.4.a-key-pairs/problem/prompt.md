# Coding problem, 5.4.a: RSA key-pair parameters

**Skill:** Mitigate Risk · **Maps to:** 5.4.A · **Language:** Python 3 (pytest)

## Problem
Before RSA can encrypt or sign anything, it needs a key pair. Given two prime numbers p
and q, implement the first steps of RSA key generation described in `atom.md`: compute
the modulus n, compute phi(n), and validate whether a proposed public/private exponent
pair (e, d) actually satisfies the required mathematical relationship.

## Function contract
Implement, in `starter.py`:
- `rsa_params(p: int, q: int) -> tuple`, given two (small, distinct) primes, return
  `(n, phi_n)` where `n = p * q` and `phi_n = (p - 1) * (q - 1)`.
- `is_valid_keypair(e: int, d: int, phi_n: int) -> bool`, return `True` iff
  `(e * d) % phi_n == 1`, i.e. d is the modular inverse of e mod phi_n.
- `solve(data: dict) -> dict`, the blackbox entry point that dispatches to the two
  functions above (see `interface.md` / `blackbox.yaml`).

## The math (see atom.md)
```
n       = p * q
phi(n)  = (p - 1) * (q - 1)
valid keypair (e, d)  <=>  (e * d) mod phi(n) == 1
```
The public key is `(e, n)`; the private key is `(d, n)`. Both share `n`, but `d` cannot
be recovered from `e` and `n` alone without knowing `phi(n)` (which requires factoring
`n` back into `p` and `q`).

## Input / Output
- `rsa_params(p, q)`: `p, q: int` (primes) -> `(n, phi_n)` tuple of `int`.
- `is_valid_keypair(e, d, phi_n)`: all `int` -> `bool`.
- `solve(data)`: `data = {"op": "params", "p": <int>, "q": <int>}` ->
  `{"n": <int>, "phi_n": <int>}`, or
  `data = {"op": "validate", "e": <int>, "d": <int>, "phi_n": <int>}` ->
  `{"valid": <bool>}`.

## Examples
```
rsa_params(3, 11)  -> (33, 20)     # n = 3*11 = 33, phi(n) = 2*10 = 20
rsa_params(5, 11)  -> (55, 40)     # n = 5*11 = 55, phi(n) = 4*10 = 40

is_valid_keypair(e=3, d=7, phi_n=20)  -> True   # 3*7 = 21, 21 % 20 == 1
is_valid_keypair(e=3, d=6, phi_n=20)  -> False  # 3*6 = 18, 18 % 20 != 1
```

## Constraints
- Deterministic, offline, standard library only. No external crypto/bignum libraries, this problem implements the underlying arithmetic directly.
- Inputs are small, textbook-scale integers as in the atom's worked examples; no
  primality checking is required.
- Must pass all cases in `tests.py` (visible + hidden), including the p=3,q=11 and
  p=5,q=11 examples from `atom.md`, and both valid and invalid keypair checks.

## How to run
```
cd problem && python -m pytest tests.py -q
```
