"""Starter code for 5.3.b. Student completes the TODOs.
This file intentionally FAILS the tests until implemented."""


def wrap_key(dek: bytes, kek: bytes) -> bytes:
    """Wrap a Data Encryption Key (DEK) with a Key Encryption Key (KEK) using a
    repeating-XOR keystream (toy envelope encryption — NOT real crypto).

    Args:
        dek: plaintext key to wrap (may be empty).
        kek: non-empty wrapping key.
    Returns:
        bytes of len(dek), where byte i = dek[i] XOR kek[i % len(kek)].
    """
    # TODO: XOR each byte of dek with the KEK byte at the same position, wrapping
    #       the KEK index around with modulo len(kek).
    raise NotImplementedError("implement wrap_key() — see prompt.md")


def unwrap_key(wrapped: bytes, kek: bytes) -> bytes:
    """Inverse of wrap_key(): recovers the original DEK given the same KEK.

    Args:
        wrapped: bytes produced by wrap_key(dek, kek).
        kek: the same non-empty KEK used to wrap.
    Returns:
        the original dek bytes.
    """
    # TODO: XOR is its own inverse — this can reuse the same logic as wrap_key.
    raise NotImplementedError("implement unwrap_key() — see prompt.md")


def looks_like_csprng(key_bytes: bytes) -> bool:
    """Heuristically flag whether key_bytes could plausibly have come from a
    CSPRNG, vs. showing obvious low-entropy structure (repeated byte, short
    repeating pattern, or an arithmetic/monotonic sequence).

    Args:
        key_bytes: candidate generated key.
    Returns:
        False if len(key_bytes) < 8 (too short to judge), or if the bytes show
        obvious structure. True otherwise.
    """
    # TODO: check length < 8 -> False.
    # TODO: check all-identical bytes -> False.
    # TODO: check for a short repeating pattern (period 1..len//2) that tiles
    #       the whole input -> False.
    # TODO: check for a constant-step arithmetic sequence (mod 256) -> False.
    # TODO: otherwise -> True.
    raise NotImplementedError("implement looks_like_csprng() — see prompt.md")


def detect_ecb_leakage(ciphertext_blocks: list) -> bool:
    """Detect ECB-mode pattern leakage: True if any two blocks are identical.

    Args:
        ciphertext_blocks: list[bytes], all the same length.
    Returns:
        True if any duplicate block exists, False otherwise (or if < 2 blocks).
    """
    # TODO: compare blocks pairwise (or use a set) to find any duplicate.
    raise NotImplementedError("implement detect_ecb_leakage() — see prompt.md")
