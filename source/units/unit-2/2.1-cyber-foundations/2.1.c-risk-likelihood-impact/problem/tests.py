"""Test suite for 2.1.c — the blackbox acceptance contract.
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
def test_avoid():
    # score >= 20 and cost > 0.6 * value
    # likelihood = 5, impact = 4 -> score = 20
    # cost = 61, value = 100 -> cost/value = 0.61 > 0.6
    data = [
        {"name": "r1", "likelihood": 5, "impact": 4, "cost": 61, "value": 100}
    ]
    assert impl.solve(data) == {"r1": "Avoid"}


def test_mitigate_high():
    # score >= 15 and cost <= 0.3 * value
    # likelihood = 3, impact = 5 -> score = 15
    # cost = 30, value = 100 -> cost/value = 0.3
    data = [
        {"name": "r1", "likelihood": 3, "impact": 5, "cost": 30, "value": 100}
    ]
    assert impl.solve(data) == {"r1": "Mitigate"}


def test_transfer():
    # score >= 15, but cost > 0.3 * value
    # likelihood = 3, impact = 5 -> score = 15
    # cost = 31, value = 100
    data = [
        {"name": "r1", "likelihood": 3, "impact": 5, "cost": 31, "value": 100}
    ]
    assert impl.solve(data) == {"r1": "Transfer"}


def test_mitigate_low():
    # score >= 5 and cost <= 0.1 * value
    # likelihood = 2, impact = 3 -> score = 6
    # cost = 10, value = 100
    data = [
        {"name": "r1", "likelihood": 2, "impact": 3, "cost": 10, "value": 100}
    ]
    assert impl.solve(data) == {"r1": "Mitigate"}


def test_accept():
    # score < 5, or (score >= 5 and cost > 0.1 * value and score < 15)
    # Case A: score = 4
    # Case B: score = 6, cost = 11, value = 100
    data = [
        {"name": "r1", "likelihood": 2, "impact": 2, "cost": 5, "value": 100},
        {"name": "r2", "likelihood": 2, "impact": 3, "cost": 11, "value": 100}
    ]
    assert impl.solve(data) == {"r1": "Accept", "r2": "Accept"}


# ---- hidden / edge cases -------------------------------------------------
def test_edge_empty():
    assert impl.solve([]) == {}


def test_multiple():
    data = [
        {"name": "avoid_it", "likelihood": 5, "impact": 5, "cost": 80, "value": 100},
        {"name": "mitigate_high", "likelihood": 4, "impact": 4, "cost": 25, "value": 100},
        {"name": "transfer_it", "likelihood": 3, "impact": 5, "cost": 40, "value": 100},
        {"name": "mitigate_low", "likelihood": 2, "impact": 4, "cost": 8, "value": 100},
        {"name": "accept_low", "likelihood": 1, "impact": 3, "cost": 10, "value": 100},
        {"name": "accept_costly", "likelihood": 3, "impact": 4, "cost": 50, "value": 100}
    ]
    expected = {
        "avoid_it": "Avoid",
        "mitigate_high": "Mitigate",
        "transfer_it": "Transfer",
        "mitigate_low": "Mitigate",
        "accept_low": "Accept",
        "accept_costly": "Accept"
    }
    assert impl.solve(data) == expected

