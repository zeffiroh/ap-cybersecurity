"""Test suite for 5.1.c — the blackbox acceptance contract.
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


# ---- visible cases -------------------------------------------------------
def test_owner_allowed():
    req = {"user_id": "u1", "role": "user", "object_id": "482"}
    own = {"482": "u1"}
    assert impl.solve(req, own) == {"allowed": True, "reason": "owner"}


def test_non_owner_denied():
    req = {"user_id": "u1", "role": "user", "object_id": "483"}
    own = {"483": "u2"}
    assert impl.solve(req, own) == {"allowed": False, "reason": "not_owner"}


def test_admin_allowed():
    req = {"user_id": "u9", "role": "admin", "object_id": "483"}
    own = {"483": "u2"}
    assert impl.solve(req, own) == {"allowed": True, "reason": "admin"}


def test_not_found():
    req = {"user_id": "u1", "role": "user", "object_id": "999"}
    own = {"483": "u2"}
    assert impl.solve(req, own) == {"allowed": False, "reason": "not_found"}


# ---- hidden / edge cases -------------------------------------------------
def test_owner_priority_over_admin_role():
    req = {"user_id": "u1", "role": "admin", "object_id": "482"}
    own = {"482": "u1"}
    assert impl.solve(req, own) == {"allowed": True, "reason": "owner"}


def test_not_found_checked_before_role():
    req = {"user_id": "u1", "role": "admin", "object_id": "does_not_exist"}
    own = {"482": "u1"}
    assert impl.solve(req, own) == {"allowed": False, "reason": "not_found"}


def test_empty_ownership():
    req = {"user_id": "u1", "role": "user", "object_id": "482"}
    assert impl.solve(req, {}) == {"allowed": False, "reason": "not_found"}
