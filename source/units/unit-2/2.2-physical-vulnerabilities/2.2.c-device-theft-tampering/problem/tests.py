"""Test suite for 2.2.c — the blackbox acceptance contract.
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


def _mk(id_, type_, encrypted, seal_intact, sensitive, hours):
    return {
        "id": id_,
        "type": type_,
        "encrypted": encrypted,
        "seal_intact": seal_intact,
        "contains_sensitive_data": sensitive,
        "hours_since_check": hours,
    }


# ---- visible cases -------------------------------------------------------
def test_theft_unencrypted_is_high():
    data = [_mk("i1", "theft", False, True, False, 1)]
    assert impl.solve(data) == {"i1": "HIGH"}


def test_theft_encrypted_sensitive_long_delay_is_medium():
    data = [_mk("i1", "theft", True, True, True, 50)]
    assert impl.solve(data) == {"i1": "MEDIUM"}


def test_theft_encrypted_sensitive_short_delay_is_low():
    data = [_mk("i1", "theft", True, True, True, 10)]
    assert impl.solve(data) == {"i1": "LOW"}


def test_theft_encrypted_not_sensitive_is_low():
    data = [_mk("i1", "theft", True, True, False, 100)]
    assert impl.solve(data) == {"i1": "LOW"}


def test_tampering_seal_broken_is_high():
    data = [_mk("i1", "tampering", True, False, False, 1)]
    assert impl.solve(data) == {"i1": "HIGH"}


def test_tampering_seal_intact_long_delay_is_medium():
    data = [_mk("i1", "tampering", True, True, False, 72)]
    assert impl.solve(data) == {"i1": "MEDIUM"}


def test_tampering_seal_intact_short_delay_is_low():
    data = [_mk("i1", "tampering", True, True, False, 5)]
    assert impl.solve(data) == {"i1": "LOW"}


def test_unknown_type_is_low():
    data = [_mk("i1", "lost", False, False, True, 1000)]
    assert impl.solve(data) == {"i1": "LOW"}


# ---- hidden / edge cases -------------------------------------------------
def test_edge_empty():
    assert impl.solve([]) == {}


def test_boundary_48_hours_is_not_yet_escalated():
    # hours_since_check == 48 is NOT > 48, so should stay LOW/at baseline.
    data = [
        _mk("theft48", "theft", True, True, True, 48),
        _mk("tamper48", "tampering", True, True, False, 48),
    ]
    assert impl.solve(data) == {"theft48": "LOW", "tamper48": "LOW"}


def test_multiple_mixed():
    data = [
        _mk("a", "theft", False, True, True, 1),
        _mk("b", "theft", True, True, True, 60),
        _mk("c", "tampering", True, False, False, 1),
        _mk("d", "tampering", True, True, False, 60),
        _mk("e", "theft", True, False, False, 1),
    ]
    expected = {
        "a": "HIGH",
        "b": "MEDIUM",
        "c": "HIGH",
        "d": "MEDIUM",
        "e": "LOW",
    }
    assert impl.solve(data) == expected
