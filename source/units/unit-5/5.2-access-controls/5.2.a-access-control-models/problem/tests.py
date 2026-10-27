"""Test suite for 5.2.a — the blackbox acceptance contract.
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
def test_dac_owner():
    req = {"subject": {"name": "alice"}, "object": {"model": "dac", "owner": "alice", "grants": {}}, "action": "read"}
    assert impl.solve(req) == {"allowed": True, "reason": "owner"}


def test_dac_granted():
    req = {"subject": {"name": "bob"}, "object": {"model": "dac", "owner": "alice", "grants": {"read": ["bob"]}}, "action": "read"}
    assert impl.solve(req) == {"allowed": True, "reason": "granted"}


def test_dac_denied():
    req = {"subject": {"name": "eve"}, "object": {"model": "dac", "owner": "alice", "grants": {"read": ["bob"]}}, "action": "read"}
    assert impl.solve(req) == {"allowed": False, "reason": "dac_denied"}


def test_mac_sufficient():
    req = {"subject": {"clearance": "secret"}, "object": {"model": "mac", "classification": "confidential"}, "action": "read"}
    assert impl.solve(req) == {"allowed": True, "reason": "clearance_sufficient"}


def test_mac_insufficient():
    req = {"subject": {"clearance": "confidential"}, "object": {"model": "mac", "classification": "secret"}, "action": "read"}
    assert impl.solve(req) == {"allowed": False, "reason": "clearance_insufficient"}


def test_rbac_role_match():
    req = {"subject": {"roles": ["nurse"]}, "object": {"model": "rbac", "allowed_roles": {"read": ["nurse", "admin"]}}, "action": "read"}
    assert impl.solve(req) == {"allowed": True, "reason": "role_match"}


def test_rbac_denied():
    req = {"subject": {"roles": ["intern"]}, "object": {"model": "rbac", "allowed_roles": {"read": ["nurse", "admin"]}}, "action": "read"}
    assert impl.solve(req) == {"allowed": False, "reason": "rbac_denied"}


# ---- hidden / edge cases -------------------------------------------------
def test_unknown_model():
    req = {"subject": {}, "object": {"model": "abac"}, "action": "read"}
    assert impl.solve(req) == {"allowed": False, "reason": "unknown_model"}


def test_mac_equal_level_allowed():
    req = {"subject": {"clearance": "top_secret"}, "object": {"model": "mac", "classification": "top_secret"}, "action": "read"}
    assert impl.solve(req) == {"allowed": True, "reason": "clearance_sufficient"}


def test_dac_owner_priority_over_grants():
    req = {"subject": {"name": "alice"}, "object": {"model": "dac", "owner": "alice", "grants": {"read": []}}, "action": "read"}
    assert impl.solve(req) == {"allowed": True, "reason": "owner"}


def test_rbac_multiple_roles_one_matches():
    req = {"subject": {"roles": ["intern", "admin"]}, "object": {"model": "rbac", "allowed_roles": {"write": ["admin"]}}, "action": "write"}
    assert impl.solve(req) == {"allowed": True, "reason": "role_match"}
