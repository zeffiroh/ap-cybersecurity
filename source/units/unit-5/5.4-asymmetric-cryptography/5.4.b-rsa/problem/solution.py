"""Reference solution for 5.4.b. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml).

Implements small-number textbook RSA directly: key derivation (n, phi_n, d via the
extended Euclidean algorithm) and encrypt/decrypt via modular exponentiation
(Python's built-in pow(), which is stdlib, not an external crypto library).
"""


def egcd(a: int, b: int):
    """Extended Euclidean algorithm. Returns (g, x, y) such that a*x + b*y = g = gcd(a, b)."""
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)


def mod_inverse(e: int, phi_n: int) -> int:
    """Return d, the modular inverse of e mod phi_n, satisfying (e * d) % phi_n == 1.

    Raises ValueError if e and phi_n are not coprime (no inverse exists)."""
    g, x, _ = egcd(e, phi_n)
    if g != 1:
        raise ValueError(f"e={e} has no modular inverse mod phi_n={phi_n} (gcd={g})")
    return x % phi_n


def rsa_keygen(p: int, q: int, e: int) -> dict:
    """Derive full RSA key material from primes p, q and public exponent e.

    Returns {"n": n, "phi_n": phi_n, "e": e, "d": d}.
    """
    n = p * q
    phi_n = (p - 1) * (q - 1)
    if not (1 < e < phi_n):
        raise ValueError(f"e={e} must satisfy 1 < e < phi_n={phi_n}")
    d = mod_inverse(e, phi_n)
    return {"n": n, "phi_n": phi_n, "e": e, "d": d}


def encrypt(m: int, e: int, n: int) -> int:
    """RSA encrypt: c = m^e mod n. m must satisfy 0 <= m < n."""
    if not (0 <= m < n):
        raise ValueError(f"message m={m} must satisfy 0 <= m < n={n}")
    return pow(m, e, n)


def decrypt(c: int, d: int, n: int) -> int:
    """RSA decrypt: m = c^d mod n."""
    return pow(c, d, n)


def solve(data):
    """Blackbox entry point. Dispatches on data['op']:
      - {"op": "keygen", "p": int, "q": int, "e": int}
            -> {"n": int, "phi_n": int, "e": int, "d": int}
      - {"op": "encrypt", "m": int, "e": int, "n": int}
            -> {"c": int}
      - {"op": "decrypt", "c": int, "d": int, "n": int}
            -> {"m": int}
      - {"op": "roundtrip", "p": int, "q": int, "e": int, "m": int}
            -> {"n": int, "phi_n": int, "d": int, "c": int, "m_decrypted": int}
    """
    op = data["op"]
    if op == "keygen":
        return rsa_keygen(data["p"], data["q"], data["e"])
    elif op == "encrypt":
        return {"c": encrypt(data["m"], data["e"], data["n"])}
    elif op == "decrypt":
        return {"m": decrypt(data["c"], data["d"], data["n"])}
    elif op == "roundtrip":
        keys = rsa_keygen(data["p"], data["q"], data["e"])
        c = encrypt(data["m"], keys["e"], keys["n"])
        m_decrypted = decrypt(c, keys["d"], keys["n"])
        return {
            "n": keys["n"],
            "phi_n": keys["phi_n"],
            "d": keys["d"],
            "c": c,
            "m_decrypted": m_decrypted,
        }
    else:
        raise ValueError(f"unknown op: {op!r}")
