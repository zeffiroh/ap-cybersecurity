# Coding problem, 5.3.c: Implement HMAC-SHA256 by hand

**Skill:** Mitigate Risk · **Maps to:** 5.3.B, 5.3.C · **Language:** Python 3 (pytest)

## Problem
An API needs to verify that requests were sent by a client holding a shared secret key, and
that the request body wasn't tampered with in transit. Rather than calling Python's built-in
`hmac` module, build the FIPS 198-1 HMAC construction yourself on top of `hashlib.sha256`, so
you can see exactly how the ipad/opad key-nesting defeats length-extension attacks.

## Function contract
Implement, in `starter.py`:
- `hmac_sha256(key: bytes, message: bytes) -> str`, return the HMAC-SHA256 tag as a
  lowercase 64-character hex string.
- `verify(key: bytes, message: bytes, tag: str) -> bool`, recompute the tag and compare it
  (case-insensitively) to the given `tag` using a constant-time comparison.
- `solve(data: dict) -> dict`, the blackbox entry point that dispatches to the two functions
  above (see `interface.md` / `blackbox.yaml`).

You must implement the ipad/opad key derivation and the double-nested hashing yourself. You
may use `hashlib.sha256` only as the inner hash primitive `H()`, do not import the `hmac`
module for the core logic.

## The construction (FIPS 198-1)
```
HMAC(key, message) = H( (key XOR opad) || H( (key XOR ipad) || message ) )
```
- Block size for SHA-256 is 64 bytes.
- If `key` is longer than 64 bytes, replace it with `H(key)` first.
- Right-pad `key` with `0x00` bytes up to exactly 64 bytes -> call this `k0`.
- `ipad` = the byte `0x36` repeated 64 times; `opad` = the byte `0x5c` repeated 64 times.
- `inner_key = k0 XOR ipad`, `outer_key = k0 XOR opad` (byte-wise XOR).
- `inner_hash = H(inner_key || message)`
- final tag = `H(outer_key || inner_hash)`, hex-encoded.

## Input / Output
- `hmac_sha256(key, message)`: `key: bytes`, `message: bytes` -> hex `str` tag.
- `verify(key, message, tag)`: `tag: str` (hex, any case) -> `bool`.
- `solve(data)`: `data = {"op": "tag", "key": "<hex>", "message": "<str>"}` ->
  `{"tag": "<hex>"}`, or `data = {"op": "verify", "key": "<hex>", "message": "<str>", "tag": "<hex>"}`
  -> `{"valid": <bool>}`.

## Examples
```
hmac_sha256(b"secretkey", b"transfer $100 to acct 42")
  -> "5b1f9a2c...b3" (64 hex chars; must match Python's hmac.new(key, msg, sha256).hexdigest())

verify(b"secretkey", b"transfer $100 to acct 42", "5b1f9a2c...b3") -> True
verify(b"secretkey", b"transfer $900 to acct 42", "5b1f9a2c...b3") -> False  # tampered message
```

## Constraints
- Deterministic, offline, standard library only (`hashlib` only, no `hmac` module).
- Correctness is checked against Python's own `hmac` module inside `tests.py` (used there only
  as an independent oracle, not as part of your implementation).
- Must pass all cases in `tests.py` (visible + hidden), including empty keys/messages, keys
  longer than the 64-byte block size, and case-insensitive tag comparison in `verify()`.

## How to run
```
cd problem && python -m pytest tests.py -q
```
