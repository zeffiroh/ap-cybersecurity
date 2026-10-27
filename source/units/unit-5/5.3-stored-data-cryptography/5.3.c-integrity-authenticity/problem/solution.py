"""Reference solution for 5.3.c. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml).

Implements the FIPS 198-1 HMAC construction by hand (ipad/opad nesting) on top of
hashlib.sha256, used only as the inner H() step. Crypto problems implement the underlying math/logic directly rather than calling hmac.*.
"""
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
    if len(key) > BLOCK_SIZE:
        key = _h(key)
    return key + b"\x00" * (BLOCK_SIZE - len(key))


def _xor_bytes(data: bytes, pad: int) -> bytes:
    return bytes(b ^ pad for b in data)


def hmac_sha256(key: bytes, message: bytes) -> str:
    """Compute HMAC-SHA256(key, message) and return the tag as a lowercase hex string.

    HMAC(key, message) = H( (key XOR opad) || H( (key XOR ipad) || message ) )
    """
    k0 = _derive_key(key)
    inner_key = _xor_bytes(k0, IPAD)
    outer_key = _xor_bytes(k0, OPAD)
    inner_hash = _h(inner_key + message)
    tag = _h(outer_key + inner_hash)
    return tag.hex()


def _constant_time_equal(a: str, b: str) -> bool:
    """Compare two equal-or-unequal-length strings without short-circuiting on the
    first mismatch, to avoid leaking timing information about where tags differ."""
    if len(a) != len(b):
        return False
    result = 0
    for ca, cb in zip(a, b):
        result |= ord(ca) ^ ord(cb)
    return result == 0


def verify(key: bytes, message: bytes, tag: str) -> bool:
    """Return True iff `tag` is the correct HMAC-SHA256 tag for (key, message)."""
    expected = hmac_sha256(key, message)
    return _constant_time_equal(expected, tag.lower())


def solve(data: dict) -> dict:
    """Blackbox entry point. Dispatches on data['op']:
      - {"op": "tag", "key": <hex str>, "message": <str>}
            -> {"tag": <hex str>}
      - {"op": "verify", "key": <hex str>, "message": <str>, "tag": <hex str>}
            -> {"valid": <bool>}
    Keys and messages are given as UTF-8 strings; `key` is provided as a hex string
    to allow arbitrary binary-looking keys through a JSON-friendly interface.
    """
    op = data["op"]
    key = bytes.fromhex(data["key"])
    message = data["message"].encode("utf-8")
    if op == "tag":
        return {"tag": hmac_sha256(key, message)}
    elif op == "verify":
        return {"valid": verify(key, message, data["tag"])}
    else:
        raise ValueError(f"unknown op: {op!r}")
