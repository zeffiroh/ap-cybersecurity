"""Test suite for 3.1.a — the blackbox acceptance contract.
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
    packets = [
        {"src_ip": "10.0.1.55",  "dst_ip": "10.0.1.1", "expected_subnet": "10.0.1.0/24"},
        {"src_ip": "192.168.5.9","dst_ip": "10.0.1.1", "expected_subnet": "10.0.1.0/24"},
        {"src_ip": "10.0.1.200", "dst_ip": "10.0.1.1", "expected_subnet": "10.0.1.0/24"}
    ]
    assert impl.solve(packets) == [1]


def test_example_2():
    packets = [
        {"src_ip": "192.168.1.15", "dst_ip": "192.168.1.1", "expected_subnet": "192.168.1.0/24"},
        {"src_ip": "172.16.0.4", "dst_ip": "192.168.1.1", "expected_subnet": "192.168.1.0/24"}
    ]
    assert impl.solve(packets) == [1]


# ---- hidden / edge cases -------------------------------------------------
def test_edge_empty():
    assert impl.solve([]) == []


def test_edge_all_clean():
    packets = [
        {"src_ip": "10.0.0.5", "dst_ip": "10.0.0.1", "expected_subnet": "10.0.0.0/8"},
        {"src_ip": "10.254.254.254", "dst_ip": "10.0.0.1", "expected_subnet": "10.0.0.0/8"}
    ]
    assert impl.solve(packets) == []


def test_edge_all_spoofed():
    packets = [
        {"src_ip": "192.168.1.1", "dst_ip": "10.0.0.1", "expected_subnet": "10.0.0.0/24"},
        {"src_ip": "192.168.1.2", "dst_ip": "10.0.0.1", "expected_subnet": "10.0.0.0/24"}
    ]
    assert impl.solve(packets) == [0, 1]


def test_invalid_format():
    packets = [
        {"src_ip": "invalid-ip", "dst_ip": "10.0.0.1", "expected_subnet": "10.0.0.0/24"},
        {"src_ip": "10.0.0.5", "dst_ip": "10.0.0.1", "expected_subnet": "invalid-subnet"}
    ]
    assert impl.solve(packets) == [0, 1]
