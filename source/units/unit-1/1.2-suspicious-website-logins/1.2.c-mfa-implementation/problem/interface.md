# Interface -- 1.2.c-totp-verifier (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(secret: str, code: str, t: int) -> bool
```

## Input
- `secret` (`str`) -- even-length lowercase hex string encoding the TOTP shared secret key
  (e.g. `"0a1b2c3d"` = 4 bytes). Tests only use valid hex strings of 4-20 bytes.
- `code` (`str`) -- 6-character string of decimal digits, zero-padded (e.g. `"007342"`).
- `t` (`int`) -- current Unix timestamp (non-negative integer).

## Output
`bool` -- `True` if `code` matches the TOTP for the 30-second step containing `t`; else `False`.

## Algorithm (exact, deterministic -- all tests derive expected values from this spec)

```
key    = bytes.fromhex(secret)
step   = t // 30
msg    = step.to_bytes(8, byteorder='big')
digest = hmac.new(key, msg, hashlib.sha1).digest()   # 20 bytes

offset = digest[19] & 0x0f
p      = ((digest[offset] & 0x7f) << 24
         | digest[offset+1] << 16
         | digest[offset+2] << 8
         | digest[offset+3])
otp    = p % 1_000_000
expected = str(otp).zfill(6)

return code == expected
```

## RFC 4226 test vector (for implementation validation)
Secret (ASCII "12345678901234567890" = 20 bytes, hex below):
```
secret = "3132333435363738393031323334353637383930"
```
Known correct codes per HOTP counter (step for TOTP = t // 30):

| step (t value) | expected code |
|----------------|---------------|
| 1  (t = 30-59)  | 287082        |
| 2  (t = 60-89)  | 359152        |
| 3  (t = 90-119) | 969429        |

These are derived from the RFC 4226 test vectors. `tests.py` uses them to validate any
implementation.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network.
- Standard library only: `import hmac`, `import hashlib`.
- Only the CURRENT step is accepted (no window tolerance / no drift allowance).
- `code` is always exactly 6 characters. A code with fewer than 6 digits is already zero-padded
  by the caller.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
