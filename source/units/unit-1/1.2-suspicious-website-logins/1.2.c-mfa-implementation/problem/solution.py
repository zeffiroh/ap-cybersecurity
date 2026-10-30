import hmac
import hashlib


def solve(secret: str, code: str, t: int) -> bool:
    key = bytes.fromhex(secret)
    step = t // 30
    msg = step.to_bytes(8, byteorder='big')
    digest = hmac.new(key, msg, hashlib.sha1).digest()

    offset = digest[19] & 0x0f
    p = (((digest[offset] & 0x7f) << 24)
         | (digest[offset + 1] << 16)
         | (digest[offset + 2] << 8)
         | digest[offset + 3])

    otp = p % 1_000_000
    expected = str(otp).zfill(6)
    return code == expected
