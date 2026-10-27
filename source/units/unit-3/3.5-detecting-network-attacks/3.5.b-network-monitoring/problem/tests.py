"""Test suite for 3.5.b — the blackbox acceptance contract.
Imports the implementation under test via IMPL env var.
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


def test_port_anomaly_flags_host():
    baseline = {
        "10.0.1.5": {"max_bytes": 500_000_000, "allowed_ports": [445, 139]},
        "10.0.2.9": {"max_bytes": 5_000_000, "allowed_ports": [80, 443]},
    }
    flows = [
        {"host": "10.0.1.5", "dst_port": 445, "bytes": 100_000_000},
        {"host": "10.0.1.5", "dst_port": 445, "bytes": 50_000_000},
        {"host": "10.0.2.9", "dst_port": 4444, "bytes": 1_000},
    ]
    assert impl.solve(baseline, flows) == ["10.0.2.9"]


def test_volume_anomaly_flags_host():
    baseline = {"10.0.3.1": {"max_bytes": 1_000_000, "allowed_ports": [443]}}
    flows = [
        {"host": "10.0.3.1", "dst_port": 443, "bytes": 900_000},
        {"host": "10.0.3.1", "dst_port": 443, "bytes": 900_000},
    ]
    assert impl.solve(baseline, flows) == ["10.0.3.1"]


def test_normal_traffic_not_flagged():
    baseline = {"10.0.5.5": {"max_bytes": 1_000_000, "allowed_ports": [80, 443]}}
    flows = [
        {"host": "10.0.5.5", "dst_port": 443, "bytes": 400_000},
        {"host": "10.0.5.5", "dst_port": 80, "bytes": 200_000},
    ]
    assert impl.solve(baseline, flows) == []


def test_unknown_host_flagged():
    baseline = {"10.0.1.1": {"max_bytes": 1_000_000, "allowed_ports": [80]}}
    flows = [
        {"host": "10.0.1.1", "dst_port": 80, "bytes": 100},
        {"host": "192.168.9.9", "dst_port": 80, "bytes": 100},
    ]
    assert impl.solve(baseline, flows) == ["192.168.9.9"]


def test_exact_boundary_not_flagged():
    baseline = {"10.0.6.1": {"max_bytes": 1_000, "allowed_ports": [80]}}
    flows = [{"host": "10.0.6.1", "dst_port": 80, "bytes": 1_000}]
    # Exactly at max_bytes is NOT an anomaly (only strictly exceeding is).
    assert impl.solve(baseline, flows) == []


def test_multiple_hosts_mixed_results():
    baseline = {
        "a": {"max_bytes": 100, "allowed_ports": [22]},
        "b": {"max_bytes": 100, "allowed_ports": [22]},
        "c": {"max_bytes": 100, "allowed_ports": [22]},
    }
    flows = [
        {"host": "a", "dst_port": 22, "bytes": 50},       # ok
        {"host": "b", "dst_port": 22, "bytes": 150},      # volume anomaly
        {"host": "c", "dst_port": 9999, "bytes": 10},     # port anomaly
    ]
    assert impl.solve(baseline, flows) == ["b", "c"]


def test_empty_flows():
    baseline = {"a": {"max_bytes": 100, "allowed_ports": [22]}}
    assert impl.solve(baseline, []) == []


def test_result_sorted_and_deduplicated():
    baseline = {"z": {"max_bytes": 10, "allowed_ports": [80]}, "a": {"max_bytes": 10, "allowed_ports": [80]}}
    flows = [
        {"host": "z", "dst_port": 999, "bytes": 1},
        {"host": "z", "dst_port": 999, "bytes": 1},
        {"host": "a", "dst_port": 999, "bytes": 1},
    ]
    assert impl.solve(baseline, flows) == ["a", "z"]
