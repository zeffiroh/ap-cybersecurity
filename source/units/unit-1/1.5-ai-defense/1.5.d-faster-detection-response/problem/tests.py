"""Test suite for 1.5.d -- the blackbox acceptance contract.
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


def _inc(id_, detected, resolved, severity="high", auto=False):
    return {"id": id_, "detected_at": detected, "resolved_at": resolved,
            "severity": severity, "auto": auto}


# ---- visible cases -------------------------------------------------------

def test_empty_input():
    result = impl.solve([])
    assert result == {"mttr": 0.0, "auto_resolved": 0}


def test_single_incident_manual():
    result = impl.solve([_inc("INC-001", 1000, 1120, "critical", False)])
    assert result["mttr"] == 120.0
    assert result["auto_resolved"] == 0


def test_single_incident_auto():
    result = impl.solve([_inc("INC-002", 2000, 2060, "low", True)])
    assert result["mttr"] == 60.0
    assert result["auto_resolved"] == 1


def test_two_incidents_mean():
    incidents = [
        _inc("INC-003", 1000, 1120, "critical", False),  # 120s
        _inc("INC-004", 2000, 2080, "high", True),       # 80s
    ]
    result = impl.solve(incidents)
    assert result["mttr"] == 100.0
    assert result["auto_resolved"] == 1


def test_all_auto_resolved():
    incidents = [
        _inc("INC-005", 0, 30, "low", True),
        _inc("INC-006", 0, 60, "medium", True),
        _inc("INC-007", 0, 90, "high", True),
    ]
    result = impl.solve(incidents)
    assert result["mttr"] == 60.0
    assert result["auto_resolved"] == 3


# ---- hidden / edge cases -------------------------------------------------

def test_no_auto_resolved():
    incidents = [
        _inc("INC-010", 100, 700, "critical", False),  # 600s
        _inc("INC-011", 200, 500, "high", False),       # 300s
    ]
    result = impl.solve(incidents)
    assert result["mttr"] == 450.0
    assert result["auto_resolved"] == 0


def test_mttr_is_float():
    result = impl.solve([_inc("INC-020", 0, 100, "medium", False)])
    assert isinstance(result["mttr"], float)


def test_auto_resolved_is_int():
    result = impl.solve([_inc("INC-021", 0, 50, "low", True)])
    assert isinstance(result["auto_resolved"], int)


def test_result_has_exactly_two_keys():
    result = impl.solve([_inc("INC-030", 0, 200)])
    assert set(result.keys()) == {"mttr", "auto_resolved"}


def test_non_integer_mean():
    # 3 incidents with response times 10, 20, 30 -> mean = 20.0 (exact)
    incidents = [
        _inc("A", 0, 10),
        _inc("B", 0, 20),
        _inc("C", 0, 30),
    ]
    result = impl.solve(incidents)
    assert result["mttr"] == 20.0


def test_fractional_mean():
    # 2 incidents: 10s and 11s -> mean = 10.5
    incidents = [
        _inc("X", 1000, 1010),
        _inc("Y", 2000, 2011),
    ]
    result = impl.solve(incidents)
    assert result["mttr"] == 10.5


def test_large_dataset():
    # 100 incidents, all 300s response time, 50 auto -> mttr=300.0, auto=50
    incidents = [_inc(f"INC-{i}", i * 1000, i * 1000 + 300, "high", i % 2 == 0)
                 for i in range(100)]
    result = impl.solve(incidents)
    assert result["mttr"] == 300.0
    assert result["auto_resolved"] == 50


def test_mixed_severities_all_auto():
    incidents = [
        _inc("M1", 0, 45, "low", True),
        _inc("M2", 0, 45, "medium", True),
        _inc("M3", 0, 45, "high", True),
        _inc("M4", 0, 45, "critical", False),
    ]
    result = impl.solve(incidents)
    assert result["mttr"] == 45.0
    assert result["auto_resolved"] == 3
