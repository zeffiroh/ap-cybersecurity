"""Starter code for 1.2.c. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""


def solve(secret: str, code: str, t: int) -> bool:
    """Verify a 6-digit TOTP code against the shared secret at Unix timestamp t.

    Args:
        secret: even-length hex string encoding the shared key (e.g. "0a1b2c3d").
        code:   6-character zero-padded decimal string (e.g. "007342").
        t:      current Unix timestamp (int, seconds since epoch).
    Returns:
        True if code matches TOTP(secret, t // 30); False otherwise.

    Algorithm (from interface.md):
      1. key    = bytes.fromhex(secret)
      2. step   = t // 30
      3. msg    = step.to_bytes(8, byteorder='big')
      4. digest = hmac.new(key, msg, hashlib.sha1).digest()   # 20 bytes
      5. offset = digest[19] & 0x0f
      6. p      = ((digest[offset] & 0x7f) << 24) | (digest[offset+1] << 16)
                  | (digest[offset+2] << 8) | digest[offset+3]
      7. otp    = p % 1_000_000
      8. return code == str(otp).zfill(6)

    Import hmac and hashlib from the standard library only.
    """
    # TODO: implement the TOTP verifier -- see prompt.md and interface.md
    raise NotImplementedError("implement solve() -- see prompt.md")
