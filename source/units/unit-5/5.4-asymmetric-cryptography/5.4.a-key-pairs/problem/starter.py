"""Starter code for 5.4.a. Student completes the TODOs.
This file intentionally FAILS the tests until implemented."""


def rsa_params(p: int, q: int) -> tuple:
    """Given two (small, distinct) primes p and q, return (n, phi_n) where
    n = p * q and phi_n = (p - 1) * (q - 1).

    This is step 1-2 of RSA key generation (see atom.md): n becomes part of both
    the public and private key; phi_n is used to derive the private exponent d.
    """
    # TODO: compute n = p * q and phi_n = (p - 1) * (q - 1); return (n, phi_n).
    raise NotImplementedError("implement rsa_params() — see prompt.md")


def is_valid_keypair(e: int, d: int, phi_n: int) -> bool:
    """Return True iff (e * d) mod phi_n == 1, i.e. d is the modular inverse of e
    mod phi_n. This is the defining relationship between the public exponent e
    and the private exponent d (see atom.md step 4)."""
    # TODO: return whether (e * d) % phi_n == 1.
    raise NotImplementedError("implement is_valid_keypair() — see prompt.md")


def solve(data: dict) -> dict:
    """Blackbox entry point. Dispatches on data['op']:
      - {"op": "params", "p": <int>, "q": <int>}
            -> {"n": <int>, "phi_n": <int>}
      - {"op": "validate", "e": <int>, "d": <int>, "phi_n": <int>}
            -> {"valid": <bool>}
    """
    # TODO: dispatch on data["op"] to rsa_params() or is_valid_keypair(),
    #       building the appropriate result dict.
    raise NotImplementedError("implement solve() — see prompt.md")
