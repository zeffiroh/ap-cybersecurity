"""Test suite for 2.2.a — the blackbox acceptance contract.
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


# ---- helpers ---------------------------------------------------------------
def mk(eid, time, badge, door, dist, sensor):
    return {"id": eid, "time": time, "badge": badge, "door": door,
            "distance_from_prev": dist, "sensor_count": sensor}


# ---- visible cases ---------------------------------------------------------
def test_impossible_speed_flagged():
    # B-204 covers 50 m in 3 s = 16.7 m/s > 2.0 — flag E002
    records = [
        mk("E001", 1000, "B-204", "D1", None, 1),
        mk("E002", 1003, "B-204", "D2", 50,   1),
    ]
    assert impl.solve(records) == ["E002"]


def test_sensor_mismatch_flagged():
    # sensor_count=2 with one badge swipe — flag E003
    records = [
        mk("E003", 2000, "B-117", "D1", None, 2),
    ]
    assert impl.solve(records) == ["E003"]


def test_clean_entry_not_flagged():
    # 10 m in 10 s = 1.0 m/s <= 2.0; sensor=1 — clean
    records = [
        mk("E004", 3000, "B-011", "D1", None, 1),
        mk("E005", 3010, "B-011", "D2", 10,   1),
    ]
    assert impl.solve(records) == []


def test_empty_log():
    assert impl.solve([]) == []


def test_both_rules_same_event():
    # sensor=2 AND speed violation on same record — appears once
    records = [
        mk("E010", 5000, "B-300", "D1", None, 1),
        mk("E011", 5001, "B-300", "D2", 30,   2),  # 30/1=30 m/s AND sensor=2
    ]
    result = impl.solve(records)
    assert result == ["E011"]
    assert result.count("E011") == 1


def test_multiple_badges_only_one_flagged():
    # B-001 is clean; B-002 has impossible speed
    records = [
        mk("E020", 6000, "B-001", "D1", None, 1),
        mk("E021", 6100, "B-001", "D2", 100,  1),   # 100/100=1.0 m/s — OK
        mk("E022", 6000, "B-002", "D1", None, 1),
        mk("E023", 6002, "B-002", "D2", 20,   1),   # 20/2=10 m/s — flagged
    ]
    assert impl.solve(records) == ["E023"]


# ---- hidden / edge cases ---------------------------------------------------
def test_same_timestamp_flagged():
    # elapsed=0 — always flag (division by zero case)
    records = [
        mk("E030", 7000, "B-400", "D1", None, 1),
        mk("E031", 7000, "B-400", "D2", 1,    1),
    ]
    assert impl.solve(records) == ["E031"]


def test_no_badge_not_flagged_by_speed():
    # badge=None rows should not trigger Rule 1 or Rule 2
    records = [
        mk("E040", 8000, None, "D1", None, 1),
        mk("E041", 8001, None, "D1", 5,    1),
    ]
    assert impl.solve(records) == []


def test_exactly_at_speed_limit_not_flagged():
    # 20 m in 10 s = exactly 2.0 m/s — not strictly greater than limit
    records = [
        mk("E050", 9000, "B-500", "D1", None, 1),
        mk("E051", 9010, "B-500", "D2", 20,   1),
    ]
    assert impl.solve(records) == []


def test_sorted_output():
    # Multiple violations — result must be sorted
    records = [
        mk("E060", 10000, "B-600", "D1", None, 1),
        mk("E061", 10001, "B-600", "D2", 50,   2),  # both rules
        mk("E062", 10100, "B-700", "D1", None, 2),  # Rule 2
    ]
    result = impl.solve(records)
    assert result == sorted(result)
    assert "E061" in result
    assert "E062" in result


def test_first_appearance_no_flag():
    # First time a badge is seen — no distance_from_prev, no speed check
    records = [
        mk("E070", 11000, "B-800", "D1", None, 1),
    ]
    assert impl.solve(records) == []
