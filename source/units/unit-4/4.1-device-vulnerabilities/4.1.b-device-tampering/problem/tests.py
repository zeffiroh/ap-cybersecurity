"""Test suite for 4.1.b — the blackbox acceptance contract."""
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


def test_empty():
    assert impl.solve([]) == []


def test_chassis_intrusion():
    logs = [
        {"timestamp": "2026-06-25T10:00:00Z", "device_id": "pc_01", "event_type": "chassis_intrusion", "details": "chassis opened detected"}
    ]
    assert impl.solve(logs) == ["pc_01"]


def test_unauthorized_boot():
    logs = [
        {"timestamp": "2026-06-25T10:00:00Z", "device_id": "laptop_02", "event_type": "boot", "details": "Booted from external Live USB"}
    ]
    assert impl.solve(logs) == ["laptop_02"]


def test_usb_rubber_ducky_success():
    logs = [
        {"timestamp": "2026-06-25T10:00:00Z", "device_id": "pc_02", "event_type": "usb_insert", "details": "USB HID Keyboard connected"},
        {"timestamp": "2026-06-25T10:00:02Z", "device_id": "pc_02", "event_type": "command", "details": "powershell -nop -w hidden -c payload"}
    ]
    assert impl.solve(logs) == ["pc_02"]


def test_usb_rubber_ducky_too_late():
    logs = [
        {"timestamp": "2026-06-25T10:00:00Z", "device_id": "pc_02", "event_type": "usb_insert", "details": "USB HID Keyboard connected"},
        {"timestamp": "2026-06-25T10:00:05Z", "device_id": "pc_02", "event_type": "command", "details": "powershell -nop -w hidden -c payload"}
    ]
    assert impl.solve(logs) == []


def test_usb_rubber_ducky_different_device():
    logs = [
        {"timestamp": "2026-06-25T10:00:00Z", "device_id": "pc_01", "event_type": "usb_insert", "details": "USB HID Keyboard connected"},
        {"timestamp": "2026-06-25T10:00:01Z", "device_id": "pc_02", "event_type": "command", "details": "powershell -nop -w hidden -c payload"}
    ]
    assert impl.solve(logs) == []


def test_multiple_compromises():
    logs = [
        {"timestamp": "2026-06-25T10:00:00Z", "device_id": "pc_03", "event_type": "chassis_intrusion", "details": "Intrusion switch opened"},
        {"timestamp": "2026-06-25T10:05:00Z", "device_id": "pc_01", "event_type": "boot", "details": "booting usb medium"},
        {"timestamp": "2026-06-25T10:10:00Z", "device_id": "pc_02", "event_type": "user_login", "details": "admin login"}
    ]
    assert impl.solve(logs) == ["pc_01", "pc_03"]
