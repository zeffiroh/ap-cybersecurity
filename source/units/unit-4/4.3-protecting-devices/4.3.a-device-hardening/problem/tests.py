import importlib.util
import os
import pathlib
import pytest

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
    data = {
        "baseline": {
            "min_password_length": 12,
            "disallowed_services": ["ftp", "telnet"],
            "firewall_enabled": True,
            "encryption_enabled": True,
            "allowed_accounts": ["admin", "operator"]
        },
        "configuration": {
            "password_length": 8,
            "services": ["ssh", "ftp"],
            "firewall_enabled": False,
            "encryption_enabled": True,
            "accounts": ["admin", "guest", "operator"]
        }
    }
    expected = ["allowed_accounts", "disallowed_services", "firewall_enabled", "min_password_length"]
    assert impl.solve(data) == expected


def test_example_2():
    data = {
        "baseline": {
            "min_password_length": 8,
            "disallowed_services": ["telnet"],
            "firewall_enabled": True,
            "encryption_enabled": False,
            "allowed_accounts": ["admin"]
        },
        "configuration": {
            "password_length": 10,
            "services": ["ssh", "http"],
            "firewall_enabled": True,
            "encryption_enabled": True,
            "accounts": ["admin"]
        }
    }
    expected = []
    assert impl.solve(data) == expected


# ---- hidden / edge cases -------------------------------------------------
def test_edge_empty():
    # Empty configurations default to fail checks that are required
    data = {
        "baseline": {
            "min_password_length": 10,
            "disallowed_services": ["ftp"],
            "firewall_enabled": True,
            "encryption_enabled": True,
            "allowed_accounts": ["admin"]
        },
        "configuration": {}
    }
    # password_length defaults to 0 (fails)
    # services defaults to [] (passes - no disallowed service present)
    # firewall_enabled defaults to False (fails)
    # encryption_enabled defaults to False (fails)
    # accounts defaults to [] (passes - no unauthorized accounts present)
    expected = ["encryption_enabled", "firewall_enabled", "min_password_length"]
    assert impl.solve(data) == expected


def test_all_pass():
    data = {
        "baseline": {
            "min_password_length": 14,
            "disallowed_services": ["ftp", "telnet", "http", "smb"],
            "firewall_enabled": True,
            "encryption_enabled": True,
            "allowed_accounts": ["root", "deploy"]
        },
        "configuration": {
            "password_length": 14,
            "services": ["ssh", "https"],
            "firewall_enabled": True,
            "encryption_enabled": True,
            "accounts": ["root"]
        }
    }
    assert impl.solve(data) == []


def test_case_sensitivity():
    data = {
        "baseline": {
            "min_password_length": 8,
            "disallowed_services": ["Telnet"],
            "firewall_enabled": False,
            "encryption_enabled": False,
            "allowed_accounts": ["Admin"]
        },
        "configuration": {
            "password_length": 8,
            "services": ["telnet"], # disallowed has 'Telnet', case-sensitive means passes
            "accounts": ["admin"] # allowed has 'Admin', case-sensitive means fails
        }
    }
    assert impl.solve(data) == ["allowed_accounts"]
