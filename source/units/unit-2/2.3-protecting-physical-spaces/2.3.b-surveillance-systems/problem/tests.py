"""Test suite for 2.3.b — Surveillance systems: camera event log anomaly detection.

Blackbox acceptance contract. The SAME tests grade:
  - solution.py  (reference — must be ALL GREEN)
  - starter.py   (must be ALL RED until student implements)

Default target: solution.py.

Timestamp hour reference (UTC, hour = (ts % 86400) // 3600):
  ts=1700000000  ->  hour 22  (10 PM)
  ts=1700035200  ->  hour  8  ( 8 AM)
  ts=1700057600  ->  hour 14  ( 2 PM)
  ts=1700000100  ->  hour 22  (10 PM, 100 s after base)
  ts=1700000010  ->  hour 22  (10 PM, 10 s after base)
  ts=1700000020  ->  hour 22  (10 PM, 20 s after base)
  ts=1700000030  ->  hour 22  (10 PM, 30 s after base)
"""
import importlib.util
import os
import pathlib
import pytest

_HERE = pathlib.Path(__file__).parent
_TARGET = os.environ.get("IMPL", str(_HERE / "solution.py"))


def _load(path):
    spec = importlib.util.spec_from_file_location("impl", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


impl = _load(_TARGET)

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _ev(camera_id, ts, motion, person_detected, area, authorized_hours):
    return {
        "camera_id": camera_id,
        "ts": ts,
        "motion": motion,
        "person_detected": person_detected,
        "area": area,
        "authorized_hours": authorized_hours,
    }


# ---------------------------------------------------------------------------
# visible cases
# ---------------------------------------------------------------------------

def test_empty_input():
    """No events -> no alerts."""
    assert impl.solve([]) == []


def test_no_alerts_daytime_person():
    """Person detected during authorized hours, no motion-only streak -> no alerts."""
    events = [
        _ev("CAM-01", 1700035200, True, True, "lobby", (8, 18)),   # hour 8 -> authorized
        _ev("CAM-01", 1700057600, True, True, "lobby", (8, 18)),   # hour 14 -> authorized
    ]
    assert impl.solve(events) == []


def test_after_hours_single_camera():
    """Person detected at hour 22, authorized 8-18 -> AFTER_HOURS:CAM-01."""
    events = [
        _ev("CAM-01", 1700000000, True, True, "lobby", (8, 18)),   # hour 22 -> after hours
    ]
    assert impl.solve(events) == ["AFTER_HOURS:CAM-01"]


def test_after_hours_multiple_cameras():
    """Two cameras both detect persons after hours -> two AFTER_HOURS alerts."""
    events = [
        _ev("CAM-01", 1700000000, True, True, "lobby",       (8, 18)),  # hour 22
        _ev("CAM-02", 1700000100, True, True, "parking",     (6, 20)),  # hour 22
    ]
    assert impl.solve(events) == ["AFTER_HOURS:CAM-01", "AFTER_HOURS:CAM-02"]


def test_after_hours_deduplication():
    """Same camera triggers AFTER_HOURS twice -> only one alert entry."""
    events = [
        _ev("CAM-03", 1700000000, True, True, "lobby", (8, 18)),   # hour 22
        _ev("CAM-03", 1700000100, True, True, "lobby", (8, 18)),   # hour 22
    ]
    assert impl.solve(events) == ["AFTER_HOURS:CAM-03"]


def test_ghost_motion_exactly_three():
    """Exactly 3 consecutive motion=True, person=False on CAM-02 -> GHOST_MOTION:CAM-02."""
    events = [
        _ev("CAM-02", 1700035200, True,  False, "hallway", (8, 18)),
        _ev("CAM-02", 1700035260, True,  False, "hallway", (8, 18)),
        _ev("CAM-02", 1700035320, True,  False, "hallway", (8, 18)),
    ]
    assert impl.solve(events) == ["GHOST_MOTION:CAM-02"]


def test_ghost_motion_two_not_enough():
    """Only 2 consecutive ghost-motion events -> no alert."""
    events = [
        _ev("CAM-02", 1700035200, True,  False, "hallway", (8, 18)),
        _ev("CAM-02", 1700035260, True,  False, "hallway", (8, 18)),
        _ev("CAM-02", 1700035320, False, False, "hallway", (8, 18)),  # streak broken
    ]
    assert impl.solve(events) == []


def test_ghost_motion_streak_reset():
    """Streak broken by person_detected=True, then resumes but stays under 3 -> no alert."""
    events = [
        _ev("CAM-04", 1700035200, True,  False, "exit",    (8, 18)),
        _ev("CAM-04", 1700035260, True,  True,  "exit",    (8, 18)),  # breaks streak
        _ev("CAM-04", 1700035320, True,  False, "exit",    (8, 18)),
        _ev("CAM-04", 1700035380, True,  False, "exit",    (8, 18)),
    ]
    assert impl.solve(events) == []


def test_crowd_server_room_triggers():
    """3 person detections in server_room within 60 s -> CROWD_SERVER_ROOM."""
    events = [
        _ev("CAM-05", 1700000010, True, True, "server_room", (8, 18)),
        _ev("CAM-05", 1700000020, True, True, "server_room", (8, 18)),
        _ev("CAM-05", 1700000030, True, True, "server_room", (8, 18)),
    ]
    # All at hour 22, authorized 8-18 -> also AFTER_HOURS
    assert impl.solve(events) == ["AFTER_HOURS:CAM-05", "CROWD_SERVER_ROOM"]


def test_crowd_server_room_spread_out():
    """3 server_room persons but spread > 60 s apart -> no CROWD_SERVER_ROOM."""
    events = [
        _ev("CAM-05", 1700000000, True, True, "server_room", (0, 24)),
        _ev("CAM-05", 1700000070, True, True, "server_room", (0, 24)),
        _ev("CAM-05", 1700000140, True, True, "server_room", (0, 24)),
    ]
    assert impl.solve(events) == []


def test_combined_all_three_alerts():
    """Scenario that triggers all three distinct alert types."""
    events = [
        # AFTER_HOURS: hour 22, authorized 8-18
        _ev("CAM-01", 1700000000, True, True, "lobby", (8, 18)),
        # GHOST_MOTION: 3 consecutive on CAM-06
        _ev("CAM-06", 1700035200, True, False, "stairwell", (8, 18)),
        _ev("CAM-06", 1700035260, True, False, "stairwell", (8, 18)),
        _ev("CAM-06", 1700035320, True, False, "stairwell", (8, 18)),
        # CROWD_SERVER_ROOM: 3 within 60 s, all during hours (0,24)
        _ev("CAM-07", 1700057600,    True, True, "server_room", (0, 24)),
        _ev("CAM-07", 1700057620,    True, True, "server_room", (0, 24)),
        _ev("CAM-07", 1700057640,    True, True, "server_room", (0, 24)),
    ]
    result = impl.solve(events)
    assert "AFTER_HOURS:CAM-01" in result
    assert "GHOST_MOTION:CAM-06" in result
    assert "CROWD_SERVER_ROOM" in result
    assert result == sorted(result)          # must be sorted
    assert len(result) == len(set(result))   # must be de-duplicated


def test_output_is_sorted():
    """Output list must be lexicographically sorted."""
    events = [
        _ev("CAM-ZZ", 1700000000, True, True, "lobby",   (8, 18)),  # AFTER_HOURS:CAM-ZZ
        _ev("CAM-AA", 1700000100, True, True, "parking",  (8, 18)),  # AFTER_HOURS:CAM-AA
    ]
    result = impl.solve(events)
    assert result == sorted(result)
    assert result[0] == "AFTER_HOURS:CAM-AA"
    assert result[1] == "AFTER_HOURS:CAM-ZZ"
