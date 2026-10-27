"""Starter code for 5.3.c. Student completes the TODOs.
This file intentionally FAILS the tests until implemented."""
import hashlib

BLOCK_SIZE = 64  # SHA-256 block size in bytes
IPAD = 0x36
OPAD = 0x5C


def _h(data: bytes) -> bytes:
    """The inner hash primitive H(). Only stdlib hashlib.sha256 is used here."""
    return hashlib.sha256(data).digest()


def _derive_key(key: bytes) -> bytes:
    """Normalize key to exactly BLOCK_SIZE bytes per FIPS 198-1:
    hash keys longer than the block size, right-pad shorter keys with zero bytes."""
    # TODO: if key is longer than BLOCK_SIZE, replace it with _h(key).
    #       Then right-pad with zero bytes (b"\\x00") up to BLOCK_SIZE.
    raise NotImplementedError("implement _derive_key() — see prompt.md")


def _xor_bytes(data: bytes, pad: int) -> bytes:
    # TODO: XOR every byte of `data` with the int `pad`; return as bytes.
    raise NotImplementedError("implement _xor_bytes() — see prompt.md")


def hmac_sha256(key: bytes, message: bytes) -> str:
    """Compute HMAC-SHA256(key, message) and return the tag as a lowercase hex string.

    HMAC(key, message) = H( (key XOR opad) || H( (key XOR ipad) || message ) )
    """
    # TODO: derive k0 with _derive_key(key); build inner_key = k0 XOR ipad and
    #       outer_key = k0 XOR opad; compute inner_hash = H(inner_key || message);
    #       return H(outer_key || inner_hash) as a hex string.
    raise NotImplementedError("implement hmac_sha256() — see prompt.md")


def _constant_time_equal(a: str, b: str) -> bool:
    """Compare two equal-or-unequal-length strings without short-circuiting on the
    first mismatch, to avoid leaking timing information about where tags differ."""
    # TODO: return False immediately if lengths differ. Otherwise OR together the
    #       XOR of every character pair and return whether the total is zero.
    raise NotImplementedError("implement _constant_time_equal() — see prompt.md")


def verify(key: bytes, message: bytes, tag: str) -> bool:
    """Return True iff `tag` is the correct HMAC-SHA256 tag for (key, message)."""
    # TODO: recompute the expected tag and compare using _constant_time_equal().
    raise NotImplementedError("implement verify() — see prompt.md")


def solve(data: dict) -> dict:
    """Blackbox entry point. Dispatches on data['op']:
      - {"op": "tag", "key": <hex str>, "message": <str>}
            -> {"tag": <hex str>}
      - {"op": "verify", "key": <hex str>, "message": <str>, "tag": <hex str>}
            -> {"valid": <bool>}
    Keys and messages are given as UTF-8 strings; `key` is provided as a hex string
    to allow arbitrary binary-looking keys through a JSON-friendly interface.
    """
    # TODO: decode data["key"] with bytes.fromhex, encode data["message"] as utf-8,
    #       then dispatch to hmac_sha256() or verify() depending on data["op"].
    raise NotImplementedError("implement solve() — see prompt.md")
