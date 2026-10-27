"""Test suite for 3.5.a — the blackbox acceptance contract.
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

# ---- shared fixtures ---------------------------------------------------------
RULES_BASIC = [
    {"port": 80,  "keyword": "etc/passwd"},
    {"port": 22,  "keyword": "libssh"},
    {"port": 3306, "keyword": "select "},
]

LOGS_BASIC = [
    {"id": "pkt-001", "dst_port": 80,   "payload": "GET /admin/../etc/passwd HTTP/1.1"},
    {"id": "pkt-002", "dst_port": 443,  "payload": "TLS handshake data"},
    {"id": "pkt-003", "dst_port": 80,   "payload": "GET /index.html HTTP/1.1"},
    {"id": "pkt-004", "dst_port": 22,   "payload": "SSH-2.0-OpenSSH_8.9"},
    {"id": "pkt-005", "dst_port": 3306, "payload": "SELECT * FROM users"},
    {"id": "pkt-006", "dst_port": 22,   "payload": "SSH-2.0-libssh_0.9.6"},
]


# ---- visible cases -----------------------------------------------------------
def test_path_traversal_match():
    result = impl.solve(LOGS_BASIC, RULES_BASIC)
    assert "pkt-001" in result, "pkt-001 matches port=80 + keyword='etc/passwd'"


def test_benign_port_no_match():
    result = impl.solve(LOGS_BASIC, RULES_BASIC)
    assert "pkt-002" not in result, "pkt-002 is port 443 — no rule for that port"
    assert "pkt-003" not in result, "pkt-003 port 80 but payload has no matching keyword"


def test_sql_case_insensitive():
    # "SELECT" (uppercase) must match keyword "select " (lowercase)
    result = impl.solve(LOGS_BASIC, RULES_BASIC)
    assert "pkt-005" in result, "SQL SELECT should match keyword 'select ' case-insensitively"


def test_libssh_match():
    result = impl.solve(LOGS_BASIC, RULES_BASIC)
    assert "pkt-006" in result, "pkt-006 port=22 payload contains 'libssh'"
    assert "pkt-004" not in result, "pkt-004 port=22 but 'OpenSSH' does not contain 'libssh'"


def test_result_sorted():
    result = impl.solve(LOGS_BASIC, RULES_BASIC)
    assert result == sorted(result), "Output must be sorted ascending"


# ---- hidden / edge cases -----------------------------------------------------
def test_empty_logs():
    assert impl.solve([], RULES_BASIC) == []


def test_empty_rules():
    assert impl.solve(LOGS_BASIC, []) == []


def test_both_empty():
    assert impl.solve([], []) == []


def test_no_payload_match():
    logs = [{"id": "x-001", "dst_port": 80, "payload": ""}]
    rules = [{"port": 80, "keyword": "admin"}]
    assert impl.solve(logs, rules) == []


def test_multiple_rules_same_entry_deduplicated():
    # pkt-A matches two rules; should appear only once
    logs = [{"id": "pkt-A", "dst_port": 80, "payload": "etc/passwd and script alert"}]
    rules = [
        {"port": 80, "keyword": "etc/passwd"},
        {"port": 80, "keyword": "script"},
    ]
    result = impl.solve(logs, rules)
    assert result.count("pkt-A") == 1, "Entry matching multiple rules must appear only once"


def test_port_must_match():
    # keyword present but wrong port — should not match
    logs = [{"id": "z-001", "dst_port": 443, "payload": "etc/passwd in body"}]
    rules = [{"port": 80, "keyword": "etc/passwd"}]
    assert impl.solve(logs, rules) == []
