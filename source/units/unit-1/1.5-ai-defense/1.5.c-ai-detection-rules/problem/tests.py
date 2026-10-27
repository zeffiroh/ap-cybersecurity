"""Test suite for 1.5.c -- the blackbox acceptance contract.
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


def _fail(src, ts_list):
    """Helper: build login_fail events for src at given timestamps."""
    return [{"ts": t, "src": src, "event": "login_fail", "ok": False} for t in ts_list]


def _ok(src, ts):
    return {"ts": ts, "src": src, "event": "login_ok", "ok": True}


# ---- visible cases -------------------------------------------------------

def test_single_ip_exactly_threshold():
    logs = _fail("10.0.0.1", [0, 10, 20, 30, 40])
    result = impl.solve(logs)
    assert result == ["ALERT brute_force src=10.0.0.1 count=5 window=60s"]


def test_below_threshold_not_flagged():
    logs = _fail("10.0.0.2", [0, 30, 59])
    assert impl.solve(logs) == []


def test_empty_logs():
    assert impl.solve([]) == []


def test_two_ips_one_flagged():
    logs = _fail("192.168.1.1", [0, 5, 10, 15, 20]) + _fail("192.168.1.2", [0, 100])
    result = impl.solve(logs)
    assert result == ["ALERT brute_force src=192.168.1.1 count=5 window=60s"]


def test_login_ok_events_ignored():
    # 4 failures + many successes = should NOT trigger
    logs = _fail("172.16.0.1", [0, 10, 20, 30]) + [_ok("172.16.0.1", t) for t in range(100)]
    assert impl.solve(logs) == []


# ---- hidden / edge cases -------------------------------------------------

def test_window_boundary_inclusive():
    # Events at ts=0 and ts=59 are exactly 59 apart -- same 60-second window
    logs = _fail("10.1.1.1", [0, 10, 20, 30, 59])
    result = impl.solve(logs)
    assert result == ["ALERT brute_force src=10.1.1.1 count=5 window=60s"]


def test_window_boundary_exclusive():
    # Events at ts=0 and ts=60 are 60 apart -- outside the 60-second window
    # Only events 0..4 fit in window starting at 0 if last is ts=60
    # But only events ts=1..59 fit for window starting 1, etc.
    # With ts=[0,15,30,45,60]: window [0..59] covers [0,15,30,45] -> 4 only
    logs = _fail("10.1.1.2", [0, 15, 30, 45, 60])
    assert impl.solve(logs) == []


def test_two_ips_both_flagged_sorted():
    logs = _fail("203.0.113.5", [0, 1, 2, 3, 4]) + _fail("198.51.100.1", [100, 101, 102, 103, 104])
    result = impl.solve(logs)
    assert result == sorted(result)
    assert len(result) == 2
    assert "ALERT brute_force src=198.51.100.1 count=5 window=60s" in result
    assert "ALERT brute_force src=203.0.113.5 count=5 window=60s" in result


def test_count_reflects_max_window():
    # 7 events within 60s; count should be 7 not 5
    logs = _fail("10.2.2.2", [0, 5, 10, 15, 20, 25, 30])
    result = impl.solve(logs)
    assert result == ["ALERT brute_force src=10.2.2.2 count=7 window=60s"]


def test_events_spread_across_two_windows():
    # 3 in first window, 5 in second; only second triggers
    logs = _fail("10.3.3.3", [0, 20, 40, 100, 110, 120, 130, 140])
    result = impl.solve(logs)
    assert result == ["ALERT brute_force src=10.3.3.3 count=5 window=60s"]


def test_no_login_fail_events():
    logs = [_ok("10.4.4.4", t) for t in range(20)]
    assert impl.solve(logs) == []


def test_duplicate_timestamps():
    # 5 events at same timestamp -- all within 60s window
    logs = _fail("10.5.5.5", [50, 50, 50, 50, 50])
    result = impl.solve(logs)
    assert result == ["ALERT brute_force src=10.5.5.5 count=5 window=60s"]


def test_output_is_sorted():
    # Multiple IPs -- output must be lexicographically sorted
    ips = ["99.1.1.1", "10.0.0.1", "172.16.0.1"]
    logs = []
    for ip in ips:
        logs += _fail(ip, [0, 1, 2, 3, 4])
    result = impl.solve(logs)
    assert result == sorted(result)
    assert len(result) == 3


def test_exactly_four_failures_not_flagged():
    logs = _fail("10.6.6.6", [0, 10, 20, 30])
    assert impl.solve(logs) == []
