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


def test_single_spike_not_jamming():
    assert impl.solve([20, 25, 90, 22, 30, 18, 24]) is False


def test_run_of_six_is_jamming():
    assert impl.solve([15, 82, 85, 88, 91, 83, 87, 20]) is True


def test_all_below_threshold():
    assert impl.solve([70, 72, 75, 71, 73, 74, 76]) is False


def test_run_of_nine_is_jamming():
    assert impl.solve([50, 81, 82, 83, 84, 85, 86, 87, 88, 30]) is True


def test_empty_input():
    assert impl.solve([]) is False


def test_run_of_exactly_five():
    assert impl.solve([10, 81, 82, 83, 84, 85, 10]) is True


def test_run_of_four_not_jamming():
    assert impl.solve([10, 81, 82, 83, 84, 10]) is False


def test_threshold_boundary_not_strictly_greater():
    assert impl.solve([80, 80, 80, 80, 80, 80]) is False


def test_threshold_boundary_81_counts():
    assert impl.solve([81, 81, 81, 81, 81]) is True


def test_interrupted_run_not_jamming():
    assert impl.solve([81, 82, 83, 84, 80, 81, 82, 83, 84]) is False


def test_long_clean_then_jamming():
    clean = [10, 20, 30] * 10
    jammed = [85, 86, 87, 88, 89]
    assert impl.solve(clean + jammed) is True


def test_jamming_at_start():
    assert impl.solve([90, 91, 92, 93, 94, 10, 10]) is True


def test_single_element_below():
    assert impl.solve([50]) is False


def test_single_element_above():
    assert impl.solve([99]) is False
