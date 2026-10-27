"""Test suite for 3.5.c — the blackbox acceptance contract.
Imports the implementation under test via IMPL env var.
Default target is solution.py.
"""
import importlib.util
import os
import pathlib

import pytest

_HERE = pathlib.Path(__file__).parent
_TARGET = os.environ.get("IMPL", str(_HERE / "solution.py"))


def _load(path):
    spec = importlib.util.spec_from_file_location("impl", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


impl = _load(_TARGET)


def test_basic_reordering():
    actions = [
        {"action": "Rebuild the server from a clean backup", "phase": "Recovery"},
        {"action": "Write the incident response plan", "phase": "Preparation"},
        {"action": "Isolate the infected host from the network", "phase": "Containment"},
        {"action": "Confirm the IDS alert is a real compromise", "phase": "Identification"},
    ]
    assert impl.solve(actions) == [
        "Write the incident response plan",
        "Confirm the IDS alert is a real compromise",
        "Isolate the infected host from the network",
        "Rebuild the server from a clean backup",
    ]


def test_all_six_phases():
    actions = [
        {"action": "Document a timeline and update the IR plan", "phase": "Lessons Learned"},
        {"action": "Remove the backdoor account", "phase": "Eradication"},
        {"action": "Reconnect the rebuilt host and monitor", "phase": "Recovery"},
        {"action": "Run a tabletop exercise", "phase": "Preparation"},
        {"action": "Block the malicious IP at the firewall", "phase": "Containment"},
        {"action": "Triage the alert queue", "phase": "Identification"},
    ]
    result = impl.solve(actions)
    assert result == [
        "Run a tabletop exercise",
        "Triage the alert queue",
        "Block the malicious IP at the firewall",
        "Remove the backdoor account",
        "Reconnect the rebuilt host and monitor",
        "Document a timeline and update the IR plan",
    ]


def test_stable_within_same_phase():
    actions = [
        {"action": "Contain host A", "phase": "Containment"},
        {"action": "Contain host B", "phase": "Containment"},
        {"action": "Prep step 1", "phase": "Preparation"},
    ]
    assert impl.solve(actions) == ["Prep step 1", "Contain host A", "Contain host B"]


def test_already_in_order_unchanged():
    actions = [
        {"action": "p", "phase": "Preparation"},
        {"action": "i", "phase": "Identification"},
        {"action": "c", "phase": "Containment"},
    ]
    assert impl.solve(actions) == ["p", "i", "c"]


def test_invalid_phase_raises_value_error():
    actions = [{"action": "Bogus phase", "phase": "Investigation"}]
    with pytest.raises(ValueError):
        impl.solve(actions)


def test_empty_list():
    assert impl.solve([]) == []


def test_single_action():
    assert impl.solve([{"action": "only one", "phase": "Recovery"}]) == ["only one"]
