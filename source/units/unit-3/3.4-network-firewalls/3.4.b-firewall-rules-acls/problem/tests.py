"""Test suite for 3.4.b — the blackbox acceptance contract.
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


def test_basic_allow_and_deny():
    rules = [
        {"action": "allow", "src": "10.0.4.0", "dst": "10.0.1.5", "port": 3306, "proto": "tcp"},
        {"action": "deny", "src": "any", "dst": "10.0.1.5", "port": 3306, "proto": "tcp"},
    ]
    packets = [
        {"src": "10.0.4.0", "dst": "10.0.1.5", "port": 3306, "proto": "tcp"},
        {"src": "10.0.9.9", "dst": "10.0.1.5", "port": 3306, "proto": "tcp"},
        {"src": "10.0.9.9", "dst": "10.0.1.5", "port": 22, "proto": "tcp"},
    ]
    assert impl.solve(rules, packets) == ["allow", "deny", "deny"]


def test_shadowing_broad_rule_first():
    rules = [
        {"action": "allow", "src": "any", "dst": "any", "port": 22, "proto": "tcp"},
        {"action": "deny", "src": "203.0.113.0", "dst": "10.0.1.10", "port": 22, "proto": "tcp"},
    ]
    packet = {"src": "203.0.113.0", "dst": "10.0.1.10", "port": 22, "proto": "tcp"}
    # Broad allow matches first; the deny below it is unreachable (shadowed).
    assert impl.solve(rules, [packet]) == ["allow"]


def test_specific_rule_first_fixes_shadowing():
    rules = [
        {"action": "deny", "src": "203.0.113.0", "dst": "10.0.1.10", "port": 22, "proto": "tcp"},
        {"action": "allow", "src": "any", "dst": "any", "port": 22, "proto": "tcp"},
    ]
    packets = [
        {"src": "203.0.113.0", "dst": "10.0.1.10", "port": 22, "proto": "tcp"},
        {"src": "198.51.100.1", "dst": "10.0.1.10", "port": 22, "proto": "tcp"},
    ]
    assert impl.solve(rules, packets) == ["deny", "allow"]


def test_any_fields_match_everything():
    rules = [
        {"action": "allow", "src": "any", "dst": "any", "port": 0, "proto": "any"},
    ]
    packets = [
        {"src": "1.1.1.1", "dst": "2.2.2.2", "port": 9999, "proto": "udp"},
        {"src": "8.8.8.8", "dst": "9.9.9.9", "port": 1, "proto": "tcp"},
    ]
    assert impl.solve(rules, packets) == ["allow", "allow"]


def test_proto_mismatch_falls_through_to_implicit_deny():
    rules = [
        {"action": "allow", "src": "any", "dst": "any", "port": 53, "proto": "udp"},
    ]
    packets = [
        {"src": "10.0.0.2", "dst": "8.8.8.8", "port": 53, "proto": "tcp"},  # wrong proto
    ]
    assert impl.solve(rules, packets) == ["deny"]


def test_empty_rules_denies_everything():
    packets = [{"src": "1.1.1.1", "dst": "2.2.2.2", "port": 80, "proto": "tcp"}]
    assert impl.solve([], packets) == ["deny"]


def test_empty_packets():
    rules = [{"action": "allow", "src": "any", "dst": "any", "port": 0, "proto": "any"}]
    assert impl.solve(rules, []) == []


def test_multiple_packets_order_preserved():
    rules = [
        {"action": "allow", "src": "any", "dst": "any", "port": 443, "proto": "tcp"},
        {"action": "allow", "src": "any", "dst": "any", "port": 80, "proto": "tcp"},
        {"action": "deny", "src": "any", "dst": "any", "port": 0, "proto": "any"},
    ]
    packets = [
        {"src": "a", "dst": "b", "port": 443, "proto": "tcp"},
        {"src": "a", "dst": "b", "port": 21, "proto": "tcp"},
        {"src": "a", "dst": "b", "port": 80, "proto": "tcp"},
    ]
    assert impl.solve(rules, packets) == ["allow", "deny", "allow"]
