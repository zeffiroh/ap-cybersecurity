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


def test_example_stateless():
    rules = [
        {"action": "allow", "proto": "tcp", "dport": 443},
        {"action": "allow", "proto": "tcp", "dport": 80},
        {"action": "drop", "proto": "any", "dport": 0},
    ]
    packets = [
        {"src": "203.0.113.10", "dst": "10.0.0.5", "sport": 55001, "dport": 443, "proto": "tcp", "flags": "SYN"},
        {"src": "10.0.0.5", "dst": "203.0.113.10", "sport": 443, "dport": 55001, "proto": "tcp", "flags": "SYN-ACK"},
        {"src": "198.51.100.7", "dst": "10.0.0.5", "sport": 44000, "dport": 443, "proto": "tcp", "flags": "ACK"},
    ]
    assert impl.solve(rules, packets, "stateless") == ["allow", "drop", "allow"]


def test_example_stateful():
    rules = [
        {"action": "allow", "proto": "tcp", "dport": 443},
        {"action": "allow", "proto": "tcp", "dport": 80},
        {"action": "drop", "proto": "any", "dport": 0},
    ]
    packets = [
        {"src": "203.0.113.10", "dst": "10.0.0.5", "sport": 55001, "dport": 443, "proto": "tcp", "flags": "SYN"},
        {"src": "10.0.0.5", "dst": "203.0.113.10", "sport": 443, "dport": 55001, "proto": "tcp", "flags": "SYN-ACK"},
        {"src": "198.51.100.7", "dst": "10.0.0.5", "sport": 44000, "dport": 443, "proto": "tcp", "flags": "ACK"},
    ]
    assert impl.solve(rules, packets, "stateful") == ["allow", "allow", "drop"]


def test_stateful_handshake_flow():
    rules = [
        {"action": "allow", "proto": "tcp", "dport": 80},
        {"action": "drop", "proto": "any", "dport": 0}
    ]
    packets = [
        {"src": "10.0.0.2", "dst": "192.168.1.10", "sport": 12345, "dport": 80, "proto": "tcp", "flags": "SYN"},
        {"src": "192.168.1.10", "dst": "10.0.0.2", "sport": 80, "dport": 12345, "proto": "tcp", "flags": "SYN-ACK"},
        {"src": "10.0.0.2", "dst": "192.168.1.10", "sport": 12345, "dport": 80, "proto": "tcp", "flags": "ACK"},
        {"src": "192.168.1.10", "dst": "10.0.0.2", "sport": 80, "dport": 12345, "proto": "tcp", "flags": "DATA"},
        {"src": "10.0.0.2", "dst": "192.168.1.10", "sport": 12345, "dport": 80, "proto": "tcp", "flags": "FIN"},
        {"src": "192.168.1.10", "dst": "10.0.0.2", "sport": 80, "dport": 12345, "proto": "tcp", "flags": "DATA"}
    ]
    assert impl.solve(rules, packets, "stateful") == ["allow", "allow", "allow", "allow", "allow", "drop"]


def test_non_tcp_stateful():
    rules = [
        {"action": "allow", "proto": "udp", "dport": 53},
        {"action": "drop", "proto": "any", "dport": 0}
    ]
    packets = [
        {"src": "10.0.0.2", "dst": "8.8.8.8", "sport": 12345, "dport": 53, "proto": "udp", "flags": ""},
        {"src": "10.0.0.2", "dst": "8.8.8.8", "sport": 12345, "dport": 54, "proto": "udp", "flags": ""}
    ]
    assert impl.solve(rules, packets, "stateful") == ["allow", "drop"]


def test_empty():
    assert impl.solve([], [], "stateless") == []
    assert impl.solve([], [], "stateful") == []
