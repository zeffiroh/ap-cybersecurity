def egcd(a: int, b: int):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)


def mod_inverse(e: int, phi_n: int) -> int:
    g, x, _ = egcd(e, phi_n)
    if g != 1:
        raise ValueError(f"e={e} has no modular inverse mod phi_n={phi_n} (gcd={g})")
    return x % phi_n


def rsa_keygen(p: int, q: int, e: int) -> dict:
    n = p * q
    phi_n = (p - 1) * (q - 1)
    if not (1 < e < phi_n):
        raise ValueError(f"e={e} must satisfy 1 < e < phi_n={phi_n}")
    d = mod_inverse(e, phi_n)
    return {"n": n, "phi_n": phi_n, "e": e, "d": d}


def encrypt(m: int, e: int, n: int) -> int:
    if not (0 <= m < n):
        raise ValueError(f"message m={m} must satisfy 0 <= m < n={n}")
    return pow(m, e, n)


def decrypt(c: int, d: int, n: int) -> int:
    return pow(c, d, n)


def solve(data):
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
