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


def _ev(camera_id, ts, motion, person_detected, area, authorized_hours):
    return {
        "camera_id": camera_id,
        "ts": ts,
        "motion": motion,
        "person_detected": person_detected,
        "area": area,
        "authorized_hours": authorized_hours,
    }


def test_empty_input():
    assert impl.solve([]) == []


def test_no_alerts_daytime_person():
    events = [
        _ev("CAM-01", 1700035200, True, True, "lobby", (8, 18)),
        _ev("CAM-01", 1700057600, True, True, "lobby", (8, 18)),
    ]
    assert impl.solve(events) == []


def test_after_hours_single_camera():
    events = [
        _ev("CAM-01", 1700000000, True, True, "lobby", (8, 18)),
    ]
    assert impl.solve(events) == ["AFTER_HOURS:CAM-01"]


def test_after_hours_multiple_cameras():
    events = [
        _ev("CAM-01", 1700000000, True, True, "lobby",       (8, 18)),
        _ev("CAM-02", 1700000100, True, True, "parking",     (6, 20)),
    ]
    assert impl.solve(events) == ["AFTER_HOURS:CAM-01", "AFTER_HOURS:CAM-02"]


def test_after_hours_deduplication():
    events = [
        _ev("CAM-03", 1700000000, True, True, "lobby", (8, 18)),
        _ev("CAM-03", 1700000100, True, True, "lobby", (8, 18)),
    ]
    assert impl.solve(events) == ["AFTER_HOURS:CAM-03"]


def test_ghost_motion_exactly_three():
    events = [
        _ev("CAM-02", 1700035200, True,  False, "hallway", (8, 18)),
        _ev("CAM-02", 1700035260, True,  False, "hallway", (8, 18)),
        _ev("CAM-02", 1700035320, True,  False, "hallway", (8, 18)),
    ]
    assert impl.solve(events) == ["GHOST_MOTION:CAM-02"]


def test_ghost_motion_two_not_enough():
    events = [
        _ev("CAM-02", 1700035200, True,  False, "hallway", (8, 18)),
        _ev("CAM-02", 1700035260, True,  False, "hallway", (8, 18)),
        _ev("CAM-02", 1700035320, False, False, "hallway", (8, 18)),
    ]
    assert impl.solve(events) == []


def test_ghost_motion_streak_reset():
    events = [
        _ev("CAM-04", 1700035200, True,  False, "exit",    (8, 18)),
        _ev("CAM-04", 1700035260, True,  True,  "exit",    (8, 18)),
        _ev("CAM-04", 1700035320, True,  False, "exit",    (8, 18)),
        _ev("CAM-04", 1700035380, True,  False, "exit",    (8, 18)),
    ]
    assert impl.solve(events) == []


def test_crowd_server_room_triggers():
    events = [
        _ev("CAM-05", 1700000010, True, True, "server_room", (8, 18)),
        _ev("CAM-05", 1700000020, True, True, "server_room", (8, 18)),
        _ev("CAM-05", 1700000030, True, True, "server_room", (8, 18)),
    ]
    assert impl.solve(events) == ["AFTER_HOURS:CAM-05", "CROWD_SERVER_ROOM"]


def test_crowd_server_room_spread_out():
    events = [
        _ev("CAM-05", 1700000000, True, True, "server_room", (0, 24)),
        _ev("CAM-05", 1700000070, True, True, "server_room", (0, 24)),
        _ev("CAM-05", 1700000140, True, True, "server_room", (0, 24)),
    ]
    assert impl.solve(events) == []


def test_combined_all_three_alerts():
    events = [
        _ev("CAM-01", 1700000000, True, True, "lobby", (8, 18)),
        _ev("CAM-06", 1700035200, True, False, "stairwell", (8, 18)),
        _ev("CAM-06", 1700035260, True, False, "stairwell", (8, 18)),
        _ev("CAM-06", 1700035320, True, False, "stairwell", (8, 18)),
        _ev("CAM-07", 1700057600,    True, True, "server_room", (0, 24)),
        _ev("CAM-07", 1700057620,    True, True, "server_room", (0, 24)),
        _ev("CAM-07", 1700057640,    True, True, "server_room", (0, 24)),
    ]
    result = impl.solve(events)
    assert "AFTER_HOURS:CAM-01" in result
    assert "GHOST_MOTION:CAM-06" in result
    assert "CROWD_SERVER_ROOM" in result
    assert result == sorted(result)
    assert len(result) == len(set(result))


def test_output_is_sorted():
    events = [
        _ev("CAM-ZZ", 1700000000, True, True, "lobby",   (8, 18)),
        _ev("CAM-AA", 1700000100, True, True, "parking",  (8, 18)),
    ]
    result = impl.solve(events)
    assert result == sorted(result)
    assert result[0] == "AFTER_HOURS:CAM-AA"
    assert result[1] == "AFTER_HOURS:CAM-ZZ"
