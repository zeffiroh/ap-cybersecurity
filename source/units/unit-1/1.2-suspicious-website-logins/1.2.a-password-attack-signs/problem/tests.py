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


def _e(ts, user, ok):
    return {"ts": ts, "user": user, "ok": ok}


def test_single_user_flagged():
    events = [
        _e(1000, "alice", False),
        _e(1010, "alice", False),
        _e(1020, "alice", False),
        _e(1030, "alice", False),
        _e(1040, "alice", False),
    ]
    assert impl.solve(events) == ["alice"]


def test_two_users_one_flagged():
    events = [
        _e(1000, "alice", False),
        _e(1010, "alice", False),
        _e(1020, "alice", False),
        _e(1030, "alice", False),
        _e(1040, "alice", False),
        _e(1000, "bob",   False),
        _e(1100, "bob",   False),
    ]
    assert impl.solve(events) == ["alice"]


def test_empty():
    assert impl.solve([]) == []


def test_all_successes_not_flagged():
    events = [_e(1000 + i * 5, "carol", True) for i in range(10)]
    assert impl.solve(events) == []


def test_exactly_four_failures_not_flagged():
    events = [_e(1000 + i * 10, "dave", False) for i in range(4)]
    assert impl.solve(events) == []


def test_window_boundary_exactly_60_not_flagged():
    events = [_e(i * 15, "eve", False) for i in range(5)]
    assert impl.solve(events) == []


def test_window_boundary_just_inside_flagged():
    events = [
        _e(0,  "frank", False),
        _e(15, "frank", False),
        _e(30, "frank", False),
        _e(45, "frank", False),
        _e(59, "frank", False),
    ]
    assert impl.solve(events) == ["frank"]


def test_unsorted_events_handled():
    events = [
        _e(1040, "grace", False),
        _e(1000, "grace", False),
        _e(1020, "grace", False),
        _e(1030, "grace", False),
        _e(1010, "grace", False),
    ]
    assert impl.solve(events) == ["grace"]


def test_success_in_middle_not_counted():
    events = [
        _e(1000, "henry", False),
        _e(1010, "henry", False),
        _e(1020, "henry", True),
        _e(1030, "henry", False),
        _e(1040, "henry", False),
    ]
    assert impl.solve(events) == []


def test_multiple_users_both_flagged_sorted():
    events = (
        [_e(2000 + i * 5, "zara", False) for i in range(5)] +
        [_e(3000 + i * 5, "alice", False) for i in range(5)]
    )
    result = impl.solve(events)
    assert result == ["alice", "zara"]
    assert result == sorted(result)


def test_second_window_triggers_flag():
    events = [
        _e(0,   "iris", False),
        _e(70,  "iris", False),
        _e(140, "iris", False),
        _e(210, "iris", False),
        _e(280, "iris", False),
        _e(400, "iris", False),
        _e(410, "iris", False),
        _e(420, "iris", False),
        _e(430, "iris", False),
        _e(440, "iris", False),
    ]
    assert impl.solve(events) == ["iris"]
