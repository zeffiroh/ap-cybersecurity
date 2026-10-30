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
    return [{"ts": t, "src": src, "event": "login_fail", "ok": False} for t in ts_list]


def _ok(src, ts):
    return {"ts": ts, "src": src, "event": "login_ok", "ok": True}


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
    logs = _fail("172.16.0.1", [0, 10, 20, 30]) + [_ok("172.16.0.1", t) for t in range(100)]
    assert impl.solve(logs) == []


def test_window_boundary_inclusive():
    logs = _fail("10.1.1.1", [0, 10, 20, 30, 59])
    result = impl.solve(logs)
    assert result == ["ALERT brute_force src=10.1.1.1 count=5 window=60s"]


def test_window_boundary_exclusive():
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
    logs = _fail("10.2.2.2", [0, 5, 10, 15, 20, 25, 30])
    result = impl.solve(logs)
    assert result == ["ALERT brute_force src=10.2.2.2 count=7 window=60s"]


def test_events_spread_across_two_windows():
    logs = _fail("10.3.3.3", [0, 20, 40, 100, 110, 120, 130, 140])
    result = impl.solve(logs)
    assert result == ["ALERT brute_force src=10.3.3.3 count=5 window=60s"]


def test_no_login_fail_events():
    logs = [_ok("10.4.4.4", t) for t in range(20)]
    assert impl.solve(logs) == []


def test_duplicate_timestamps():
    logs = _fail("10.5.5.5", [50, 50, 50, 50, 50])
    result = impl.solve(logs)
    assert result == ["ALERT brute_force src=10.5.5.5 count=5 window=60s"]


def test_output_is_sorted():
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
