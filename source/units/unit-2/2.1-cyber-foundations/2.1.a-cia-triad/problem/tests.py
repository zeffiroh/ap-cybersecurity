"""Test suite for 2.1.a — the blackbox acceptance contract.
Imports the implementation under test via IMPL env var.
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

def test_basic_confidentiality():
    data = [{"id": "1", "description": "Attacker read the unencrypted files."}]
    res = impl.solve(data)
    assert res == {"1": ["Confidentiality"]}

def test_basic_integrity():
    data = [{"id": "2", "description": "Someone altered the transaction logs."}]
    res = impl.solve(data)
    assert res == {"2": ["Integrity"]}

def test_basic_availability():
    data = [{"id": "3", "description": "The service went offline due to power loss."}]
    res = impl.solve(data)
    assert res == {"3": ["Availability"]}

def test_multiple_violations():
    data = [{"id": "4", "description": "Ransomware locked the system and leaked credentials."}]
    res = impl.solve(data)
    # locked/ransomware -> Availability
    # leaked/credentials -> Confidentiality
    assert res == {"4": ["Availability", "Confidentiality"]}

def test_all_violations():
    data = [{"id": "5", "description": "A competitor stole the DB backup, did modify it, and crashed the server."}]
    res = impl.solve(data)
    # stole -> Confidentiality
    # did modify -> Integrity
    # crashed -> Availability
    assert res == {"5": ["Availability", "Confidentiality", "Integrity"]}

def test_case_insensitivity():
    data = [{"id": "6", "description": "DISCLOSED PASSWORDS AND CRASHED THE PORTAL"}]
    res = impl.solve(data)
    assert res == {"6": ["Availability", "Confidentiality"]}

def test_empty_description():
    data = [{"id": "7", "description": ""}]
    res = impl.solve(data)
    assert res == {"7": []}

def test_empty_list():
    res = impl.solve([])
    assert res == {}

def test_multiple_reports():
    data = [
        {"id": "A", "description": "Credential leak detected."},
        {"id": "B", "description": "Normal operation."},
        {"id": "C", "description": "DB tamper and crash."}
    ]
    res = impl.solve(data)
    assert res == {
        "A": ["Confidentiality"],
        "B": [],
        "C": ["Availability", "Integrity"]
    }
