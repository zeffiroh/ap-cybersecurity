"""Test suite for 3.3.a — the blackbox acceptance contract.
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
def test_example_1():
    vlan_map = {"WS-01": 20, "SRV-01": 30, "GUEST-01": 40, "MGMT-01": 10}
    flows = [("WS-01", "SRV-01"), ("GUEST-01", "SRV-01"), ("WS-01", "WS-01")]
    expected = [("GUEST-01", "SRV-01")]
    assert impl.solve(vlan_map, flows) == expected


def test_example_2():
    vlan_map = {"WS-01": 20, "SRV-01": 30, "GUEST-01": 40, "MGMT-01": 10}
    # Test one-way exception: 20 -> 30 is allowed, 30 -> 20 is blocked!
    flows = [("SRV-01", "WS-01"), ("MGMT-01", "WS-01")]
    expected = [("SRV-01", "WS-01"), ("MGMT-01", "WS-01")]
    assert impl.solve(vlan_map, flows) == expected


# ---- hidden / edge cases -------------------------------------------------
def test_edge_empty():
    vlan_map = {"WS-01": 20, "SRV-01": 30}
    assert impl.solve(vlan_map, []) == []


def test_all_blocked():
    vlan_map = {"WS-01": 20, "SRV-01": 30, "GUEST-01": 40}
    flows = [("GUEST-01", "WS-01"), ("SRV-01", "WS-01"), ("GUEST-01", "SRV-01")]
    assert impl.solve(vlan_map, flows) == flows


def test_all_allowed():
    vlan_map = {"WS-01": 20, "SRV-01": 30, "WS-02": 20}
    flows = [("WS-01", "WS-02"), ("WS-01", "SRV-01"), ("WS-02", "WS-01")]
    assert impl.solve(vlan_map, flows) == []
