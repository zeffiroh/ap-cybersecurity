import hashlib
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

N = 3233
E = 17
D = 2753

def _oracle_digest_mod_n(message: bytes, n: int) -> int:
    digest_bytes = hashlib.sha256(message).digest()
    return int.from_bytes(digest_bytes, "big") % n


def _oracle_sign(message: bytes, d: int, n: int) -> int:
    return pow(_oracle_digest_mod_n(message, n), d, n)


def _find_d(e: int, phi_n: int) -> int:
    for cand in range(2, phi_n):
        if (e * cand) % phi_n == 1:
            return cand
    raise ValueError("no modular inverse found")


_P2, _Q2 = 59, 61
N2 = _P2 * _Q2
_PHI2 = (_P2 - 1) * (_Q2 - 1)
E2 = 7
D2 = _find_d(E2, _PHI2)


def test_sign_matches_oracle():
    message = b"transfer $100 to acct 42"
    got = impl.sign(message, D, N)
    assert got == _oracle_sign(message, D, N)


def test_valid_signature_verifies_true():
    message = b"pay Bob $50"
    signature = impl.sign(message, D, N)
    assert impl.verify(message, signature, E, N) is True


def test_tampered_message_fails_verification():
    message = b"pay Bob $50"
    tampered = b"pay Bob $950"
    signature = impl.sign(message, D, N)
    assert impl.verify(tampered, signature, E, N) is False


def test_wrong_public_key_fails_verification():
    message = b"deploy build 42"
    signature = impl.sign(message, D, N)
    assert impl.verify(message, signature, E2, N2) is False


def test_solve_sign_op():
    result = impl.solve({"op": "sign", "message": "hello", "d": D, "n": N})
    expected = _oracle_sign(b"hello", D, N)
    assert result == {"signature": expected}


def test_solve_verify_op_valid():
    message = "audit log entry 7"
    signature = _oracle_sign(message.encode("utf-8"), D, N)
    result = impl.solve({"op": "verify", "message": message, "signature": signature, "e": E, "n": N})
    assert result == {"valid": True}


def test_solve_verify_op_tampered_message():
    message = "audit log entry 7"
    signature = _oracle_sign(message.encode("utf-8"), D, N)
    result = impl.solve(
        {"op": "verify", "message": "audit log entry 8", "signature": signature, "e": E, "n": N}
    )
    assert result == {"valid": False}


def test_single_bit_change_in_message_flips_signature():
    a = b"password reset for user 1000"
    b = b"password reset for user 1001"
    sig_a = impl.sign(a, D, N)
    sig_b = impl.sign(b, D, N)
    assert sig_a != sig_b


def test_empty_message_signs_and_verifies():
    message = b""
    signature = impl.sign(message, D, N)
    assert impl.verify(message, signature, E, N) is True


def test_verify_rejects_signature_from_different_message_same_key():
    msg1 = b"approve invoice 9001"
    msg2 = b"approve invoice 9002"
    sig1 = impl.sign(msg1, D, N)
    assert impl.verify(msg2, sig1, E, N) is False


def test_signature_is_deterministic():
    message = b"same input, same output"
    sig1 = impl.sign(message, D, N)
    sig2 = impl.sign(message, D, N)
    assert sig1 == sig2


def test_signature_in_valid_range():
    message = b"range check"
    signature = impl.sign(message, D, N)
    assert 0 <= signature < N


def test_solve_unknown_op_raises():
    import pytest

    with pytest.raises(Exception):
        impl.solve({"op": "bogus", "message": "x"})
