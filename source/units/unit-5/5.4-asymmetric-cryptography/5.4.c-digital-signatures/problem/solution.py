"""Reference solution for 5.4.c. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml).

Implements textbook RSA "hash-then-sign" digital signatures by hand: the digest is
computed with hashlib.sha256 (stdlib), reduced mod n, and the RSA private/public-key
operation (modular exponentiation) is implemented directly with Python's built-in
pow(base, exp, mod) rather than any external crypto library.
Crypto problems implement the underlying math/logic directly.
"""
import hashlib


def _digest_mod_n(message: bytes, n: int) -> int:
    """Hash message with SHA-256 and reduce it to an integer mod n.

    This is the 'hash, then sign' step from atom.md: we never run RSA on the raw
    message, only on a fixed-size digest of it.
    """
    digest_bytes = hashlib.sha256(message).digest()
    digest_int = int.from_bytes(digest_bytes, "big")
    return digest_int % n


def sign(message: bytes, d: int, n: int) -> int:
    """Sign `message` with private exponent d and modulus n.

    signature = hash(message)^d mod n
    """
    digest = _digest_mod_n(message, n)
    return pow(digest, d, n)


def verify(message: bytes, signature: int, e: int, n: int) -> bool:
    """Verify that `signature` is a valid signature over `message` under public
    key (e, n).

    Recomputes hash(message) mod n and compares it to signature^e mod n.
    """
    expected_digest = _digest_mod_n(message, n)
    recovered_digest = pow(signature, e, n)
    return expected_digest == recovered_digest


def solve(data: dict) -> dict:
    """Blackbox entry point. Dispatches on data['op']:
      - {"op": "sign", "message": <str>, "d": <int>, "n": <int>}
            -> {"signature": <int>}
      - {"op": "verify", "message": <str>, "signature": <int>, "e": <int>, "n": <int>}
            -> {"valid": <bool>}
    Messages are given as UTF-8 strings; d/e/n/signature are given as ints (small,
    textbook-scale RSA parameters — JSON-friendly, no hex/bignum encoding needed).
    """
    op = data["op"]
    message = data["message"].encode("utf-8")
    if op == "sign":
        signature = sign(message, data["d"], data["n"])
        return {"signature": signature}
    elif op == "verify":
        valid = verify(message, data["signature"], data["e"], data["n"])
        return {"valid": valid}
    else:
        raise ValueError(f"unknown op: {op!r}")
