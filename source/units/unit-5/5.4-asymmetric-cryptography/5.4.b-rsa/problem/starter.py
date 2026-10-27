"""Starter code for 5.4.b. Student completes the TODOs.
This file intentionally FAILS the tests until implemented."""


def egcd(a: int, b: int):
    """Extended Euclidean algorithm. Returns (g, x, y) such that a*x + b*y = g = gcd(a, b)."""
    # TODO: base case: if b == 0, return (a, 1, 0).
    #       otherwise recurse: g, x1, y1 = egcd(b, a % b); return (g, y1, x1 - (a // b) * y1)
    raise NotImplementedError("implement egcd() — see prompt.md")


def mod_inverse(e: int, phi_n: int) -> int:
    """Return d, the modular inverse of e mod phi_n, satisfying (e * d) % phi_n == 1.

    Raises ValueError if e and phi_n are not coprime (no inverse exists)."""
    # TODO: call egcd(e, phi_n) -> (g, x, _). If g != 1, raise ValueError.
    #       Otherwise return x % phi_n.
    raise NotImplementedError("implement mod_inverse() — see prompt.md")


def rsa_keygen(p: int, q: int, e: int) -> dict:
    """Derive full RSA key material from primes p, q and public exponent e.

    Returns {"n": n, "phi_n": phi_n, "e": e, "d": d}.
    """
    # TODO: n = p * q; phi_n = (p-1)*(q-1); validate 1 < e < phi_n (else ValueError);
    #       d = mod_inverse(e, phi_n); return the dict.
    raise NotImplementedError("implement rsa_keygen() — see prompt.md")


def encrypt(m: int, e: int, n: int) -> int:
    """RSA encrypt: c = m^e mod n. m must satisfy 0 <= m < n."""
    # TODO: validate 0 <= m < n (else ValueError), then return pow(m, e, n).
    raise NotImplementedError("implement encrypt() — see prompt.md")


def decrypt(c: int, d: int, n: int) -> int:
    """RSA decrypt: m = c^d mod n."""
    # TODO: return pow(c, d, n).
    raise NotImplementedError("implement decrypt() — see prompt.md")


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
    # TODO: dispatch on data["op"] to rsa_keygen()/encrypt()/decrypt(), and for
    #       "roundtrip" combine all three the way solution.py does.
    raise NotImplementedError("implement solve() — see prompt.md")
