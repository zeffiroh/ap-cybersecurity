# Coding problem, 5.4.d: Validate a certificate chain

**Skill:** Mitigate Risk · **Maps to:** 5.4.B, 5.4.C · **Language:** Python 3 (pytest)

## Problem
A browser has just received a TLS certificate chain from a server: a leaf (end-entity) certificate
and one or more issuing CA certificates, and it needs to decide whether to trust it. Real browsers
call into a full X.509 library to do this; you are going to implement the *validation logic itself*, the same logic that library runs under the hood, using the small-number RSA sign/verify math from
5.4.b/5.4.c.

Each certificate is a plain `dict`:
```python
{
  "subject": "www.meridianbank.example",     # who this certificate identifies
  "issuer": "Meridian Intermediate CA",       # who issued (signed) it
  "public_key": [17, 2501],                   # [e, n] -- this cert's own public key
  "signature": 1271,                          # issuer's signature over this cert's fields
  "not_before": 1000,                         # validity window, integer "time units"
  "not_after": 9000,
  "revoked": False,
}
```

A **chain** is a list of these dicts ordered leaf-first: `[leaf, intermediate..., root]`. The last
entry is claimed to be a root CA certificate (self-signed: its own `issuer` equals its own
`subject`).

## What you implement (in `starter.py`)
- `compute_digest(cert: dict) -> int`, a deterministic, keyless digest of a certificate's identity
  fields (everything except `signature` and `revoked`), used as the thing that actually gets signed.
  Canonicalize as the string
  `f"{subject}|{issuer}|{public_key[0]}:{public_key[1]}|{not_before}|{not_after}"`
  and reduce it with the rolling hash:
  ```python
  h = 0
  for ch in s:
      h = (h * 131 + ord(ch)) % (2**61 - 1)
  ```
- `rsa_sign(digest: int, d: int, n: int) -> int`, `signature = (digest mod n) ** d mod n`.
- `rsa_verify(digest: int, signature: int, e: int, n: int) -> bool`, return whether
  `signature ** e mod n == digest mod n`.
- `validate_chain(chain: list[dict], trusted_roots: dict[str, list[int]], current_time: int) -> dict`, validate the whole chain (see below). `trusted_roots` maps a trusted root CA's `subject` name to
  its known-good `[e, n]` public key (this is the browser's local trust store, never taken from the
  chain itself).
- `solve(data: dict) -> dict`, blackbox dispatcher (see `interface.md`).

## Validation algorithm
Walk the chain from the leaf (index 0) upward. For each certificate `cert` at index `i`:

1. **Validity window**, if `current_time < cert["not_before"]` or `current_time >
   cert["not_after"]` -> reason `"expired"`.
2. **Revocation**, if `cert["revoked"]` is `True` -> reason `"revoked"`.
3. **Chain linkage / signer's public key:**
   - If this is *not* the last certificate in the chain, the next certificate up (`chain[i+1]`) must
     be its issuer: `cert["issuer"] == chain[i+1]["subject"]`. If not -> reason `"broken_chain"`. The
     public key used to check this cert's signature is `chain[i+1]["public_key"]`.
   - If this *is* the last certificate in the chain, it must be a certificate for a root in
     `trusted_roots`: `cert["subject"]` must be a key in `trusted_roots`, and
     `trusted_roots[cert["subject"]]` must equal `cert["public_key"]` exactly. If either check fails
     -> reason `"untrusted_root"`. The public key used to check this cert's own (self-)signature is
     `trusted_roots[cert["subject"]]`.
4. **Signature check**, recompute `compute_digest(cert)` and check `rsa_verify(digest,
   cert["signature"], e, n)` using the public key established in step 3. If it fails -> reason
   `"bad_signature"`.

If every certificate in the chain passes all four checks, the chain is valid -> reason `"valid"`.
Stop at the *first* certificate (starting from the leaf) that fails any check and return that
specific reason -- do not keep scanning past a failure.

## Input / Output
- `validate_chain(chain, trusted_roots, current_time)` -> `{"valid": bool, "reason": str}` where
  `reason` is one of: `"valid"`, `"expired"`, `"revoked"`, `"broken_chain"`, `"untrusted_root"`,
  `"bad_signature"`.
- `solve(data)`: `data = {"op": "validate", "chain": [...], "trusted_roots": {...}, "current_time":
  int}` -> `validate_chain(...)`'s return dict directly. `data = {"op": "digest", "cert": {...}}` ->
  `{"digest": int}`.

## Examples
```
validate_chain([leaf, intermediate, root], {"Meridian Root CA": [17, 2773]}, 5000)
  -> {"valid": True, "reason": "valid"}

validate_chain([expired_leaf, intermediate, root], {"Meridian Root CA": [17, 2773]}, 9500)
  -> {"valid": False, "reason": "expired"}
```

## Constraints
- Deterministic, offline, standard library only. No `cryptography`, no `ssl`, no `hashlib` -- this
  is a from-scratch textbook-RSA exercise (same style as 5.4.b/5.4.c), not a real X.509 parser.
- `trusted_roots` is the only source of truth for which root keys are trusted -- a self-signed
  certificate whose subject is not in `trusted_roots` must be rejected as `"untrusted_root"`, even if
  its self-signature verifies correctly.
- Must pass all cases in `tests.py` (visible + hidden): a fully valid chain, an expired leaf, a
  revoked intermediate, a broken issuer/subject link, an untrusted (self-signed but unrecognized)
  root, and a tampered signature.

## How to run
```
cd problem && python -m pytest tests.py -q
```
