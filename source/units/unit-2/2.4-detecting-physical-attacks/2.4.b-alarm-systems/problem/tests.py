"""Test suite for 2.4.b — the blackbox acceptance contract.
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

BASE = 1_700_000_000


def _e(ts, zone, sensor, arm_state, since_armed_sec):
    return {
        "ts": ts,
        "zone": zone,
        "sensor": sensor,
        "arm_state": arm_state,
        "since_armed_sec": since_armed_sec,
    }


# ---- visible cases -------------------------------------------------------

def test_false_alarm_inside_exit_delay():
    """Contact trip 10s after arming, well inside default 45s exit delay."""
    events = [_e(BASE, "front-door", "contact", "ARMED_AWAY", 10)]
    assert impl.solve(events) == ["FALSE_ALARM"]


def test_suppressed_when_disarmed():
    """Contact trip while disarmed is SUPPRESSED."""
    events = [_e(BASE, "back-window", "contact", "DISARMED", 0)]
    assert impl.solve(events) == ["SUPPRESSED"]


def test_panic_dispatch_even_disarmed():
    """Panic button always DISPATCH, even when arm_state is DISARMED."""
    events = [_e(BASE, "reception", "panic", "DISARMED", 0)]
    assert impl.solve(events) == ["DISPATCH"]


def test_real_trip_no_corroboration_local_only():
    """A real trip alone in the batch, past exit delay, with no other zone -> LOCAL_ONLY."""
    events = [_e(BASE, "garage", "glass_break", "ARMED_AWAY", 900)]
    assert impl.solve(events) == ["LOCAL_ONLY"]


def test_cross_zone_verification_dispatch():
    """Two real trips in different zones within verify_window_sec -> both DISPATCH."""
    events = [
        _e(BASE, "z1", "contact", "ARMED_AWAY", 300),
        _e(BASE + 50, "z2", "glass_break", "ARMED_AWAY", 305),
    ]
    assert impl.solve(events) == ["DISPATCH", "DISPATCH"]


def test_same_zone_repeats_do_not_corroborate():
    """Two real trips in the SAME zone within the window do not verify each other."""
    events = [
        _e(BASE, "z1", "contact", "ARMED_AWAY", 300),
        _e(BASE + 50, "z1", "contact", "ARMED_AWAY", 305),
    ]
    assert impl.solve(events) == ["LOCAL_ONLY", "LOCAL_ONLY"]


def test_empty_events():
    """Empty stream returns empty list."""
    assert impl.solve([]) == []


def test_mixed_batch_order_preserved():
    """Output order matches input order, not chronological or classification order."""
    events = [
        _e(BASE + 1000, "z9", "glass_break", "ARMED_AWAY", 900),   # LOCAL_ONLY (alone)
        _e(BASE, "front-door", "contact", "ARMED_AWAY", 5),        # FALSE_ALARM
        _e(BASE + 2000, "vault", "panic", "ARMED_STAY", 0),        # DISPATCH
    ]
    assert impl.solve(events) == ["LOCAL_ONLY", "FALSE_ALARM", "DISPATCH"]


# ---- hidden / edge cases -------------------------------------------------

def test_boundary_exit_delay_below_is_false_alarm():
    """44s (one below default 45s exit_delay_sec) is still FALSE_ALARM."""
    events = [_e(BASE, "lobby", "contact", "ARMED_AWAY", 44)]
    assert impl.solve(events) == ["FALSE_ALARM"]


def test_boundary_exit_delay_at_threshold_is_real():
    """Exactly 45s (== exit_delay_sec) counts as past the exit delay -> real trip -> LOCAL_ONLY alone."""
    events = [_e(BASE, "server-room", "contact", "ARMED_AWAY", 45)]
    assert impl.solve(events) == ["LOCAL_ONLY"]


def test_boundary_verify_window_exactly_at_limit():
    """Gap of exactly verify_window_sec (120s default) between different zones still verifies."""
    events = [
        _e(BASE, "a1", "contact", "ARMED_AWAY", 200),
        _e(BASE + 120, "a2", "contact", "ARMED_AWAY", 200),
    ]
    assert impl.solve(events) == ["DISPATCH", "DISPATCH"]


def test_boundary_verify_window_one_second_beyond():
    """Gap of verify_window_sec + 1 does NOT verify; both LOCAL_ONLY."""
    events = [
        _e(BASE, "b1", "contact", "ARMED_AWAY", 200),
        _e(BASE + 121, "b2", "contact", "ARMED_AWAY", 200),
    ]
    assert impl.solve(events) == ["LOCAL_ONLY", "LOCAL_ONLY"]


def test_armed_stay_treated_same_as_armed_away():
    """ARMED_STAY follows the same exit-delay / real-trip logic as ARMED_AWAY."""
    events = [_e(BASE, "side-door", "contact", "ARMED_STAY", 10)]
    assert impl.solve(events) == ["FALSE_ALARM"]


def test_custom_exit_delay_and_verify_window_params():
    """Custom exit_delay_sec / verify_window_sec parameters are respected."""
    events = [_e(BASE, "z1", "contact", "ARMED_AWAY", 20)]
    # with exit_delay_sec=15, 20s since armed is now a real trip (alone -> LOCAL_ONLY)
    assert impl.solve(events, exit_delay_sec=15) == ["LOCAL_ONLY"]
    # with default exit_delay_sec=45, 20s is still inside grace period
    assert impl.solve(events) == ["FALSE_ALARM"]

    events2 = [
        _e(BASE, "c1", "contact", "ARMED_AWAY", 300),
        _e(BASE + 100, "c2", "contact", "ARMED_AWAY", 300),
    ]
    # default verify_window_sec=120 -> corroborates
    assert impl.solve(events2) == ["DISPATCH", "DISPATCH"]
    # tighter verify_window_sec=50 -> does not corroborate
    assert impl.solve(events2, verify_window_sec=50) == ["LOCAL_ONLY", "LOCAL_ONLY"]


def test_panic_ignores_since_armed_and_does_not_need_corroboration():
    """A panic button trip alone in the batch, mid-exit-delay, still DISPATCHes."""
    events = [_e(BASE, "vault", "panic", "ARMED_AWAY", 2)]
    assert impl.solve(events) == ["DISPATCH"]


def test_three_zone_batch_one_isolated():
    """Two zones corroborate each other; a third isolated zone stays LOCAL_ONLY."""
    events = [
        _e(BASE, "x1", "contact", "ARMED_AWAY", 300),
        _e(BASE + 10, "x2", "glass_break", "ARMED_AWAY", 300),
        _e(BASE + 10000, "x3", "contact", "ARMED_AWAY", 300),
    ]
    assert impl.solve(events) == ["DISPATCH", "DISPATCH", "LOCAL_ONLY"]
