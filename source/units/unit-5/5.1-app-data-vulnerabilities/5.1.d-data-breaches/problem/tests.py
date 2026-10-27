"""Test suite for 5.1.d — the blackbox acceptance contract.
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
def test_low_public_small():
    report = {"categories": ["public"], "record_count": 50, "days_to_detect": 1}
    assert impl.solve(report) == {"score": 0, "label": "low"}


def test_critical_pii_plaintext_large_slow():
    report = {"categories": ["pii", "auth_plaintext"], "record_count": 500000, "days_to_detect": 45}
    assert impl.solve(report) == {"score": 120, "label": "critical"}


def test_medium_email_small_moderate():
    report = {"categories": ["email"], "record_count": 200, "days_to_detect": 5}
    assert impl.solve(report) == {"score": 30, "label": "medium"}


def test_hashed_auth_only():
    report = {"categories": ["auth_hashed"], "record_count": 50, "days_to_detect": 1}
    assert impl.solve(report) == {"score": 15, "label": "low"}


# ---- hidden / edge cases -------------------------------------------------
def test_high_financial_million_records_fast_detect():
    report = {"categories": ["financial"], "record_count": 2_000_000, "days_to_detect": 1}
    assert impl.solve(report) == {"score": 70, "label": "high"}


def test_multiple_categories_additive():
    report = {"categories": ["pii", "financial", "health"], "record_count": 50, "days_to_detect": 1}
    assert impl.solve(report) == {"score": 120, "label": "critical"}


def test_unknown_category_contributes_zero():
    report = {"categories": ["mystery_category"], "record_count": 50, "days_to_detect": 1}
    assert impl.solve(report) == {"score": 0, "label": "low"}


def test_empty_report():
    report = {"categories": [], "record_count": 0, "days_to_detect": 0}
    assert impl.solve(report) == {"score": 0, "label": "low"}


def test_boundary_record_count_10000():
    report = {"categories": [], "record_count": 10000, "days_to_detect": 0}
    assert impl.solve(report) == {"score": 20, "label": "medium"}
