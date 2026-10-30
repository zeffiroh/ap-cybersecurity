import hashlib


def _digest_mod_n(message: bytes, n: int) -> int:
    digest_bytes = hashlib.sha256(message).digest()
    digest_int = int.from_bytes(digest_bytes, "big")
    return digest_int % n


def sign(message: bytes, d: int, n: int) -> int:
    digest = _digest_mod_n(message, n)
    return pow(digest, d, n)


def verify(message: bytes, signature: int, e: int, n: int) -> bool:
    expected_digest = _digest_mod_n(message, n)
    recovered_digest = pow(signature, e, n)
    return expected_digest == recovered_digest


def solve(data: dict) -> dict:
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
