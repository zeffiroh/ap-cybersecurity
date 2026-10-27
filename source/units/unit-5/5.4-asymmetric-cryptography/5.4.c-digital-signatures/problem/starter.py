"""Starter code for 5.4.c. Student completes the TODOs.
This file intentionally FAILS the tests until implemented."""
import hashlib


def _digest_mod_n(message: bytes, n: int) -> int:
    """Hash message with SHA-256 and reduce it to an integer mod n.

    This is the 'hash, then sign' step from atom.md: we never run RSA on the raw
    message, only on a fixed-size digest of it.
    """
    # TODO: compute hashlib.sha256(message).digest(), convert it to an int with
    #       int.from_bytes(..., "big"), and reduce it mod n.
    raise NotImplementedError("implement _digest_mod_n() — see prompt.md")


def sign(message: bytes, d: int, n: int) -> int:
    """Sign `message` with private exponent d and modulus n.

    signature = hash(message)^d mod n
    """
    # TODO: compute the digest with _digest_mod_n(), then return pow(digest, d, n).
    raise NotImplementedError("implement sign() — see prompt.md")


def verify(message: bytes, signature: int, e: int, n: int) -> bool:
    """Verify that `signature` is a valid signature over `message` under public
    key (e, n).

    Recomputes hash(message) mod n and compares it to signature^e mod n.
    """
    # TODO: recompute the expected digest with _digest_mod_n(), recover the digest
    #       the signer actually signed with pow(signature, e, n), and compare them.
    raise NotImplementedError("implement verify() — see prompt.md")


def solve(data: dict) -> dict:
    """Blackbox entry point. Dispatches on data['op']:
      - {"op": "sign", "message": <str>, "d": <int>, "n": <int>}
            -> {"signature": <int>}
      - {"op": "verify", "message": <str>, "signature": <int>, "e": <int>, "n": <int>}
            -> {"valid": <bool>}
    Messages are given as UTF-8 strings; d/e/n/signature are given as ints (small,
    textbook-scale RSA parameters — JSON-friendly, no hex/bignum encoding needed).
    """
    # TODO: encode data["message"] as utf-8, then dispatch to sign() or verify()
    #       depending on data["op"], and wrap the result in the right dict shape.
    raise NotImplementedError("implement solve() — see prompt.md")
