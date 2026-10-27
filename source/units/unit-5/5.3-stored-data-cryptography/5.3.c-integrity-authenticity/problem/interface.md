# Interface, 5.3.c-hmac-sha256 (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry points
```python
def hmac_sha256(key: bytes, message: bytes) -> str
def verify(key: bytes, message: bytes, tag: str) -> bool
def solve(data: dict) -> dict
```

`solve()` is the blackbox entry point; `hmac_sha256()` and `verify()` are the underlying
primitives it's built on and are tested directly as well.

## Input
- `hmac_sha256(key, message)`: `key` and `message` are raw `bytes` of any length (including
  empty and longer-than-block-size keys).
- `verify(key, message, tag)`: same `key`/`message` as above; `tag` is a hex string (may be
  upper or lower case) claiming to be the correct HMAC-SHA256 tag.
- `solve(data)`: `data` is a `dict` with `"op"` equal to `"tag"` or `"verify"`.
  - `"tag"`: `{"op": "tag", "key": <hex str>, "message": <str>}`
  - `"verify"`: `{"op": "verify", "key": <hex str>, "message": <str>, "tag": <hex str>}`
  - `key` arrives as a hex string (decode with `bytes.fromhex`); `message` arrives as a
    plain UTF-8 string (encode with `.encode("utf-8")`).

## Output (`result`)
- `hmac_sha256(...)` returns a lowercase hex string (64 hex characters for SHA-256).
- `verify(...)` returns `bool`.
- `solve(...)` returns `{"tag": <hex str>}` for op `"tag"`, or `{"valid": <bool>}` for op `"verify"`.

## Guarantees / rules
- Pure functions, deterministic, no I/O, no network. Standard library only
  (`hashlib.sha256` may be used as the inner hash primitive `H()`; the ipad/opad key
  derivation and double-nesting must be implemented directly, not via the `hmac` module).
- Must implement the FIPS 198-1 HMAC construction:
  `HMAC(key, message) = H((key XOR opad) || H((key XOR ipad) || message))`, with
  `ipad = 0x36` and `opad = 0x5c` repeated to the 64-byte SHA-256 block size, and keys
  longer than the block size first hashed down with `H()` before padding.
- Any single-bit change to `message` or `key` must produce a different tag.
- `verify()` must accept tags regardless of hex case (upper/lower).

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
