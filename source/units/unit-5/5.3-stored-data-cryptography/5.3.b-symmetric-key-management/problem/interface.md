# Interface, 5.3.b-symmetric-key-toolkit (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry points
```python
def wrap_key(dek: bytes, kek: bytes) -> bytes
def unwrap_key(wrapped: bytes, kek: bytes) -> bytes
def looks_like_csprng(key_bytes: bytes) -> bool
def detect_ecb_leakage(ciphertext_blocks: list) -> bool
```

## Input / output

### `wrap_key(dek, kek) -> bytes`
- `dek`: `bytes`, the plaintext Data Encryption Key to wrap (may be empty).
- `kek`: `bytes`, the Key Encryption Key, non-empty.
- Returns `bytes` of the same length as `dek`, where output byte `i` is
  `dek[i] XOR kek[i % len(kek)]` (repeating-XOR keystream).

### `unwrap_key(wrapped, kek) -> bytes`
- Inverse of `wrap_key`: `unwrap_key(wrap_key(dek, kek), kek) == dek` for any `dek` and any
  non-empty `kek`, since XOR is its own inverse.

### `looks_like_csprng(key_bytes) -> bool`
- `key_bytes`: `bytes`, a candidate generated key.
- Returns `False` if `len(key_bytes) < 8` (too short to judge).
- Returns `False` if the bytes show obvious low-entropy structure:
  - all bytes identical, OR
  - the byte sequence is a short repeating pattern (period `p` with
    `1 <= p <= len(key_bytes)//2`) that tiles the whole input, OR
  - the byte sequence is strictly a constant-step arithmetic sequence (e.g. `0,1,2,3...` or
    `10,8,6,4...`), taken modulo 256.
- Returns `True` otherwise.

### `detect_ecb_leakage(ciphertext_blocks) -> bool`
- `ciphertext_blocks`: `list[bytes]`, all the same length (as ECB-mode block-cipher output would
  be); may be empty or contain a single block.
- Returns `True` if any two blocks in the list are byte-for-byte identical (indicating the
  plaintext blocks that produced them were also identical, the ECB pattern-leakage weakness).
- Returns `False` if all blocks are distinct, or if there are fewer than 2 blocks.

## Guarantees / rules
- Pure functions, deterministic, no I/O, no network. Standard library only.
- No use of `random`, `os.urandom`, `secrets`, or any real cipher/hash primitive, the point of
  this toy toolkit is to reason about structure and wrapping mechanics, not to be secure.
- `wrap_key`/`unwrap_key`: `kek` non-empty is a caller guarantee, not something the function must
  validate defensively beyond raising on empty `kek`.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
