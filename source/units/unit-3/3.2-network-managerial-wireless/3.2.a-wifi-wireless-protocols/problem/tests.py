"""Test suite for 3.2.a — the blackbox acceptance contract.
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


def _cfg(protocol="WPA3", mode="personal", psk_length=24, guest=True, admin=True, fw=True):
    return {
        "protocol": protocol,
        "mode": mode,
        "psk_length": psk_length,
        "guest_network_isolated": guest,
        "admin_password_strong": admin,
        "firmware_current": fw,
    }


# ---- visible cases -------------------------------------------------------

def test_perfect_config_no_gaps():
    assert impl.evaluate_wifi_config(_cfg()) == []


def test_tkip_and_weak_psk():
    cfg = _cfg(protocol="WPA2-TKIP", psk_length=12)
    assert impl.evaluate_wifi_config(cfg) == ["insecure_protocol", "weak_psk"]


def test_wep_flagged():
    cfg = _cfg(protocol="WEP")
    assert impl.evaluate_wifi_config(cfg) == ["insecure_protocol"]


def test_open_flagged():
    cfg = _cfg(protocol="OPEN")
    assert impl.evaluate_wifi_config(cfg) == ["insecure_protocol"]


def test_wpa2_aes_acceptable():
    cfg = _cfg(protocol="WPA2-AES", psk_length=20)
    assert impl.evaluate_wifi_config(cfg) == []


def test_no_guest_isolation_flagged():
    cfg = _cfg(guest=False)
    assert impl.evaluate_wifi_config(cfg) == ["no_guest_isolation"]


def test_weak_admin_password_flagged():
    cfg = _cfg(admin=False)
    assert impl.evaluate_wifi_config(cfg) == ["weak_admin_password"]


def test_outdated_firmware_flagged():
    cfg = _cfg(fw=False)
    assert impl.evaluate_wifi_config(cfg) == ["outdated_firmware"]


def test_all_gaps_sorted():
    cfg = _cfg(protocol="WEP", psk_length=5, guest=False, admin=False, fw=False)
    assert impl.evaluate_wifi_config(cfg) == [
        "insecure_protocol",
        "no_guest_isolation",
        "outdated_firmware",
        "weak_admin_password",
        "weak_psk",
    ]


# ---- hidden / edge cases -------------------------------------------------

def test_enterprise_mode_ignores_psk_length():
    """Enterprise mode uses per-user 802.1X creds; psk_length must never trigger weak_psk."""
    cfg = _cfg(mode="enterprise", psk_length=1)
    assert impl.evaluate_wifi_config(cfg) == []


def test_psk_length_boundary_19_is_weak():
    cfg = _cfg(psk_length=19)
    assert impl.evaluate_wifi_config(cfg) == ["weak_psk"]


def test_psk_length_boundary_20_is_ok():
    cfg = _cfg(psk_length=20)
    assert impl.evaluate_wifi_config(cfg) == []


def test_wpa3_enterprise_perfect():
    cfg = _cfg(protocol="WPA3", mode="enterprise", psk_length=0)
    assert impl.evaluate_wifi_config(cfg) == []


def test_wpa2_tkip_enterprise_still_flags_protocol_only():
    cfg = _cfg(protocol="WPA2-TKIP", mode="enterprise", psk_length=0)
    assert impl.evaluate_wifi_config(cfg) == ["insecure_protocol"]


def test_no_duplicate_gap_codes():
    cfg = _cfg(protocol="OPEN", psk_length=0, guest=False, admin=False, fw=False)
    result = impl.evaluate_wifi_config(cfg)
    assert len(result) == len(set(result))
