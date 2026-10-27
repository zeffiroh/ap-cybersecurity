"""Test suite for 3.4.a — the blackbox acceptance contract.
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
    # Stateless mode judges each packet by header fields alone (no memory of prior
    # packets), so the SYN-ACK (dport 55001, matches no rule) is dropped even though
    # it is legitimate return traffic; the SYN and rogue ACK both match dport 443.
    assert impl.solve(rules, packets, "stateless") == ["allow", "drop", "allow"]


def test_example_stateful():
    rules = [
        {"action": "allow", "proto": "tcp", "dport": 443},
        {"action": "allow", "proto": "tcp", "dport": 80},
        {"action": "drop", "proto": "any", "dport": 0},
    ]
    # Handshake packet 1: Client -> Server SYN (Allowed by rule dport 443)
    # Handshake packet 2: Server -> Client SYN-ACK (Allowed because reverse connection exists)
    # Handshake packet 3: Rogue client -> Server ACK (Dropped because no prior SYN)
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
        # 1. SYN to port 80 (Allowed by rule)
        {"src": "10.0.0.2", "dst": "192.168.1.10", "sport": 12345, "dport": 80, "proto": "tcp", "flags": "SYN"},
        # 2. SYN-ACK back (Allowed by state)
        {"src": "192.168.1.10", "dst": "10.0.0.2", "sport": 80, "dport": 12345, "proto": "tcp", "flags": "SYN-ACK"},
        # 3. ACK to port 80 (Allowed by state)
        {"src": "10.0.0.2", "dst": "192.168.1.10", "sport": 12345, "dport": 80, "proto": "tcp", "flags": "ACK"},
        # 4. DATA from server (Allowed by state)
        {"src": "192.168.1.10", "dst": "10.0.0.2", "sport": 80, "dport": 12345, "proto": "tcp", "flags": "DATA"},
        # 5. FIN from client (Allowed, closes state)
        {"src": "10.0.0.2", "dst": "192.168.1.10", "sport": 12345, "dport": 80, "proto": "tcp", "flags": "FIN"},
        # 6. Subsequent DATA from server (Dropped because connection was torn down)
        {"src": "192.168.1.10", "dst": "10.0.0.2", "sport": 80, "dport": 12345, "proto": "tcp", "flags": "DATA"}
    ]
    assert impl.solve(rules, packets, "stateful") == ["allow", "allow", "allow", "allow", "allow", "drop"]


def test_non_tcp_stateful():
    rules = [
        {"action": "allow", "proto": "udp", "dport": 53},
        {"action": "drop", "proto": "any", "dport": 0}
    ]
    packets = [
        # UDP matches rule (allow)
        {"src": "10.0.0.2", "dst": "8.8.8.8", "sport": 12345, "dport": 53, "proto": "udp", "flags": ""},
        # UDP does not match rule (drop)
        {"src": "10.0.0.2", "dst": "8.8.8.8", "sport": 12345, "dport": 54, "proto": "udp", "flags": ""}
    ]
    assert impl.solve(rules, packets, "stateful") == ["allow", "drop"]


def test_empty():
    assert impl.solve([], [], "stateless") == []
    assert impl.solve([], [], "stateful") == []
