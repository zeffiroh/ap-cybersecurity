"""Test suite for 2.3.a — the blackbox acceptance contract.
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
def test_example_1():
    # Scenario A from activity.md
    facility = {
        "keyed_lock": True,
        "badge_reader": True,
        "biometric_reader": False,
        "mantrap": False,
        "cctv": True,
        "security_guard": False
    }
    expected = ["no_identity_verification", "no_tailgating_prevention"]
    assert impl.solve(facility) == expected


def test_example_2():
    # Scenario B from activity.md
    facility = {
        "keyed_lock": False,
        "badge_reader": False,
        "biometric_reader": False,
        "mantrap": True,
        "cctv": False,
        "security_guard": True
    }
    expected = ["no_electronic_access", "no_key_control", "no_visual_monitoring"]
    assert impl.solve(facility) == expected


# ---- hidden / edge cases -------------------------------------------------
def test_edge_all_present():
    facility = {
        "keyed_lock": True,
        "badge_reader": True,
        "biometric_reader": True,
        "mantrap": True,
        "cctv": True,
        "security_guard": True
    }
    assert impl.solve(facility) == []


def test_edge_all_absent():
    facility = {
        "keyed_lock": False,
        "badge_reader": False,
        "biometric_reader": False,
        "mantrap": False,
        "cctv": False,
        "security_guard": False
    }
    expected = [
        "no_electronic_access",
        "no_identity_verification",
        "no_key_control",
        "no_tailgating_prevention",
        "no_visual_monitoring"
    ]
    assert impl.solve(facility) == expected

