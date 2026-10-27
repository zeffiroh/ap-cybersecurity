# Interface, 5.4.c-rsa-digital-signatures (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry points
```python
def sign(message: bytes, d: int, n: int) -> int
def verify(message: bytes, signature: int, e: int, n: int) -> bool
def solve(data: dict) -> dict
```

`solve()` is the blackbox entry point; `sign()` and `verify()` are the underlying primitives
it's built on and are tested directly as well.

## Input
- `sign(message, d, n)`: `message` is raw `bytes` of any length (including empty); `d` is the
  signer's private exponent; `n` is the RSA modulus (both small, textbook-scale ints).
- `verify(message, signature, e, n)`: `message` as above; `signature` is the claimed signature
  (`int`); `e` is the public exponent; `n` is the modulus that must match the key pair used to
  sign (verifying with a different `n`/`e` pair must fail).
- `solve(data)`: `data` is a `dict` with `"op"` equal to `"sign"` or `"verify"`.
  - `"sign"`: `{"op": "sign", "message": <str>, "d": <int>, "n": <int>}`
  - `"verify"`: `{"op": "verify", "message": <str>, "signature": <int>, "e": <int>, "n": <int>}`
  - `message` arrives as a plain UTF-8 string (encode with `.encode("utf-8")`).

## Output (`result`)
- `sign(...)` returns an `int` signature in the range `[0, n)`.
- `verify(...)` returns `bool`.
- `solve(...)` returns `{"signature": <int>}` for op `"sign"`, or `{"valid": <bool>}` for op
  `"verify"`.

## Guarantees / rules
- Pure functions, deterministic, no I/O, no network. Standard library only (`hashlib.sha256`
  may be used as the hash primitive; the RSA sign/verify math itself, reducing the digest mod
  `n` and using modular exponentiation, e.g. Python's built-in `pow(base, exp, mod)`, must be
  implemented directly, not via any external crypto library).
- Must implement "hash, then sign": `signature = (SHA-256(message) mod n)^d mod n`; verification
  recomputes `SHA-256(message) mod n` and compares it to `signature^e mod n`.
- Any single-bit change to `message` must (with overwhelming probability) produce a different
  signature, and verification against the original signature must then fail.
- Verifying a genuine `(message, signature)` pair with an unrelated key pair's public key
  `(e, n)` must return `False`.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
