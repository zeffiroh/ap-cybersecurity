"""Reference solution for 5.3.b. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""


def wrap_key(dek: bytes, kek: bytes) -> bytes:
    """Wrap a DEK with a KEK using a repeating-XOR keystream (toy envelope encryption)."""
    if not kek:
        raise ValueError("kek must be non-empty")
    return bytes(b ^ kek[i % len(kek)] for i, b in enumerate(dek))


def unwrap_key(wrapped: bytes, kek: bytes) -> bytes:
    """Inverse of wrap_key(): XOR is its own inverse."""
    return wrap_key(wrapped, kek)


def looks_like_csprng(key_bytes: bytes) -> bool:
    """Heuristically flag whether key_bytes could plausibly have come from a CSPRNG."""
    n = len(key_bytes)
    if n < 8:
        return False

    # All bytes identical.
    if len(set(key_bytes)) == 1:
        return False

    # Short repeating pattern that tiles the whole input.
    for period in range(1, n // 2 + 1):
        pattern = key_bytes[:period]
        tiled = (pattern * (n // period + 1))[:n]
        if tiled == key_bytes:
            return False

    # Constant-step arithmetic sequence (mod 256).
    step = (key_bytes[1] - key_bytes[0]) % 256
    is_arithmetic = all(
        (key_bytes[i] - key_bytes[i - 1]) % 256 == step for i in range(1, n)
    )
    if is_arithmetic:
        return False

    return True


def detect_ecb_leakage(ciphertext_blocks: list) -> bool:
    """True if any two blocks in ciphertext_blocks are identical (ECB pattern leak)."""
    seen = set()
    for block in ciphertext_blocks:
        if block in seen:
            return True
        seen.add(block)
    return False
