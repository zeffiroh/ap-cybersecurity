# Coding problem, 5.4.c: Implement RSA digital signatures (hash-then-sign)

**Skill:** Mitigate Risk · **Maps to:** 5.4.B · **Language:** Python 3 (pytest)

## Problem
A software vendor wants to let users verify that a downloaded update really came from them and
was not modified in transit. Rather than signing the whole update file directly with RSA (slow,
and structurally risky per atom.md), implement the standard "hash, then sign" digital signature
scheme: hash the message with SHA-256, reduce the digest mod n, and apply the RSA private-key
operation to that digest, not the raw message.

## Function contract
Implement, in `starter.py`:
- `sign(message: bytes, d: int, n: int) -> int`, return the signature
  `(SHA-256(message) mod n)^d mod n`, using the signer's private exponent `d` and modulus `n`.
- `verify(message: bytes, signature: int, e: int, n: int) -> bool`, recompute
  `SHA-256(message) mod n` and compare it to `signature^e mod n`, using the signer's public
  exponent `e` and modulus `n`. Return `True` iff they match.
- `solve(data: dict) -> dict`, the blackbox entry point that dispatches to the two functions
  above (see `interface.md` / `blackbox.yaml`).

You may use `hashlib.sha256` for the hash step only. Implement the digest-reduction and the
modular exponentiation (`pow(base, exp, mod)` is fine, it's Python's built-in, not an external
crypto library) yourself, per the construction below.

## The construction
```
digest        = int.from_bytes(SHA256(message).digest(), "big") % n
sign:         signature = digest^d mod n
verify:       recovered = signature^e mod n     ; valid iff recovered == digest (recomputed)
```
- Hashing first keeps the signature a fixed size regardless of message length, and means a
  single changed byte in `message` produces a completely different digest (avalanche effect,
  5.3.b), which is what makes tampering detectable.
- `d` and `n` form the private key; `e` and `n` form the matching public key (5.4.b).

## Input / Output
- `sign(message, d, n)`: `message: bytes`, `d: int`, `n: int` -> `int` signature.
- `verify(message, signature, e, n)`: `signature: int`, `e: int`, `n: int` -> `bool`.
- `solve(data)`: `data = {"op": "sign", "message": "<str>", "d": <int>, "n": <int>}` ->
  `{"signature": <int>}`, or
  `data = {"op": "verify", "message": "<str>", "signature": <int>, "e": <int>, "n": <int>}` ->
  `{"valid": <bool>}`.

## Examples
Using the textbook-scale key pair `p=61, q=53 -> n=3233`, `e=17`, `d=2753`:
```
sign(b"pay Bob $50", 2753, 3233)        -> some int in [0, 3233)
verify(b"pay Bob $50", <that signature>, 17, 3233)   -> True
verify(b"pay Bob $950", <that signature>, 17, 3233)  -> False   # message tampered after signing
```

## Constraints
- Deterministic, offline, standard library only (`hashlib` only, no external crypto packages).
- Correctness is checked in `tests.py` against an independent oracle that recomputes the same
  hash-then-sign math directly (not by importing your functions).
- Must pass all cases in `tests.py` (visible + hidden), including: a tampered message failing
  verification, a wrong public key failing verification, an empty message, and determinism
  (signing the same message twice yields the same signature).

## How to run
```
cd problem && python -m pytest tests.py -q
```
