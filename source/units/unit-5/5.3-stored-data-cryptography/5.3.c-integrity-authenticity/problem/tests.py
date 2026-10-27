"""Test suite for 5.3.c — the blackbox acceptance contract.
Imports the implementation under test via IMPL env var so the SAME tests grade:
  - solution.py   (reference, must be green)
  - starter.py    (must be red until completed)
Default target is solution.py.
"""
import hashlib
import hmac as _stdlib_hmac  # only used here, in tests, as an independent oracle
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


def _oracle_tag(key: bytes, message: bytes) -> str:
    """Independent reference tag computed with Python's stdlib hmac, used only to
    check the student implementation's output, never as part of the implementation."""
    return _stdlib_hmac.new(key, message, hashlib.sha256).hexdigest()


# ---- visible cases -------------------------------------------------------
def test_matches_stdlib_hmac_short_key():
    key = b"secretkey"
    message = b"transfer $100 to acct 42"
    got = impl.hmac_sha256(key, message)
    assert got == _oracle_tag(key, message)


def test_matches_stdlib_hmac_long_key():
    key = b"x" * 100  # longer than the 64-byte block size, exercises key-hashing path
    message = b"hello world"
    got = impl.hmac_sha256(key, message)
    assert got == _oracle_tag(key, message)


def test_tampered_message_changes_tag():
    key = b"secretkey"
    original = b"transfer $100 to acct 42"
    tampered = b"transfer $900 to acct 42"
    tag_original = impl.hmac_sha256(key, original)
    tag_tampered = impl.hmac_sha256(key, tampered)
    assert tag_original != tag_tampered


def test_verify_accepts_correct_tag():
    key = b"apikey123"
    message = b"GET /accounts/42"
    tag = impl.hmac_sha256(key, message)
    assert impl.verify(key, message, tag) is True


def test_verify_rejects_tampered_message():
    key = b"apikey123"
    message = b"GET /accounts/42"
    tag = impl.hmac_sha256(key, message)
    assert impl.verify(key, b"GET /accounts/99", tag) is False


def test_solve_tag_op():
    result = impl.solve({"op": "tag", "key": "deadbeef", "message": "hello"})
    expected = _oracle_tag(bytes.fromhex("deadbeef"), b"hello")
    assert result == {"tag": expected}


def test_solve_verify_op():
    key_hex = "deadbeef"
    tag = _oracle_tag(bytes.fromhex(key_hex), b"hello")
    result = impl.solve({"op": "verify", "key": key_hex, "message": "hello", "tag": tag})
    assert result == {"valid": True}


# ---- hidden / edge cases -------------------------------------------------
def test_wrong_key_fails_verify():
    message = b"payload"
    tag = impl.hmac_sha256(b"key-a", message)
    assert impl.verify(b"key-b", message, tag) is False


def test_empty_message():
    key = b"secretkey"
    got = impl.hmac_sha256(key, b"")
    assert got == _oracle_tag(key, b"")


def test_empty_key():
    message = b"some data"
    got = impl.hmac_sha256(b"", message)
    assert got == _oracle_tag(b"", message)


def test_key_exactly_block_size():
    key = b"k" * 64  # exactly the SHA-256 block size boundary
    message = b"boundary case"
    got = impl.hmac_sha256(key, message)
    assert got == _oracle_tag(key, message)


def test_single_bit_flip_changes_tag_completely():
    key = b"secretkey"
    a = b"password reset for user 1000"
    b = b"password reset for user 1001"  # differs by a single character
    tag_a = impl.hmac_sha256(key, a)
    tag_b = impl.hmac_sha256(key, b)
    assert tag_a != tag_b
    # avalanche: tags should differ in most positions, not just a trailing few
    diff = sum(1 for x, y in zip(tag_a, tag_b) if x != y)
    assert diff > len(tag_a) // 4


def test_verify_case_insensitive_hex_tag():
    key = b"secretkey"
    message = b"case check"
    tag = impl.hmac_sha256(key, message)
    assert impl.verify(key, message, tag.upper()) is True


def test_solve_verify_op_rejects_bad_tag():
    result = impl.solve({"op": "verify", "key": "aa", "message": "x", "tag": "0" * 64})
    assert result == {"valid": False}
