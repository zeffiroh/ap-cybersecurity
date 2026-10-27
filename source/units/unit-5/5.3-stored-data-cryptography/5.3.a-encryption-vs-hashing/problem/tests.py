"""Test suite for 5.3.a — the blackbox acceptance contract.
Imports the implementation under test via IMPL env var so the SAME tests grade:
  - solution.py   (reference, must be green)
  - starter.py    (must be red until completed)
Default target is solution.py.
"""
import importlib.util
import os
import pathlib
import hashlib

_HERE = pathlib.Path(__file__).parent
_TARGET = os.environ.get("IMPL", str(_HERE / "solution.py"))


def _load(path):
    spec = importlib.util.spec_from_file_location("impl", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


impl = _load(_TARGET)


# ---- visible cases -------------------------------------------------------
def test_hash_simple():
    salt = "random_salt"
    pwd = "password123"
    expected_digest = hashlib.sha256((salt + pwd).encode("utf-8")).hexdigest()
    expected_hash = f"{salt}${expected_digest}"
    assert impl.solve("hash", pwd, salt) == expected_hash


def test_verify_correct():
    salt = "s3cr3t_s4lt"
    pwd = "mySuperSecretPassword!"
    # Use direct computation to ensure we aren't relying on impl.solve for expected
    expected_digest = hashlib.sha256((salt + pwd).encode("utf-8")).hexdigest()
    stored_hash = f"{salt}${expected_digest}"
    assert impl.solve("verify", pwd, stored_hash) is True


def test_verify_incorrect():
    salt = "s3cr3t_s4lt"
    pwd = "mySuperSecretPassword!"
    expected_digest = hashlib.sha256((salt + pwd).encode("utf-8")).hexdigest()
    stored_hash = f"{salt}${expected_digest}"
    assert impl.solve("verify", "wrongPassword!", stored_hash) is False


# ---- hidden / edge cases -------------------------------------------------
def test_verify_invalid_format():
    assert impl.solve("verify", "password", "no_dollar_sign_here") is False


def test_empty_password_and_salt():
    salt = ""
    pwd = ""
    expected_digest = hashlib.sha256((salt + pwd).encode("utf-8")).hexdigest()
    expected_hash = f"{salt}${expected_digest}"
    assert impl.solve("hash", pwd, salt) == expected_hash
    assert impl.solve("verify", pwd, expected_hash) is True
