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


def mk(eid, time, badge, door, dist, sensor):
    return {"id": eid, "time": time, "badge": badge, "door": door,
            "distance_from_prev": dist, "sensor_count": sensor}


def test_impossible_speed_flagged():
    records = [
        mk("E001", 1000, "B-204", "D1", None, 1),
        mk("E002", 1003, "B-204", "D2", 50,   1),
    ]
    assert impl.solve(records) == ["E002"]


def test_sensor_mismatch_flagged():
    records = [
        mk("E003", 2000, "B-117", "D1", None, 2),
    ]
    assert impl.solve(records) == ["E003"]


def test_clean_entry_not_flagged():
    records = [
        mk("E004", 3000, "B-011", "D1", None, 1),
        mk("E005", 3010, "B-011", "D2", 10,   1),
    ]
    assert impl.solve(records) == []


def test_empty_log():
    assert impl.solve([]) == []


def test_both_rules_same_event():
    records = [
        mk("E010", 5000, "B-300", "D1", None, 1),
        mk("E011", 5001, "B-300", "D2", 30,   2),
    ]
    result = impl.solve(records)
    assert result == ["E011"]
    assert result.count("E011") == 1


def test_multiple_badges_only_one_flagged():
    records = [
        mk("E020", 6000, "B-001", "D1", None, 1),
        mk("E021", 6100, "B-001", "D2", 100,  1),
        mk("E022", 6000, "B-002", "D1", None, 1),
        mk("E023", 6002, "B-002", "D2", 20,   1),
    ]
    assert impl.solve(records) == ["E023"]


def test_same_timestamp_flagged():
    records = [
        mk("E030", 7000, "B-400", "D1", None, 1),
        mk("E031", 7000, "B-400", "D2", 1,    1),
    ]
    assert impl.solve(records) == ["E031"]


def test_no_badge_not_flagged_by_speed():
    records = [
        mk("E040", 8000, None, "D1", None, 1),
        mk("E041", 8001, None, "D1", 5,    1),
    ]
    assert impl.solve(records) == []


def test_exactly_at_speed_limit_not_flagged():
    records = [
        mk("E050", 9000, "B-500", "D1", None, 1),
        mk("E051", 9010, "B-500", "D2", 20,   1),
    ]
    assert impl.solve(records) == []


def test_sorted_output():
    records = [
        mk("E060", 10000, "B-600", "D1", None, 1),
        mk("E061", 10001, "B-600", "D2", 50,   2),
        mk("E062", 10100, "B-700", "D1", None, 2),
    ]
    result = impl.solve(records)
    assert result == sorted(result)
    assert "E061" in result
    assert "E062" in result


def test_first_appearance_no_flag():
    records = [
        mk("E070", 11000, "B-800", "D1", None, 1),
    ]
    assert impl.solve(records) == []
