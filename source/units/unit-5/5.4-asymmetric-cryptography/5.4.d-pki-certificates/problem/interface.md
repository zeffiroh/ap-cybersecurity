# Interface, 5.4.d-cert-chain-validation (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry points
```python
def compute_digest(cert: dict) -> int
def rsa_sign(digest: int, d: int, n: int) -> int
def rsa_verify(digest: int, signature: int, e: int, n: int) -> bool
def validate_chain(chain: list, trusted_roots: dict, current_time: int) -> dict
def solve(data: dict) -> dict
```

`solve()` is the blackbox entry point; the other functions are the underlying primitives it is
built on and are tested directly as well.

## Input
- `compute_digest(cert)`: `cert` is a `dict` with keys `subject` (`str`), `issuer` (`str`),
  `public_key` (`[e, n]` list of two `int`), `not_before` (`int`), `not_after` (`int`). (`signature`
  and `revoked` may also be present but are not part of the digest.)
- `rsa_sign(digest, d, n)` / `rsa_verify(digest, signature, e, n)`: all `int`.
- `validate_chain(chain, trusted_roots, current_time)`:
  - `chain`: `list[dict]`, leaf-first, each dict shaped like `cert` above plus `signature` (`int`,
    the issuer's signature over `compute_digest(cert)`) and `revoked` (`bool`).
  - `trusted_roots`: `dict[str, list[int]]` mapping a trusted root CA's `subject` name to its known
    `[e, n]` public key (the local trust store).
  - `current_time`: `int`.
- `solve(data)`: `data` is a `dict` with `"op"` equal to `"validate"` or `"digest"`.
  - `"validate"`: `{"op": "validate", "chain": [...], "trusted_roots": {...}, "current_time": int}`
  - `"digest"`: `{"op": "digest", "cert": {...}}`

## Output (`result`)
- `compute_digest(...)` returns an `int`.
- `rsa_sign(...)` returns an `int`.
- `rsa_verify(...)` returns `bool`.
- `validate_chain(...)` returns `{"valid": bool, "reason": str}`, where `reason` is one of
  `"valid"`, `"expired"`, `"revoked"`, `"broken_chain"`, `"untrusted_root"`, `"bad_signature"`.
- `solve(...)` returns `validate_chain(...)`'s dict for op `"validate"`, or `{"digest": int}` for op
  `"digest"`.

## Guarantees / rules
- Pure functions, deterministic, no I/O, no network. Standard library only -- no `cryptography`,
  `ssl`, or `hashlib`; this is a from-scratch textbook-RSA exercise, not a real X.509 parser.
- `compute_digest` canonicalizes as
  `f"{subject}|{issuer}|{e}:{n}|{not_before}|{not_after}"` and reduces with the rolling hash
  `h = (h * 131 + ord(ch)) % (2**61 - 1)` over every character.
- `validate_chain` walks the chain leaf-first (index 0) to root (last index) and, for each
  certificate, checks in this order: validity window, revocation, issuer/subject chain linkage
  (or trusted-root membership for the last certificate), then signature -- returning the first
  failure encountered.
- The public key used to verify a non-root certificate's signature is always the *next*
  certificate's `public_key`, never the certificate's own key. The public key used to verify the
  root's self-signature is always looked up from `trusted_roots`, never trusted from the chain data
  itself.
- A self-signed certificate whose subject is absent from `trusted_roots` is `"untrusted_root"`, even
  if its own signature verifies correctly.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
