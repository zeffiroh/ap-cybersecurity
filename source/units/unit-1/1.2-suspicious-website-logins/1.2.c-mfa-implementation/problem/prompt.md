# Coding problem -- 1.2.c: TOTP Verifier

**Skill:** Mitigate Risk · **Maps to:** 1.2.C · **Language:** Python 3 (pytest)

## Problem
Implement the server-side Time-based One-Time Password (TOTP) verifier that an authentication
backend would call to check a user's second factor. Given the shared secret, a submitted code,
and the current time, return True if the code is valid for the current 30-second window.

This is the algorithm defined in RFC 6238 (TOTP) / RFC 4226 (HOTP), implemented using only
Python's standard library `hmac` and `hashlib` modules.

## Function contract
Implement `solve(secret: str, code: str, t: int) -> bool` in `starter.py`
(see `interface.md` / `blackbox.yaml`).

## Input
- `secret` (`str`) -- the shared secret key, encoded as an **even-length lowercase hex string**
  (e.g. `"0a1b2c3d"` represents 4 bytes: `b'\x0a\x1b\x2c\x3d'`).
- `code` (`str`) -- the 6-digit code submitted by the user, zero-padded if necessary
  (e.g. `"007342"` or `"123456"`).
- `t` (`int`) -- the current Unix timestamp (seconds since epoch) at the moment of verification.

## Output
`True` if the computed TOTP code for the current 30-second step matches `code`; `False` otherwise.

## Algorithm (exact steps, deterministic)
1. Decode the secret: `key = bytes.fromhex(secret)`
2. Compute the time step: `step = t // 30`
3. Encode the step as an 8-byte big-endian integer: `msg = step.to_bytes(8, 'big')`
4. Compute HMAC-SHA1: `digest = hmac.new(key, msg, hashlib.sha1).digest()`
   (This produces a 20-byte bytes object.)
5. Dynamic truncation:
   a. `offset = digest[19] & 0x0f`
   b. `p = ((digest[offset] & 0x7f) << 24) | (digest[offset+1] << 16) | (digest[offset+2] << 8) | digest[offset+3]`
6. Compute the OTP: `otp = p % 1_000_000`
7. Zero-pad: `expected = str(otp).zfill(6)`
8. Return `code == expected`

## Examples
```python
# Using key=bytes.fromhex("3132333435363738393031323334353637383930") (RFC 4226 test vector)
# At t=59 (step=1): expected code is "287082"
solve("3132333435363738393031323334353637383930", "287082", 59)   -> True
solve("3132333435363738393031323334353637383930", "287082", 60)   -> False  # step changed
solve("3132333435363738393031323334353637383930", "000000", 59)   -> False  # wrong code
```

## Constraints
- Deterministic, offline, stdlib only (`hmac`, `hashlib`).
- Accept only the CURRENT step (no window drift / no adjacent steps).
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
