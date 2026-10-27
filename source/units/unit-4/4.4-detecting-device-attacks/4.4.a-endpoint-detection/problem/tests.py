"""Test suite for 4.4.a — the blackbox acceptance contract.
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
    events = [
        {"pid": 501, "process": "powershell.exe", "parent_process": "winword.exe",
         "external_connection": True, "bytes_transferred": 500},
        {"pid": 502, "process": "chrome.exe", "parent_process": "explorer.exe",
         "external_connection": True, "bytes_transferred": 200000},
        {"pid": 503, "process": "backup.exe", "parent_process": "explorer.exe",
         "external_connection": True, "bytes_transferred": 5000000},
    ]
    assert impl.solve(events) == [501, 503]


def test_example_2_no_flags():
    events = [
        {"pid": 1, "process": "notepad.exe", "parent_process": "explorer.exe",
         "external_connection": False, "bytes_transferred": 0},
        {"pid": 2, "process": "cmd.exe", "parent_process": "explorer.exe",
         "external_connection": False, "bytes_transferred": 0},
    ]
    assert impl.solve(events) == []


# ---- hidden / edge cases -------------------------------------------------
def test_edge_empty_events():
    assert impl.solve([]) == []


def test_case_insensitive_matching():
    events = [
        {"pid": 10, "process": "PowerShell.EXE", "parent_process": "WINWORD.EXE",
         "external_connection": False, "bytes_transferred": 0},
    ]
    assert impl.solve(events) == [10]


def test_interpreter_from_explorer_is_safe():
    events = [
        {"pid": 20, "process": "cmd.exe", "parent_process": "explorer.exe",
         "external_connection": False, "bytes_transferred": 0},
        {"pid": 21, "process": "CMD.EXE", "parent_process": "EXPLORER.EXE",
         "external_connection": False, "bytes_transferred": 0},
    ]
    assert impl.solve(events) == []


def test_transfer_threshold_boundary_not_exceeded():
    events = [
        {"pid": 30, "process": "sync.exe", "parent_process": "explorer.exe",
         "external_connection": True, "bytes_transferred": 1000000},
    ]
    assert impl.solve(events) == []


def test_transfer_threshold_boundary_exceeded():
    events = [
        {"pid": 31, "process": "sync.exe", "parent_process": "explorer.exe",
         "external_connection": True, "bytes_transferred": 1000001},
    ]
    assert impl.solve(events) == [31]


def test_no_external_connection_ignores_large_transfer():
    events = [
        {"pid": 40, "process": "backup.exe", "parent_process": "explorer.exe",
         "external_connection": False, "bytes_transferred": 9999999},
    ]
    assert impl.solve(events) == []


def test_result_deduplicated_and_sorted():
    events = [
        {"pid": 60, "process": "mshta.exe", "parent_process": "outlook.exe",
         "external_connection": True, "bytes_transferred": 5000000},
        {"pid": 50, "process": "wscript.exe", "parent_process": "outlook.exe",
         "external_connection": False, "bytes_transferred": 0},
    ]
    assert impl.solve(events) == [50, 60]


def test_living_off_the_land_variants():
    events = [
        {"pid": 71, "process": "cscript.exe", "parent_process": "svchost.exe",
         "external_connection": False, "bytes_transferred": 0},
        {"pid": 72, "process": "wscript.exe", "parent_process": "outlook.exe",
         "external_connection": False, "bytes_transferred": 0},
    ]
    assert impl.solve(events) == [71, 72]
