# Coding problem, 5.3.b: Symmetric key-management toolkit

**Skill:** Mitigate Risk · **Maps to:** 5.3.A, 5.3.B · **Language:** Python 3 (pytest)

## Problem
Build three small helpers a security engineer would use when reasoning about symmetric key
management, without relying on any real crypto library (standard library only, this is a toy,
pedagogical model, not production cryptography).

1. **Key wrapping (envelope encryption).** Implement `wrap_key(dek, kek)` and
   `unwrap_key(wrapped, kek)` using a repeating-XOR keystream: each byte of `dek` is XORed with
   the KEK byte at the same position modulo `len(kek)`. This models how a Key Encryption Key
   (KEK) wraps a Data Encryption Key (DEK) for storage (see atom.md, "Key wrapping (Envelope
   Encryption)"). Unwrapping with the same KEK must recover the original DEK exactly, since
   XOR is its own inverse.
2. **Weak-RNG detection.** Implement `looks_like_csprng(key_bytes)`, a heuristic that flags keys
   that could NOT plausibly have come from a CSPRNG because they show low entropy / obvious
   structure (e.g., a single repeated byte, a short repeating pattern, or a strictly
   monotonic/arithmetic byte sequence like `0,1,2,3...`). Real CSPRNG output has no such
   structure.
3. **ECB pattern-leakage detection.** Implement `detect_ecb_leakage(ciphertext_blocks)`, which
   takes a list of same-size `bytes` blocks (as an ECB-mode block cipher would produce) and
   returns `True` if any two blocks are identical, the tell-tale sign that ECB mode is leaking
   repeated plaintext patterns into the ciphertext (see atom.md, "Electronic Codebook (ECB) Mode
   (Insecure)").

## Function contract
Implement all three functions in `starter.py` (see `interface.md` / `blackbox.yaml`):
```python
def wrap_key(dek: bytes, kek: bytes) -> bytes
def unwrap_key(wrapped: bytes, kek: bytes) -> bytes
def looks_like_csprng(key_bytes: bytes) -> bool
def detect_ecb_leakage(ciphertext_blocks: list) -> bool
```

## Input
- `wrap_key`/`unwrap_key`: `dek`/`wrapped` are `bytes` (may be empty); `kek` is non-empty `bytes`.
- `looks_like_csprng`: `key_bytes` is `bytes`, at least 1 byte.
- `detect_ecb_leakage`: `ciphertext_blocks` is `list[bytes]`, all blocks the same length.

## Output
- `wrap_key`/`unwrap_key` return `bytes` the same length as their key argument.
- `looks_like_csprng` returns `bool`.
- `detect_ecb_leakage` returns `bool`.

## Examples
```python
wrap_key(b"\x01\x02\x03\x04", b"\xff\x00")
# -> bytes([0x01^0xff, 0x02^0x00, 0x03^0xff, 0x04^0x00]) == b"\xfe\x02\xfc\x04"

unwrap_key(wrap_key(dek, kek), kek) == dek   # always, for any non-empty kek

looks_like_csprng(bytes([5]*16))            -> False   # single repeated byte
looks_like_csprng(bytes(range(16)))         -> False   # arithmetic/monotonic sequence
looks_like_csprng(b"\x4e\x91\x0a\xd3\x77\xbb\x02\xf8")  -> True   # no obvious structure

detect_ecb_leakage([b"AAAAAAAA", b"BBBBBBBB", b"AAAAAAAA"]) -> True    # block 0 == block 2
detect_ecb_leakage([b"AAAAAAAA", b"BBBBBBBB", b"CCCCCCCC"]) -> False
```

## Constraints
- Deterministic, offline, standard library only. No `import random`, no real crypto libraries
  (`cryptography`, `pycryptodome`, `hashlib`-based ciphers, etc.).
- `kek` is always non-empty for `wrap_key`/`unwrap_key`; `dek` may be empty (returns `b""`).
- `looks_like_csprng` receives at least 1 byte; treat any input shorter than 8 bytes as
  "too short to judge" and return `False` (not enough data to look random).
- `detect_ecb_leakage` receives zero or more equal-length `bytes` blocks.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
