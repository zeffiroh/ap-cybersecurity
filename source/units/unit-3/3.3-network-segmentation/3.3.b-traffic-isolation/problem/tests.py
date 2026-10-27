"""Test suite for 3.3.b — the blackbox acceptance contract.
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


def test_example():
    policy = {
        "allowed_roles": {
            "ehr_db": ["doctor", "admin"],
            "mri_machine": ["admin", "technician"]
        },
        "requires_internal": ["ehr_db", "mri_machine"],
        "requires_posture": ["ehr_db"],
        "internal_prefixes": ["192.168.1.", "10.0."]
    }
    requests = [
        {
            "id": "REQ-01",
            "user": "alice",
            "role": "doctor",
            "resource": "ehr_db",
            "ip": "192.168.1.50",
            "device_posture": {"antivirus_ok": True, "disk_encrypted": True}
        },
        {
            "id": "REQ-02",
            "user": "bob",
            "role": "guest",
            "resource": "ehr_db",
            "ip": "192.168.1.60",
            "device_posture": {"antivirus_ok": True}
        },
        {
            "id": "REQ-03",
            "user": "charlie",
            "role": "admin",
            "resource": "mri_machine",
            "ip": "203.0.113.4",  # external
            "device_posture": {}
        }
    ]
    # REQ-01: Allowed (Matches doctor role, internal IP, clean posture)
    # REQ-02: Denied (Guest role not allowed on ehr_db)
    # REQ-03: Denied (External IP for mri_machine which requires internal)
    assert impl.solve(requests, policy) == ["REQ-01"]


def test_posture_failure():
    policy = {
        "allowed_roles": {"ehr_db": ["doctor"]},
        "requires_internal": [],
        "requires_posture": ["ehr_db"],
        "internal_prefixes": []
    }
    requests = [
        {
            "id": "REQ-01",
            "user": "alice",
            "role": "doctor",
            "resource": "ehr_db",
            "ip": "12.0.0.1",
            "device_posture": {"antivirus_ok": True, "disk_encrypted": False}
        }
    ]
    # Denied because disk_encrypted is False
    assert impl.solve(requests, policy) == []


def test_empty_posture_allowed():
    policy = {
        "allowed_roles": {"ehr_db": ["doctor"]},
        "requires_internal": [],
        "requires_posture": ["ehr_db"],
        "internal_prefixes": []
    }
    requests = [
        {
            "id": "REQ-01",
            "user": "alice",
            "role": "doctor",
            "resource": "ehr_db",
            "ip": "12.0.0.1",
            "device_posture": {}  # empty is compliant
        }
    ]
    assert impl.solve(requests, policy) == ["REQ-01"]


def test_empty_requests():
    policy = {
        "allowed_roles": {"ehr_db": ["doctor"]},
        "requires_internal": [],
        "requires_posture": ["ehr_db"],
        "internal_prefixes": []
    }
    assert impl.solve([], policy) == []


def test_resource_not_in_policy():
    policy = {
        "allowed_roles": {"ehr_db": ["doctor"]},
        "requires_internal": [],
        "requires_posture": [],
        "internal_prefixes": []
    }
    requests = [
        {
            "id": "REQ-01",
            "user": "alice",
            "role": "doctor",
            "resource": "some_other_db",
            "ip": "12.0.0.1",
            "device_posture": {}
        }
    ]
    assert impl.solve(requests, policy) == []
