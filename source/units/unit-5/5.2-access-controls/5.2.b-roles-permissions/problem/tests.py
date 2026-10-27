"""Test suite for 5.2.b — the blackbox acceptance contract.
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
def test_dana_has_excess():
    roles = {"support": ["read_ticket", "write_ticket_reply"], "billing": ["read_invoice", "issue_refund"]}
    user_roles = {"dana": ["support", "billing"]}
    job_requirements = {"dana": ["read_ticket", "write_ticket_reply"]}
    assert impl.solve(roles, user_roles, job_requirements) == {"dana": ["issue_refund", "read_invoice"]}


def test_sam_no_excess_omitted():
    roles = {"support": ["read_ticket"]}
    user_roles = {"sam": ["support"]}
    job_requirements = {"sam": ["read_ticket"]}
    assert impl.solve(roles, user_roles, job_requirements) == {}


def test_multiple_users_mixed():
    roles = {"support": ["read_ticket", "write_ticket_reply"], "admin": ["delete_user", "read_ticket"]}
    user_roles = {"a": ["support"], "b": ["admin"]}
    job_requirements = {"a": ["read_ticket", "write_ticket_reply"], "b": ["read_ticket"]}
    assert impl.solve(roles, user_roles, job_requirements) == {"b": ["delete_user"]}


# ---- hidden / edge cases -------------------------------------------------
def test_user_with_no_roles():
    roles = {"support": ["read_ticket"]}
    user_roles = {"ghost": []}
    job_requirements = {"ghost": []}
    assert impl.solve(roles, user_roles, job_requirements) == {}


def test_user_missing_from_job_requirements_treated_as_none_required():
    roles = {"support": ["read_ticket"]}
    user_roles = {"newhire": ["support"]}
    job_requirements = {}
    assert impl.solve(roles, user_roles, job_requirements) == {"newhire": ["read_ticket"]}


def test_overlapping_roles_deduplicated():
    roles = {"r1": ["p1", "p2"], "r2": ["p2", "p3"]}
    user_roles = {"u": ["r1", "r2"]}
    job_requirements = {"u": ["p1", "p2", "p3"]}
    assert impl.solve(roles, user_roles, job_requirements) == {}


def test_empty_inputs():
    assert impl.solve({}, {}, {}) == {}
