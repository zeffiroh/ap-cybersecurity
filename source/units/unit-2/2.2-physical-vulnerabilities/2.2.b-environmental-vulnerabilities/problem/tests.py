"""Test suite for 2.2.b — the blackbox acceptance contract.
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
def test_power_levels():
    data = [
        {"id": "p1", "room": "a", "type": "power", "value": 0},
        {"id": "p2", "room": "a", "type": "power", "value": 92},
        {"id": "p3", "room": "a", "type": "power", "value": 100},
        {"id": "p4", "room": "a", "type": "power", "value": 108},
        {"id": "p5", "room": "a", "type": "power", "value": 120},
    ]
    assert impl.solve(data) == {
        "p1": "CRITICAL",
        "p2": "WARNING",
        "p3": "NORMAL",
        "p4": "WARNING",
        "p5": "CRITICAL",
    }


def test_temperature_and_humidity_no_escalation():
    # Only temperature elevated in room b, humidity stays NORMAL -> no escalation.
    data = [
        {"id": "t1", "room": "b", "type": "temperature", "value": 28},
        {"id": "h1", "room": "b", "type": "humidity", "value": 50},
    ]
    assert impl.solve(data) == {"t1": "WARNING", "h1": "NORMAL"}


def test_smoke_and_water():
    data = [
        {"id": "s1", "room": "c", "type": "smoke", "value": 0},
        {"id": "s2", "room": "c", "type": "smoke", "value": 3},
        {"id": "w1", "room": "c", "type": "water", "value": 0},
        {"id": "w2", "room": "c", "type": "water", "value": 1},
    ]
    assert impl.solve(data) == {
        "s1": "NORMAL",
        "s2": "CRITICAL",
        "w1": "NORMAL",
        "w2": "CRITICAL",
    }


def test_combined_escalation():
    # Room d: temperature WARNING + humidity WARNING -> both escalate to CRITICAL.
    # Power reading in same room is unaffected.
    data = [
        {"id": "t1", "room": "d", "type": "temperature", "value": 29},
        {"id": "h1", "room": "d", "type": "humidity", "value": 65},
        {"id": "p1", "room": "d", "type": "power", "value": 100},
    ]
    assert impl.solve(data) == {"t1": "CRITICAL", "h1": "CRITICAL", "p1": "NORMAL"}


def test_accept():
    data = [
        {"id": "t1", "room": "e", "type": "temperature", "value": 20},
        {"id": "h1", "room": "e", "type": "humidity", "value": 45},
    ]
    assert impl.solve(data) == {"t1": "NORMAL", "h1": "NORMAL"}


# ---- hidden / edge cases -------------------------------------------------
def test_edge_empty():
    assert impl.solve([]) == {}


def test_multiple_rooms_independent():
    data = [
        {"id": "t1", "room": "room1", "type": "temperature", "value": 31},
        {"id": "h1", "room": "room2", "type": "humidity", "value": 75},
        {"id": "t2", "room": "room2", "type": "temperature", "value": 20},
    ]
    # room1: only temperature elevated (already CRITICAL, no escalation needed to check)
    # room2: humidity CRITICAL but temperature NORMAL -> no escalation of temperature
    assert impl.solve(data) == {"t1": "CRITICAL", "h1": "CRITICAL", "t2": "NORMAL"}


def test_already_critical_stays_critical_after_escalation():
    data = [
        {"id": "t1", "room": "f", "type": "temperature", "value": 35},
        {"id": "h1", "room": "f", "type": "humidity", "value": 65},
    ]
    assert impl.solve(data) == {"t1": "CRITICAL", "h1": "CRITICAL"}


def test_low_temperature_and_low_humidity_escalate():
    data = [
        {"id": "t1", "room": "g", "type": "temperature", "value": 10},
        {"id": "h1", "room": "g", "type": "humidity", "value": 25},
    ]
    assert impl.solve(data) == {"t1": "CRITICAL", "h1": "CRITICAL"}
