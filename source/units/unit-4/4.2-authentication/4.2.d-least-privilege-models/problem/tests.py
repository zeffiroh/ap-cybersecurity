"""Test suite for 4.2.d — the blackbox acceptance contract.
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
def test_example_1_marketing_intern_no_justification():
    req = {"current_role": "Marketing Intern", "requested_access": "prod-db-write",
           "justification_present": False, "time_bound": False,
           "last_reviewed_days_ago": 10}
    assert impl.solve(req) == "deny_no_justification"


def test_example_2_hr_privilege_creep():
    req = {"current_role": "HR Analyst", "requested_access": "payroll-admin",
           "justification_present": True, "time_bound": False,
           "last_reviewed_days_ago": 800}
    assert impl.solve(req) == "flag_privilege_creep"


def test_example_3_oncall_time_bound():
    req = {"current_role": "On-call Engineer", "requested_access": "prod-ssh",
           "justification_present": True, "time_bound": True,
           "last_reviewed_days_ago": 5}
    assert impl.solve(req) == "approve_time_bound"


def test_example_4_plain_approve():
    req = {"current_role": "Analyst", "requested_access": "reporting-read",
           "justification_present": True, "time_bound": False,
           "last_reviewed_days_ago": 30}
    assert impl.solve(req) == "approve"


# ---- hidden / edge cases -------------------------------------------------
def test_boundary_exactly_365_is_not_stale():
    req = {"current_role": "Analyst", "requested_access": "reporting-read",
           "justification_present": True, "time_bound": False,
           "last_reviewed_days_ago": 365}
    assert impl.solve(req) == "approve"


def test_boundary_366_is_stale():
    req = {"current_role": "Analyst", "requested_access": "reporting-read",
           "justification_present": True, "time_bound": False,
           "last_reviewed_days_ago": 366}
    assert impl.solve(req) == "flag_privilege_creep"


def test_priority_no_justification_beats_privilege_creep():
    # justification_present False AND last_reviewed_days_ago > 365:
    # rule 1 is checked first, so deny_no_justification wins.
    req = {"current_role": "HR Analyst", "requested_access": "payroll-admin",
           "justification_present": False, "time_bound": False,
           "last_reviewed_days_ago": 900}
    assert impl.solve(req) == "deny_no_justification"


def test_priority_privilege_creep_beats_time_bound():
    req = {"current_role": "Contractor", "requested_access": "prod-ssh",
           "justification_present": True, "time_bound": True,
           "last_reviewed_days_ago": 400}
    assert impl.solve(req) == "flag_privilege_creep"


def test_missing_justification_key_defaults_false():
    req = {"current_role": "Intern", "requested_access": "prod-db-write",
           "time_bound": False, "last_reviewed_days_ago": 10}
    assert impl.solve(req) == "deny_no_justification"


def test_missing_time_bound_and_review_keys_default_to_approve():
    req = {"current_role": "Analyst", "requested_access": "reporting-read",
           "justification_present": True}
    assert impl.solve(req) == "approve"


def test_time_bound_none_treated_as_false():
    req = {"current_role": "Analyst", "requested_access": "reporting-read",
           "justification_present": True, "time_bound": None,
           "last_reviewed_days_ago": 5}
    assert impl.solve(req) == "approve"
