"""Test suite for 1.5.a — the blackbox acceptance contract.
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
def test_single_root_login():
    lines = ["PermitRootLogin yes", "Port 22"]
    assert impl.solve(lines) == ["insecure:PermitRootLogin"]


def test_multiple_findings():
    lines = ["PasswordAuthentication yes", "X11Forwarding yes", "PermitRootLogin yes"]
    assert impl.solve(lines) == [
        "insecure:PasswordAuthentication",
        "insecure:PermitRootLogin",
        "insecure:X11Forwarding",
    ]


def test_port23_and_ssl():
    lines = ["port 23", "ssl false"]
    assert impl.solve(lines) == ["insecure:Port23", "insecure:SSLDisabled"]


def test_all_safe():
    lines = ["# all defaults", "Port 22", "PermitRootLogin no", ""]
    assert impl.solve(lines) == []


# ---- hidden / edge cases -------------------------------------------------
def test_empty_input():
    assert impl.solve([]) == []


def test_case_insensitive():
    assert impl.solve(["PERMITROOTLOGIN YES"]) == ["insecure:PermitRootLogin"]


def test_comment_lines_ignored():
    assert impl.solve(["# PermitRootLogin yes"]) == []


def test_blank_lines_ignored():
    assert impl.solve(["", "   ", "\t"]) == []


def test_tls_off_variant():
    assert impl.solve(["tls off"]) == ["insecure:SSLDisabled"]


def test_ssl_off_variant():
    assert impl.solve(["SSL OFF"]) == ["insecure:SSLDisabled"]


def test_permit_empty_passwords():
    assert impl.solve(["PermitEmptyPasswords yes"]) == ["insecure:PermitEmptyPasswords"]


def test_dedup_sorted():
    # two lines both triggering PermitRootLogin should yield one tag
    lines = ["PermitRootLogin yes", "permitrootlogin yes"]
    result = impl.solve(lines)
    assert result == sorted(set(result))
    assert result == ["insecure:PermitRootLogin"]


def test_full_config():
    config = [
        "# /etc/ssh/sshd_config for dev-server",
        "Port 22",
        "PermitRootLogin yes",
        "PasswordAuthentication yes",
        "X11Forwarding yes",
        "PermitEmptyPasswords yes",
        "AllowTcpForwarding yes",
        "",
    ]
    assert impl.solve(config) == [
        "insecure:PasswordAuthentication",
        "insecure:PermitEmptyPasswords",
        "insecure:PermitRootLogin",
        "insecure:X11Forwarding",
    ]
