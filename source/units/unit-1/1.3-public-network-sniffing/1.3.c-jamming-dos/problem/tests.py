"""Test suite for 1.3.c — the blackbox acceptance contract.
Imports the implementation under test via IMPL env var so the SAME tests grade:
  - solution.py   (reference, must be green)
  - starter.py    (must be red until completed)
Default target is solution.py.

Detection rule: return True if any run of >= 5 consecutive samples is ALL strictly > 80.
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


# ---- visible cases -------------------------------------------------------

def test_single_spike_not_jamming():
    """One sample above threshold — run length 1 < 5 -> False."""
    assert impl.solve([20, 25, 90, 22, 30, 18, 24]) is False


def test_run_of_six_is_jamming():
    """Six consecutive samples > 80 -> True."""
    assert impl.solve([15, 82, 85, 88, 91, 83, 87, 20]) is True


def test_all_below_threshold():
    """No sample exceeds T=80 -> False."""
    assert impl.solve([70, 72, 75, 71, 73, 74, 76]) is False


def test_run_of_nine_is_jamming():
    """Nine consecutive samples > 80 -> True."""
    assert impl.solve([50, 81, 82, 83, 84, 85, 86, 87, 88, 30]) is True


# ---- hidden / edge cases -------------------------------------------------

def test_empty_input():
    assert impl.solve([]) is False


def test_run_of_exactly_five():
    """Boundary: exactly 5 consecutive samples above T -> True."""
    assert impl.solve([10, 81, 82, 83, 84, 85, 10]) is True


def test_run_of_four_not_jamming():
    """Boundary: only 4 consecutive -> False."""
    assert impl.solve([10, 81, 82, 83, 84, 10]) is False


def test_threshold_boundary_not_strictly_greater():
    """Exactly T=80 does NOT count (strictly greater than 80)."""
    assert impl.solve([80, 80, 80, 80, 80, 80]) is False


def test_threshold_boundary_81_counts():
    """81 is strictly greater than 80 -> counts in run."""
    assert impl.solve([81, 81, 81, 81, 81]) is True


def test_interrupted_run_not_jamming():
    """Run of 4, then 1 sample = 80, then 4 more -> two partial runs, neither >= 5."""
    assert impl.solve([81, 82, 83, 84, 80, 81, 82, 83, 84]) is False


def test_long_clean_then_jamming():
    """Clean samples for a long time, then a jammed burst."""
    clean = [10, 20, 30] * 10
    jammed = [85, 86, 87, 88, 89]
    assert impl.solve(clean + jammed) is True


def test_jamming_at_start():
    """Jamming run at the very beginning of the series."""
    assert impl.solve([90, 91, 92, 93, 94, 10, 10]) is True


def test_single_element_below():
    assert impl.solve([50]) is False


def test_single_element_above():
    """Single element above T but run length 1 < 5 -> False."""
    assert impl.solve([99]) is False
