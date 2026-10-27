"""Test suite for 5.4.b — the blackbox acceptance contract.
Imports the implementation under test via IMPL env var so the SAME tests grade:
  - solution.py   (reference, must be green)
  - starter.py    (must be red until completed)
Default target is solution.py.
"""
import importlib.util
import os
import pathlib

import pytest

_HERE = pathlib.Path(__file__).parent
_TARGET = os.environ.get("IMPL", str(_HERE / "solution.py"))


def _load(path):
    spec = importlib.util.spec_from_file_location("impl", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


impl = _load(_TARGET)


# ---- visible cases -------------------------------------------------------
def test_keygen_small_example():
    # p=3, q=11, e=7 -> n=33, phi_n=20, d=3 (matches atom.md worked example)
    result = impl.rsa_keygen(3, 11, 7)
    assert result == {"n": 33, "phi_n": 20, "e": 7, "d": 3}


def test_encrypt_matches_worked_example():
    assert impl.encrypt(5, 7, 33) == 14


def test_decrypt_matches_worked_example():
    assert impl.decrypt(14, 3, 33) == 5


def test_encrypt_then_decrypt_roundtrip():
    keys = impl.rsa_keygen(3, 11, 7)
    for m in range(0, 33):
        c = impl.encrypt(m, keys["e"], keys["n"])
        assert impl.decrypt(c, keys["d"], keys["n"]) == m


def test_solve_keygen_op():
    result = impl.solve({"op": "keygen", "p": 3, "q": 11, "e": 7})
    assert result == {"n": 33, "phi_n": 20, "e": 7, "d": 3}


def test_solve_encrypt_op():
    result = impl.solve({"op": "encrypt", "m": 5, "e": 7, "n": 33})
    assert result == {"c": 14}


def test_solve_decrypt_op():
    result = impl.solve({"op": "decrypt", "c": 14, "d": 3, "n": 33})
    assert result == {"m": 5}


def test_solve_roundtrip_op():
    result = impl.solve({"op": "roundtrip", "p": 3, "q": 11, "e": 7, "m": 5})
    assert result == {"n": 33, "phi_n": 20, "d": 3, "c": 14, "m_decrypted": 5}


# ---- hidden / edge cases -------------------------------------------------
def test_keygen_different_primes():
    # p=61, q=53, e=17 (larger textbook-style example)
    result = impl.rsa_keygen(61, 53, 17)
    n = 61 * 53
    phi_n = 60 * 52
    assert result["n"] == n
    assert result["phi_n"] == phi_n
    assert (17 * result["d"]) % phi_n == 1


def test_full_roundtrip_larger_keys():
    keys = impl.rsa_keygen(61, 53, 17)
    m = 1234
    c = impl.encrypt(m, keys["e"], keys["n"])
    assert impl.decrypt(c, keys["d"], keys["n"]) == m
    assert c != m


def test_mod_inverse_correctness():
    d = impl.mod_inverse(7, 20)
    assert (7 * d) % 20 == 1
    assert d == 3


def test_mod_inverse_raises_when_not_coprime():
    with pytest.raises(ValueError):
        impl.mod_inverse(4, 20)  # gcd(4, 20) = 4, no inverse


def test_encrypt_message_zero():
    keys = impl.rsa_keygen(3, 11, 7)
    c = impl.encrypt(0, keys["e"], keys["n"])
    assert c == 0
    assert impl.decrypt(c, keys["d"], keys["n"]) == 0


def test_encrypt_rejects_message_too_large():
    with pytest.raises(ValueError):
        impl.encrypt(33, 7, 33)  # m must be < n


def test_keygen_rejects_invalid_e():
    with pytest.raises(ValueError):
        impl.rsa_keygen(3, 11, 4)  # gcd(4, 20) = 4, not coprime with phi_n


def test_ciphertext_differs_from_plaintext_for_nontrivial_message():
    keys = impl.rsa_keygen(61, 53, 17)
    m = 42
    c = impl.encrypt(m, keys["e"], keys["n"])
    assert c != m


def test_egcd_basic_identity():
    a, b = 7, 20
    g, x, y = impl.egcd(a, b)
    assert g == 1
    assert a * x + b * y == g
