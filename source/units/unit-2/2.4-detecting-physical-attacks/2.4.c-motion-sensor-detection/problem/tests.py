"""Test suite for 2.4.c — the blackbox acceptance contract.
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

# ---------------------------------------------------------------------------
# Shared fixtures — deterministic, matches lesson's known false-positive causes
# ---------------------------------------------------------------------------
FP = {"sunlight", "hvac_airflow", "pet", "insect", "vibration", "foliage"}


def _single(id_, sensor_type, cause):
    return {"id": id_, "sensor_type": sensor_type, "cause": cause}


def _dual(id_, cause_pir, cause_mw):
    return {"id": id_, "sensor_type": "dual-tech", "cause_pir": cause_pir, "cause_mw": cause_mw}


# ---- visible cases -------------------------------------------------------

def test_pir_person_is_true_detection():
    events = [_single("EVT-001", "pir", "person")]
    assert impl.solve(events, FP) == ["EVT-001"]


def test_pir_sunlight_is_false_positive():
    events = [_single("EVT-002", "pir", "sunlight")]
    assert impl.solve(events, FP) == []


def test_microwave_vibration_is_false_positive():
    events = [_single("EVT-003", "microwave", "vibration")]
    assert impl.solve(events, FP) == []


def test_ultrasonic_person_is_true_detection():
    events = [_single("EVT-004", "ultrasonic", "person")]
    assert impl.solve(events, FP) == ["EVT-004"]


def test_dual_tech_both_person_is_true_detection():
    events = [_dual("EVT-005", "person", "person")]
    assert impl.solve(events, FP) == ["EVT-005"]


def test_dual_tech_pir_false_positive_overrides():
    events = [_dual("EVT-006", "hvac_airflow", "person")]
    assert impl.solve(events, FP) == []


def test_dual_tech_mw_false_positive_overrides():
    events = [_dual("EVT-007", "person", "vibration")]
    assert impl.solve(events, FP) == []


def test_empty_events():
    assert impl.solve([], FP) == []


def test_mixed_batch():
    events = [
        _single("EVT-008", "pir", "person"),
        _single("EVT-009", "pir", "pet"),
        _single("EVT-010", "microwave", "hvac_airflow"),
        _dual("EVT-011", "person", "person"),
        _dual("EVT-012", "person", "vibration"),
        _single("EVT-013", "ultrasonic", "insect"),
    ]
    assert impl.solve(events, FP) == ["EVT-008", "EVT-011"]


# ---- hidden / edge cases -------------------------------------------------

def test_dual_tech_both_false_positive():
    """Both elements report known false-positive causes -> still false positive."""
    events = [_dual("EVT-014", "sunlight", "vibration")]
    assert impl.solve(events, FP) == []


def test_single_tech_unknown_cause_treated_as_genuine():
    """A cause tag not in the known false-positive set is treated as genuine (e.g. "tailgater")."""
    events = [_single("EVT-015", "pir", "tailgater")]
    assert impl.solve(events, FP) == ["EVT-015"]


def test_output_sorted_and_deduplicated():
    events = [
        _single("EVT-020", "pir", "person"),
        _single("EVT-019", "microwave", "person"),
        _single("EVT-018", "ultrasonic", "person"),
    ]
    result = impl.solve(events, FP)
    assert result == sorted(result)
    assert result == ["EVT-018", "EVT-019", "EVT-020"]


def test_all_sensor_types_mixed_with_custom_fp_set():
    """A smaller false_positive_causes set changes which causes count as genuine."""
    custom_fp = {"sunlight"}
    events = [
        _single("EVT-021", "pir", "hvac_airflow"),   # not in custom_fp -> true detection
        _single("EVT-022", "pir", "sunlight"),        # in custom_fp -> false positive
        _dual("EVT-023", "hvac_airflow", "person"),   # neither in custom_fp -> true detection
    ]
    assert impl.solve(events, custom_fp) == ["EVT-021", "EVT-023"]


def test_no_true_detections_returns_empty_list():
    events = [
        _single("EVT-024", "pir", "pet"),
        _dual("EVT-025", "person", "foliage"),
    ]
    assert impl.solve(events, FP) == []
