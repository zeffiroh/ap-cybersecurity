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

BASE = 1_700_000_000


def _e(ts, zone, sensor, arm_state, since_armed_sec):
    return {
        "ts": ts,
        "zone": zone,
        "sensor": sensor,
        "arm_state": arm_state,
        "since_armed_sec": since_armed_sec,
    }


def test_false_alarm_inside_exit_delay():
    events = [_e(BASE, "front-door", "contact", "ARMED_AWAY", 10)]
    assert impl.solve(events) == ["FALSE_ALARM"]


def test_suppressed_when_disarmed():
    events = [_e(BASE, "back-window", "contact", "DISARMED", 0)]
    assert impl.solve(events) == ["SUPPRESSED"]


def test_panic_dispatch_even_disarmed():
    events = [_e(BASE, "reception", "panic", "DISARMED", 0)]
    assert impl.solve(events) == ["DISPATCH"]


def test_real_trip_no_corroboration_local_only():
    events = [_e(BASE, "garage", "glass_break", "ARMED_AWAY", 900)]
    assert impl.solve(events) == ["LOCAL_ONLY"]


def test_cross_zone_verification_dispatch():
    events = [
        _e(BASE, "z1", "contact", "ARMED_AWAY", 300),
        _e(BASE + 50, "z2", "glass_break", "ARMED_AWAY", 305),
    ]
    assert impl.solve(events) == ["DISPATCH", "DISPATCH"]


def test_same_zone_repeats_do_not_corroborate():
    events = [
        _e(BASE, "z1", "contact", "ARMED_AWAY", 300),
        _e(BASE + 50, "z1", "contact", "ARMED_AWAY", 305),
    ]
    assert impl.solve(events) == ["LOCAL_ONLY", "LOCAL_ONLY"]


def test_empty_events():
    assert impl.solve([]) == []


def test_mixed_batch_order_preserved():
    events = [
        _e(BASE + 1000, "z9", "glass_break", "ARMED_AWAY", 900),
        _e(BASE, "front-door", "contact", "ARMED_AWAY", 5),
        _e(BASE + 2000, "vault", "panic", "ARMED_STAY", 0),
    ]
    assert impl.solve(events) == ["LOCAL_ONLY", "FALSE_ALARM", "DISPATCH"]


def test_boundary_exit_delay_below_is_false_alarm():
    events = [_e(BASE, "lobby", "contact", "ARMED_AWAY", 44)]
    assert impl.solve(events) == ["FALSE_ALARM"]


def test_boundary_exit_delay_at_threshold_is_real():
    events = [_e(BASE, "server-room", "contact", "ARMED_AWAY", 45)]
    assert impl.solve(events) == ["LOCAL_ONLY"]


def test_boundary_verify_window_exactly_at_limit():
    events = [
        _e(BASE, "a1", "contact", "ARMED_AWAY", 200),
        _e(BASE + 120, "a2", "contact", "ARMED_AWAY", 200),
    ]
    assert impl.solve(events) == ["DISPATCH", "DISPATCH"]


def test_boundary_verify_window_one_second_beyond():
    events = [
        _e(BASE, "b1", "contact", "ARMED_AWAY", 200),
        _e(BASE + 121, "b2", "contact", "ARMED_AWAY", 200),
    ]
    assert impl.solve(events) == ["LOCAL_ONLY", "LOCAL_ONLY"]


def test_armed_stay_treated_same_as_armed_away():
    events = [_e(BASE, "side-door", "contact", "ARMED_STAY", 10)]
    assert impl.solve(events) == ["FALSE_ALARM"]


def test_custom_exit_delay_and_verify_window_params():
    events = [_e(BASE, "z1", "contact", "ARMED_AWAY", 20)]
    assert impl.solve(events, exit_delay_sec=15) == ["LOCAL_ONLY"]
    assert impl.solve(events) == ["FALSE_ALARM"]

    events2 = [
        _e(BASE, "c1", "contact", "ARMED_AWAY", 300),
        _e(BASE + 100, "c2", "contact", "ARMED_AWAY", 300),
    ]
    assert impl.solve(events2) == ["DISPATCH", "DISPATCH"]
    assert impl.solve(events2, verify_window_sec=50) == ["LOCAL_ONLY", "LOCAL_ONLY"]


def test_panic_ignores_since_armed_and_does_not_need_corroboration():
    events = [_e(BASE, "vault", "panic", "ARMED_AWAY", 2)]
    assert impl.solve(events) == ["DISPATCH"]


def test_three_zone_batch_one_isolated():
    events = [
        _e(BASE, "x1", "contact", "ARMED_AWAY", 300),
        _e(BASE + 10, "x2", "glass_break", "ARMED_AWAY", 300),
        _e(BASE + 10000, "x3", "contact", "ARMED_AWAY", 300),
    ]
    assert impl.solve(events) == ["DISPATCH", "DISPATCH", "LOCAL_ONLY"]
