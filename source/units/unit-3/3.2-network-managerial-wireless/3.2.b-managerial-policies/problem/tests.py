"""Test suite for 3.2.b — the blackbox acceptance contract.
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


def _s(id_, desc, mech):
    return {"id": id_, "description": desc, "mechanism": mech}


# ---- visible cases -------------------------------------------------------

def test_policy_document_is_managerial():
    scenarios = [_s("s1", "New hires sign an AUP.", "policy_document")]
    assert impl.classify_controls(scenarios) == ["managerial"]


def test_software_enforcement_is_technical():
    scenarios = [_s("s2", "Firewall blocks malicious IPs automatically.", "software_or_hardware_enforcement")]
    assert impl.classify_controls(scenarios) == ["technical"]


def test_physical_barrier_is_physical():
    scenarios = [_s("s3", "Server room door requires a badge.", "physical_barrier")]
    assert impl.classify_controls(scenarios) == ["physical"]


def test_training_program_is_managerial():
    scenarios = [_s("s4", "Annual phishing-awareness training for all staff.", "training_program")]
    assert impl.classify_controls(scenarios) == ["managerial"]


def test_access_review_process_is_managerial():
    scenarios = [_s("s5", "Quarterly review of who has admin access.", "access_review_process")]
    assert impl.classify_controls(scenarios) == ["managerial"]


def test_mixed_batch_order_preserved():
    scenarios = [
        _s("a", "desc a", "physical_barrier"),
        _s("b", "desc b", "policy_document"),
        _s("c", "desc c", "software_or_hardware_enforcement"),
    ]
    assert impl.classify_controls(scenarios) == ["physical", "managerial", "technical"]


def test_empty_scenarios():
    assert impl.classify_controls([]) == []


# ---- hidden / edge cases -------------------------------------------------

def test_all_three_managerial_mechanisms():
    scenarios = [
        _s("1", "d1", "policy_document"),
        _s("2", "d2", "training_program"),
        _s("3", "d3", "access_review_process"),
    ]
    assert impl.classify_controls(scenarios) == ["managerial", "managerial", "managerial"]


def test_description_text_does_not_affect_classification():
    """Even if description mentions a firewall, mechanism decides the classification."""
    scenarios = [_s("x", "Employees are trained on how firewalls work.", "training_program")]
    assert impl.classify_controls(scenarios) == ["managerial"]


def test_large_batch_deterministic():
    mechs = ["policy_document", "training_program", "access_review_process",
             "software_or_hardware_enforcement", "physical_barrier"]
    expected_map = {
        "policy_document": "managerial",
        "training_program": "managerial",
        "access_review_process": "managerial",
        "software_or_hardware_enforcement": "technical",
        "physical_barrier": "physical",
    }
    scenarios = [_s(str(i), f"d{i}", mechs[i % 5]) for i in range(20)]
    expected = [expected_map[mechs[i % 5]] for i in range(20)]
    assert impl.classify_controls(scenarios) == expected
