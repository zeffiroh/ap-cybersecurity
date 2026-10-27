"""Reference solution for 5.4.d. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml).

Implements X.509-style certificate chain validation directly (no cryptography/ssl libraries),
using the small-number textbook-RSA sign/verify math from 5.4.b/5.4.c as the signature primitive.
"""
from typing import Any

_MODULUS = (2 ** 61) - 1  # large Mersenne prime used only to bound the rolling hash


def compute_digest(cert: dict) -> int:
    """Deterministic, keyless digest of a certificate's identity fields (everything except
    'signature' and 'revoked' -- those aren't part of what gets signed)."""
    e, n = cert["public_key"]
    canonical = f'{cert["subject"]}|{cert["issuer"]}|{e}:{n}|{cert["not_before"]}|{cert["not_after"]}'
    h = 0
    for ch in canonical:
        h = (h * 131 + ord(ch)) % _MODULUS
    return h


def rsa_sign(digest: int, d: int, n: int) -> int:
    """signature = (digest mod n) ** d mod n, using the issuer's private exponent d."""
    return pow(digest % n, d, n)


def rsa_verify(digest: int, signature: int, e: int, n: int) -> bool:
    """True iff signature ** e mod n recovers digest mod n, using the issuer's public key (e, n)."""
    return pow(signature, e, n) == digest % n


def validate_chain(chain: list, trusted_roots: dict, current_time: int) -> dict:
    """Validate a leaf-first certificate chain against a local trust store.

    Walks leaf -> root, checking (in order, per certificate) validity window, revocation,
    issuer/subject linkage (or trusted-root membership at the top), and signature. Returns the
    first failure encountered, or {"valid": True, "reason": "valid"} if the whole chain checks out.
    """
    for i, cert in enumerate(chain):
        if current_time < cert["not_before"] or current_time > cert["not_after"]:
            return {"valid": False, "reason": "expired"}

        if cert.get("revoked", False):
            return {"valid": False, "reason": "revoked"}

        if i + 1 < len(chain):
            issuer_cert = chain[i + 1]
            if cert["issuer"] != issuer_cert["subject"]:
                return {"valid": False, "reason": "broken_chain"}
            issuer_pubkey = issuer_cert["public_key"]
        else:
            root_key = trusted_roots.get(cert["subject"])
            if root_key is None or list(root_key) != list(cert["public_key"]):
                return {"valid": False, "reason": "untrusted_root"}
            issuer_pubkey = root_key

        digest = compute_digest(cert)
        e, n = issuer_pubkey
        if not rsa_verify(digest, cert["signature"], e, n):
            return {"valid": False, "reason": "bad_signature"}

    return {"valid": True, "reason": "valid"}


def solve(data: Any) -> Any:
    """Blackbox entry point. Dispatches on data['op']:
      - {"op": "validate", "chain": [...], "trusted_roots": {...}, "current_time": int}
            -> validate_chain(...)'s result dict
      - {"op": "digest", "cert": {...}}
            -> {"digest": int}
    """
    op = data["op"]
    if op == "validate":
        return validate_chain(data["chain"], data["trusted_roots"], data["current_time"])
    elif op == "digest":
        return {"digest": compute_digest(data["cert"])}
    else:
        raise ValueError(f"unknown op: {op!r}")
