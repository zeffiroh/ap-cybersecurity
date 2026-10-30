import hashlib

BLOCK_SIZE = 64
IPAD = 0x36
OPAD = 0x5C


def _h(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def _derive_key(key: bytes) -> bytes:
    if len(key) > BLOCK_SIZE:
        key = _h(key)
    return key + b"\x00" * (BLOCK_SIZE - len(key))


def _xor_bytes(data: bytes, pad: int) -> bytes:
    return bytes(b ^ pad for b in data)


def hmac_sha256(key: bytes, message: bytes) -> str:
    k0 = _derive_key(key)
    inner_key = _xor_bytes(k0, IPAD)
    outer_key = _xor_bytes(k0, OPAD)
    inner_hash = _h(inner_key + message)
    tag = _h(outer_key + inner_hash)
    return tag.hex()


def _constant_time_equal(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    result = 0
    for ca, cb in zip(a, b):
        result |= ord(ca) ^ ord(cb)
    return result == 0


def verify(key: bytes, message: bytes, tag: str) -> bool:
    expected = hmac_sha256(key, message)
    return _constant_time_equal(expected, tag.lower())


def solve(data: dict) -> dict:
    op = data["op"]
    key = bytes.fromhex(data["key"])
    message = data["message"].encode("utf-8")
    if op == "tag":
        return {"tag": hmac_sha256(key, message)}
    elif op == "verify":
        return {"valid": verify(key, message, data["tag"])}
    else:
        raise ValueError(f"unknown op: {op!r}")
