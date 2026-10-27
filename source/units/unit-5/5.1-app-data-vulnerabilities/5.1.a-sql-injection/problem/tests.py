"""Test suite for 5.1.a, the blackbox acceptance contract.

The SAME tests grade any implementation, loaded via the IMPL env var:
  - solution.py  (parameterized, must be green)
  - starter.py   (vulnerable concatenation, must be red: injections authenticate)
The injection cases are the point: they pass only when the query is parameterized.
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

USERS = [
    ("admin", "administrator", "S3cr3t-Admin-Pw"),
    ("jordan", "staff", "autumn-maple-31"),
    ("priya", "staff", "river-stone-77"),
]


# ---- legitimate logins still work ---------------------------------------
def test_valid_admin():
    assert impl.authenticate(USERS, "admin", "S3cr3t-Admin-Pw") == "administrator"


def test_valid_staff():
    assert impl.authenticate(USERS, "jordan", "autumn-maple-31") == "staff"


def test_wrong_password_rejected():
    assert impl.authenticate(USERS, "admin", "not-the-password") is None


def test_unknown_user_rejected():
    assert impl.authenticate(USERS, "nobody", "whatever") is None


# ---- injection must NOT authenticate (only parameterization passes these) ----
def test_comment_truncation_blocked():
    assert impl.authenticate(USERS, "admin'--", "anything") is None


def test_or_bypass_blocked():
    assert impl.authenticate(USERS, "' OR '1'='1", "x") is None


def test_or_bypass_with_comment_blocked():
    assert impl.authenticate(USERS, "' OR '1'='1'--", "x") is None


def test_union_blocked():
    assert impl.authenticate(USERS, "' UNION SELECT role FROM users--", "x") is None


# ---- a password field carrying an injection is also treated as data ----
def test_injection_in_password_blocked():
    assert impl.authenticate(USERS, "admin", "' OR '1'='1") is None


# ---- a legitimate but unusual username with a quote is handled literally ----
def test_literal_quote_username():
    users = USERS + [("o'brien", "staff", "pw-123")]
    assert impl.authenticate(users, "o'brien", "pw-123") == "staff"
    assert impl.authenticate(users, "o'brien", "wrong") is None


def test_empty_users():
    assert impl.authenticate([], "admin", "x") is None
