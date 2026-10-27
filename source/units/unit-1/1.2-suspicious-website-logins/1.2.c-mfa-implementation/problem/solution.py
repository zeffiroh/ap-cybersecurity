"""Reference solution for 1.2.c. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
import hmac
import hashlib


def solve(secret: str, code: str, t: int) -> bool:
    """Verify a 6-digit TOTP code against the shared secret at Unix timestamp t.

    Args:
        secret: even-length hex string encoding the shared key (e.g. "0a1b2c3d").
        code:   6-character zero-padded decimal string (e.g. "007342").
        t:      current Unix timestamp (int, seconds since epoch).
    Returns:
        True if code matches TOTP(secret, t // 30); False otherwise.
    """
    key = bytes.fromhex(secret)
    step = t // 30
    msg = step.to_bytes(8, byteorder='big')
    digest = hmac.new(key, msg, hashlib.sha1).digest()

    # RFC 4226 dynamic truncation
    offset = digest[19] & 0x0f
    p = (((digest[offset] & 0x7f) << 24)
         | (digest[offset + 1] << 16)
         | (digest[offset + 2] << 8)
         | digest[offset + 3])

    otp = p % 1_000_000
    expected = str(otp).zfill(6)
    return code == expected
