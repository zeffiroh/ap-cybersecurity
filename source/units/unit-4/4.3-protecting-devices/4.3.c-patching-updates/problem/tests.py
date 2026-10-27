"""Test suite for 4.3.c — the blackbox acceptance contract.
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
def test_example_1_emergency_exploited_internet_facing():
    vulns = [{"id": "V1", "cvss": 9.1, "exploited_in_wild": True,
              "internet_facing": True, "end_of_life": False}]
    assert impl.solve(vulns) == [{"id": "V1", "urgency": "emergency"}]


def test_example_2_compensate_end_of_life_overrides_severity():
    vulns = [{"id": "V2", "cvss": 8.8, "exploited_in_wild": False,
              "internet_facing": False, "end_of_life": True}]
    assert impl.solve(vulns) == [{"id": "V2", "urgency": "compensate"}]


def test_example_3_routine_low_severity():
    vulns = [{"id": "V3", "cvss": 4.2, "exploited_in_wild": False,
              "internet_facing": False, "end_of_life": False}]
    assert impl.solve(vulns) == [{"id": "V3", "urgency": "routine"}]


# ---- hidden / edge cases -------------------------------------------------
def test_edge_empty_list():
    assert impl.solve([]) == []


def test_critical_internal_is_scheduled_not_emergency():
    vulns = [{"id": "V4", "cvss": 9.8, "exploited_in_wild": False,
              "internet_facing": False, "end_of_life": False}]
    assert impl.solve(vulns) == [{"id": "V4", "urgency": "scheduled"}]


def test_critical_internet_facing_not_yet_exploited_is_emergency():
    vulns = [{"id": "V5", "cvss": 9.0, "exploited_in_wild": False,
              "internet_facing": True, "end_of_life": False}]
    assert impl.solve(vulns) == [{"id": "V5", "urgency": "emergency"}]


def test_moderate_severity_internet_facing_is_scheduled():
    vulns = [{"id": "V6", "cvss": 7.5, "exploited_in_wild": False,
              "internet_facing": True, "end_of_life": False}]
    assert impl.solve(vulns) == [{"id": "V6", "urgency": "scheduled"}]


def test_moderate_severity_internal_is_routine():
    vulns = [{"id": "V7", "cvss": 7.0, "exploited_in_wild": False,
              "internet_facing": False, "end_of_life": False}]
    assert impl.solve(vulns) == [{"id": "V7", "urgency": "routine"}]


def test_end_of_life_overrides_exploited_and_internet_facing():
    vulns = [{"id": "V8", "cvss": 10.0, "exploited_in_wild": True,
              "internet_facing": True, "end_of_life": True}]
    assert impl.solve(vulns) == [{"id": "V8", "urgency": "compensate"}]


def test_boundary_cvss_exactly_seven_internet_facing():
    vulns = [{"id": "V9", "cvss": 7.0, "exploited_in_wild": False,
              "internet_facing": True, "end_of_life": False}]
    assert impl.solve(vulns) == [{"id": "V9", "urgency": "scheduled"}]


def test_boundary_cvss_just_below_seven_internet_facing_is_routine():
    vulns = [{"id": "V10", "cvss": 6.9, "exploited_in_wild": False,
              "internet_facing": True, "end_of_life": False}]
    assert impl.solve(vulns) == [{"id": "V10", "urgency": "routine"}]


def test_order_preserved_and_multiple_entries():
    vulns = [
        {"id": "A", "cvss": 2.0, "exploited_in_wild": False,
         "internet_facing": False, "end_of_life": False},
        {"id": "B", "cvss": 9.9, "exploited_in_wild": True,
         "internet_facing": True, "end_of_life": False},
        {"id": "C", "cvss": 5.0, "exploited_in_wild": False,
         "internet_facing": False, "end_of_life": True},
    ]
    assert impl.solve(vulns) == [
        {"id": "A", "urgency": "routine"},
        {"id": "B", "urgency": "emergency"},
        {"id": "C", "urgency": "compensate"},
    ]
