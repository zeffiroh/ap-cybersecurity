"""Reference solution for 5.4.a. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml).

Implements the RSA key-pair math by hand (n, phi(n), keypair validation) as described
in atom.md, using small textbook-scale primes. No external crypto libraries — this is
a from-scratch pedagogical implementation: crypto problems
implement the underlying math/logic directly.
"""


def rsa_params(p: int, q: int) -> tuple:
    """Given two (small, distinct) primes p and q, return (n, phi_n) where
    n = p * q and phi_n = (p - 1) * (q - 1).

    This is step 1-2 of RSA key generation (see atom.md): n becomes part of both
    the public and private key; phi_n is used to derive the private exponent d.
    """
    n = p * q
    phi_n = (p - 1) * (q - 1)
    return (n, phi_n)


def is_valid_keypair(e: int, d: int, phi_n: int) -> bool:
    """Return True iff (e * d) mod phi_n == 1, i.e. d is the modular inverse of e
    mod phi_n. This is the defining relationship between the public exponent e
    and the private exponent d (see atom.md step 4)."""
    return (e * d) % phi_n == 1


def solve(data: dict) -> dict:
    """Blackbox entry point. Dispatches on data['op']:
      - {"op": "params", "p": <int>, "q": <int>}
            -> {"n": <int>, "phi_n": <int>}
      - {"op": "validate", "e": <int>, "d": <int>, "phi_n": <int>}
            -> {"valid": <bool>}
    """
    op = data["op"]
    if op == "params":
        n, phi_n = rsa_params(data["p"], data["q"])
        return {"n": n, "phi_n": phi_n}
    elif op == "validate":
        return {"valid": is_valid_keypair(data["e"], data["d"], data["phi_n"])}
    else:
        raise ValueError(f"unknown op: {op!r}")
