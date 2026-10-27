"""Test suite for 4.3.b — the blackbox acceptance contract.
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
def test_example_1_prompt_scenario():
    data = {
        "signatures": ["d41d8cd98f00b204e9800998ecf8427e", "098f6bcd4621d373cade4e832627b4f6"],
        "behavioral_rules": {"max_file_modifications": 10, "max_network_connections": 5},
        "processes": [
            {"pid": 101, "name": "backup_agent.exe", "hash": "81dc9bdb52d04dc20036dbd8313ed055",
             "file_modifications": 8, "network_connections": 2},
            {"pid": 102, "name": "ransomware.exe", "hash": "d41d8cd98f00b204e9800998ecf8427e",
             "file_modifications": 2, "network_connections": 0},
            {"pid": 103, "name": "spam_sender.exe", "hash": "1f10c9aa0090ff91e90ff8a8bc8a9bcf",
             "file_modifications": 1, "network_connections": 12},
        ],
    }
    assert impl.solve(data) == [102, 103]


def test_example_2_no_flags():
    data = {
        "signatures": ["aaaa"],
        "behavioral_rules": {"max_file_modifications": 10, "max_network_connections": 5},
        "processes": [
            {"pid": 1, "name": "clean.exe", "hash": "bbbb",
             "file_modifications": 3, "network_connections": 1},
        ],
    }
    assert impl.solve(data) == []


# ---- hidden / edge cases -------------------------------------------------
def test_edge_empty_process_list():
    data = {
        "signatures": ["aaaa"],
        "behavioral_rules": {"max_file_modifications": 10, "max_network_connections": 5},
        "processes": [],
    }
    assert impl.solve(data) == []


def test_signature_case_insensitive():
    data = {
        "signatures": ["A1B2C3"],
        "behavioral_rules": {"max_file_modifications": 100, "max_network_connections": 100},
        "processes": [
            {"pid": 5, "name": "evil.exe", "hash": "a1b2c3",
             "file_modifications": 0, "network_connections": 0},
        ],
    }
    assert impl.solve(data) == [5]


def test_boundary_thresholds_not_exceeded_when_equal():
    data = {
        "signatures": [],
        "behavioral_rules": {"max_file_modifications": 10, "max_network_connections": 5},
        "processes": [
            {"pid": 7, "name": "borderline.exe", "hash": "zzzz",
             "file_modifications": 10, "network_connections": 5},
        ],
    }
    assert impl.solve(data) == []


def test_boundary_thresholds_exceeded_by_one():
    data = {
        "signatures": [],
        "behavioral_rules": {"max_file_modifications": 10, "max_network_connections": 5},
        "processes": [
            {"pid": 8, "name": "over.exe", "hash": "zzzz",
             "file_modifications": 11, "network_connections": 0},
            {"pid": 9, "name": "over2.exe", "hash": "zzzz",
             "file_modifications": 0, "network_connections": 6},
        ],
    }
    assert impl.solve(data) == [8, 9]


def test_result_sorted_ascending_regardless_of_input_order():
    data = {
        "signatures": ["hash1", "hash2", "hash3"],
        "behavioral_rules": {"max_file_modifications": 999, "max_network_connections": 999},
        "processes": [
            {"pid": 30, "name": "c.exe", "hash": "hash3",
             "file_modifications": 0, "network_connections": 0},
            {"pid": 10, "name": "a.exe", "hash": "hash1",
             "file_modifications": 0, "network_connections": 0},
            {"pid": 20, "name": "b.exe", "hash": "hash2",
             "file_modifications": 0, "network_connections": 0},
        ],
    }
    assert impl.solve(data) == [10, 20, 30]


def test_multiple_reasons_same_pid_counted_once():
    data = {
        "signatures": ["deadbeef"],
        "behavioral_rules": {"max_file_modifications": 1, "max_network_connections": 1},
        "processes": [
            {"pid": 42, "name": "multi.exe", "hash": "deadbeef",
             "file_modifications": 50, "network_connections": 50},
        ],
    }
    assert impl.solve(data) == [42]
