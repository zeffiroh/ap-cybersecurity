"""Test suite for 5.2.c — the blackbox acceptance contract.
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
def test_lateral_movement_flagged():
    events = [
        {"account": "mkt_dana", "host": "h1", "ts": 0},
        {"account": "mkt_dana", "host": "h2", "ts": 2},
        {"account": "mkt_dana", "host": "h3", "ts": 4},
        {"account": "svc_backup", "host": "h9", "ts": 0},
    ]
    assert impl.solve(events, threshold=3, window_minutes=5) == ["mkt_dana"]


def test_too_far_apart_not_flagged():
    events = [
        {"account": "alice", "host": "h1", "ts": 0},
        {"account": "alice", "host": "h2", "ts": 100},
    ]
    assert impl.solve(events, threshold=2, window_minutes=5) == []


def test_same_host_repeated_not_counted_twice():
    events = [
        {"account": "bob", "host": "h1", "ts": 0},
        {"account": "bob", "host": "h1", "ts": 1},
        {"account": "bob", "host": "h1", "ts": 2},
    ]
    assert impl.solve(events, threshold=2, window_minutes=5) == []


def test_multiple_accounts_flagged_sorted():
    events = [
        {"account": "zed", "host": "h1", "ts": 0},
        {"account": "zed", "host": "h2", "ts": 1},
        {"account": "amy", "host": "h3", "ts": 0},
        {"account": "amy", "host": "h4", "ts": 1},
    ]
    assert impl.solve(events, threshold=2, window_minutes=5) == ["amy", "zed"]


# ---- hidden / edge cases -------------------------------------------------
def test_window_boundary_inclusive():
    events = [
        {"account": "u", "host": "h1", "ts": 0},
        {"account": "u", "host": "h2", "ts": 5},
    ]
    assert impl.solve(events, threshold=2, window_minutes=5) == ["u"]


def test_window_boundary_exclusive_just_outside():
    events = [
        {"account": "u", "host": "h1", "ts": 0},
        {"account": "u", "host": "h2", "ts": 6},
    ]
    assert impl.solve(events, threshold=2, window_minutes=5) == []


def test_unsorted_input_events():
    events = [
        {"account": "u", "host": "h3", "ts": 4},
        {"account": "u", "host": "h1", "ts": 0},
        {"account": "u", "host": "h2", "ts": 2},
    ]
    assert impl.solve(events, threshold=3, window_minutes=5) == ["u"]


def test_empty_events():
    assert impl.solve([], threshold=1, window_minutes=5) == []
