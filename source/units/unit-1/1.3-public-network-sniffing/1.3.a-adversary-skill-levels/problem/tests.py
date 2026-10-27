"""Test suite for 1.3.a — the blackbox acceptance contract.
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

# ---- visible cases -------------------------------------------------------

def test_zero_day_is_high():
    a = {"uses_zero_day": True, "custom_tooling": False,
         "targets_specific_victim": False, "off_the_shelf_only": False,
         "adapts_to_defenses": False}
    assert impl.solve(a) == "high"


def test_custom_tooling_is_high():
    a = {"uses_zero_day": False, "custom_tooling": True,
         "targets_specific_victim": False, "off_the_shelf_only": False,
         "adapts_to_defenses": False}
    assert impl.solve(a) == "high"


def test_script_kiddie_is_low():
    a = {"uses_zero_day": False, "custom_tooling": False,
         "targets_specific_victim": False, "off_the_shelf_only": True,
         "adapts_to_defenses": False}
    assert impl.solve(a) == "low"


def test_targeted_adaptive_is_high():
    a = {"uses_zero_day": False, "custom_tooling": False,
         "targets_specific_victim": True, "off_the_shelf_only": False,
         "adapts_to_defenses": True}
    assert impl.solve(a) == "high"


# ---- hidden / edge cases -------------------------------------------------

def test_targeted_not_adaptive_is_low():
    """Targeting alone without adaptation is not enough for high tier."""
    a = {"uses_zero_day": False, "custom_tooling": False,
         "targets_specific_victim": True, "off_the_shelf_only": True,
         "adapts_to_defenses": False}
    assert impl.solve(a) == "low"


def test_adaptive_not_targeted_is_low():
    """Adapts to defenses but is opportunistic, not targeted — stays low."""
    a = {"uses_zero_day": False, "custom_tooling": False,
         "targets_specific_victim": False, "off_the_shelf_only": False,
         "adapts_to_defenses": True}
    assert impl.solve(a) == "low"


def test_all_false_is_low():
    a = {"uses_zero_day": False, "custom_tooling": False,
         "targets_specific_victim": False, "off_the_shelf_only": False,
         "adapts_to_defenses": False}
    assert impl.solve(a) == "low"


def test_zero_day_overrides_targeted_and_adaptive():
    """Zero-day flag still returns high regardless of other fields."""
    a = {"uses_zero_day": True, "custom_tooling": True,
         "targets_specific_victim": True, "off_the_shelf_only": False,
         "adapts_to_defenses": True}
    assert impl.solve(a) == "high"
