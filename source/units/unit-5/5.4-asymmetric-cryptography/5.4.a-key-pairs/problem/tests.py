"""Test suite for 5.4.a — the blackbox acceptance contract.
Imports the implementation under test via IMPL env var so the SAME tests grade:
  - solution.py   (reference, must be green)
  - starter.py    (must be red until completed)
Default target is solution.py.
"""
import importlib.util
import os
import pathlib

_HERE = pathlib.Path(__file__).parent
_TARGET = os.environ.get("IMPL", str(_HERE / "solution.py"))


def _load(path):
    spec = importlib.util.spec_from_file_location("impl", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


impl = _load(_TARGET)


def _oracle_params(p, q):
    """Independent reference computation of (n, phi_n), used only to check the
    student implementation's output, never as part of the implementation."""
    return (p * q, (p - 1) * (q - 1))


# ---- visible cases -------------------------------------------------------
def test_rsa_params_small_primes_3_11():
    # worked example from atom.md / quiz.yaml q3
    n, phi_n = impl.rsa_params(3, 11)
    assert (n, phi_n) == (33, 20)


def test_rsa_params_small_primes_5_11():
    # worked example from atom.md's "Try it" section
    n, phi_n = impl.rsa_params(5, 11)
    assert (n, phi_n) == (55, 40)


def test_rsa_params_matches_oracle():
    p, q = 7, 13
    got = impl.rsa_params(p, q)
    assert got == _oracle_params(p, q)


def test_is_valid_keypair_true_case():
    # e=3, d=7, phi_n=20: 3*7 = 21, 21 % 20 == 1
    assert impl.is_valid_keypair(3, 7, 20) is True


def test_is_valid_keypair_false_case():
    # e=3, d=6, phi_n=20: 3*6 = 18, 18 % 20 != 1
    assert impl.is_valid_keypair(3, 6, 20) is False


def test_solve_params_op():
    result = impl.solve({"op": "params", "p": 3, "q": 11})
    assert result == {"n": 33, "phi_n": 20}


def test_solve_validate_op_valid():
    result = impl.solve({"op": "validate", "e": 3, "d": 7, "phi_n": 20})
    assert result == {"valid": True}


# ---- hidden / edge cases -------------------------------------------------
def test_rsa_params_return_type_is_tuple_like():
    n, phi_n = impl.rsa_params(3, 11)  # unpacking must work
    assert n == 33 and phi_n == 20


def test_solve_validate_op_invalid():
    result = impl.solve({"op": "validate", "e": 3, "d": 6, "phi_n": 20})
    assert result == {"valid": False}


def test_is_valid_keypair_e_d_larger_than_phi_n():
    # e=23, d=7, phi_n=20: 23*7 = 161, 161 % 20 == 1 -> valid even though e > phi_n
    assert impl.is_valid_keypair(23, 7, 20) is True


def test_is_valid_keypair_off_by_one_is_invalid():
    # e=3, d=8, phi_n=20: 3*8 = 24, 24 % 20 == 4, not 1
    assert impl.is_valid_keypair(3, 8, 20) is False


def test_rsa_params_larger_primes():
    p, q = 17, 23
    n, phi_n = impl.rsa_params(p, q)
    assert (n, phi_n) == _oracle_params(p, q)


def test_full_keygen_roundtrip_p5_q11_e3():
    # From p=5, q=11: n=55, phi_n=40. e=3 has inverse d=27 mod 40 (3*27=81, 81%40=1).
    n, phi_n = impl.rsa_params(5, 11)
    assert (n, phi_n) == (55, 40)
    assert impl.is_valid_keypair(3, 27, phi_n) is True
    assert impl.is_valid_keypair(3, 13, phi_n) is False


def test_solve_params_op_matches_oracle_random_primes():
    p, q = 13, 19
    result = impl.solve({"op": "params", "p": p, "q": q})
    expected_n, expected_phi = _oracle_params(p, q)
    assert result == {"n": expected_n, "phi_n": expected_phi}
