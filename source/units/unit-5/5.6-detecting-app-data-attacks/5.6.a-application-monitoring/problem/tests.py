"""Test suite for 5.6.a — the blackbox acceptance contract.
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
def test_brute_force_flagged():
    entries = [
        {"ip": "10.0.0.1", "ts": 0, "status": 401},
        {"ip": "10.0.0.1", "ts": 10, "status": 401},
        {"ip": "10.0.0.1", "ts": 20, "status": 401},
        {"ip": "10.0.0.1", "ts": 30, "status": 401},
        {"ip": "10.0.0.1", "ts": 40, "status": 401},
    ]
    assert impl.solve(entries, threshold=5, window_seconds=60) == ["10.0.0.1"]


def test_successful_logins_not_counted():
    entries = [
        {"ip": "10.0.0.2", "ts": 0, "status": 200},
        {"ip": "10.0.0.2", "ts": 1, "status": 200},
        {"ip": "10.0.0.2", "ts": 2, "status": 200},
    ]
    assert impl.solve(entries, threshold=2, window_seconds=60) == []


def test_below_threshold_not_flagged():
    entries = [
        {"ip": "10.0.0.3", "ts": 0, "status": 401},
        {"ip": "10.0.0.3", "ts": 5, "status": 401},
    ]
    assert impl.solve(entries, threshold=5, window_seconds=60) == []


def test_multiple_ips_flagged_sorted():
    entries = [
        {"ip": "10.0.0.9", "ts": 0, "status": 401},
        {"ip": "10.0.0.9", "ts": 1, "status": 401},
        {"ip": "10.0.0.5", "ts": 0, "status": 401},
        {"ip": "10.0.0.5", "ts": 1, "status": 401},
    ]
    assert impl.solve(entries, threshold=2, window_seconds=60) == ["10.0.0.5", "10.0.0.9"]


def test_events_too_far_apart_not_flagged():
    entries = [
        {"ip": "10.0.0.4", "ts": 0, "status": 401},
        {"ip": "10.0.0.4", "ts": 120, "status": 401},
    ]
    assert impl.solve(entries, threshold=2, window_seconds=60) == []


# ---- hidden / edge cases -------------------------------------------------
def test_window_boundary_inclusive():
    entries = [
        {"ip": "10.0.0.6", "ts": 0, "status": 401},
        {"ip": "10.0.0.6", "ts": 60, "status": 401},
    ]
    assert impl.solve(entries, threshold=2, window_seconds=60) == ["10.0.0.6"]


def test_unsorted_input():
    entries = [
        {"ip": "10.0.0.7", "ts": 40, "status": 401},
        {"ip": "10.0.0.7", "ts": 0, "status": 401},
        {"ip": "10.0.0.7", "ts": 20, "status": 401},
    ]
    assert impl.solve(entries, threshold=3, window_seconds=60) == ["10.0.0.7"]


def test_mixed_status_only_401_counts():
    entries = [
        {"ip": "10.0.0.8", "ts": 0, "status": 401},
        {"ip": "10.0.0.8", "ts": 1, "status": 200},
        {"ip": "10.0.0.8", "ts": 2, "status": 403},
        {"ip": "10.0.0.8", "ts": 3, "status": 401},
    ]
    assert impl.solve(entries, threshold=2, window_seconds=60) == ["10.0.0.8"]


def test_empty_entries():
    assert impl.solve([], threshold=1, window_seconds=60) == []
