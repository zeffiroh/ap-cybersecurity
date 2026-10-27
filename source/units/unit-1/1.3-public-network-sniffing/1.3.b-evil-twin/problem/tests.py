"""Test suite for 1.3.b — the blackbox acceptance contract.
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

def test_duplicate_ssid_flags_all():
    """Rule 1: same SSID, two different BSSIDs -> both flagged."""
    aps = [
        {"ssid": "CafeGuest", "bssid": "AA:BB:CC:11:22:33", "security": "WPA2", "signal": -55},
        {"ssid": "CafeGuest", "bssid": "DE:AD:BE:EF:00:01", "security": "WPA2", "signal": -42},
        {"ssid": "HotelLobby", "bssid": "11:22:33:44:55:66", "security": "WPA2", "signal": -65},
    ]
    result = impl.solve(aps)
    assert result == ["AA:BB:CC:11:22:33", "DE:AD:BE:EF:00:01"]


def test_security_downgrade_flags_weaker():
    """Rule 2: same SSID with different security -> weaker entry flagged."""
    aps = [
        {"ssid": "Airport-Free", "bssid": "00:11:22:33:44:55", "security": "WPA2", "signal": -70},
        {"ssid": "Airport-Free", "bssid": "FF:EE:DD:CC:BB:AA", "security": "OPEN", "signal": -48},
        {"ssid": "SafeNet", "bssid": "AA:00:BB:11:CC:22", "security": "WPA3", "signal": -60},
    ]
    result = impl.solve(aps)
    # Both rule 1 (dup SSID) and rule 2 (OPEN < WPA2) apply; stronger BSSID also flagged by rule 1
    assert "FF:EE:DD:CC:BB:AA" in result  # weaker entry always flagged
    assert "00:11:22:33:44:55" in result  # rule 1 also flags the stronger entry
    assert "AA:00:BB:11:CC:22" not in result  # clean single BSSID WPA3


def test_clean_scan_empty_result():
    """No anomaly: each SSID has exactly one BSSID and consistent security."""
    aps = [
        {"ssid": "HomeNet", "bssid": "00:11:22:33:44:55", "security": "WPA3", "signal": -50},
        {"ssid": "OfficeNet", "bssid": "66:77:88:99:AA:BB", "security": "WPA2", "signal": -60},
    ]
    assert impl.solve(aps) == []


def test_empty_input():
    assert impl.solve([]) == []


# ---- hidden / edge cases -------------------------------------------------

def test_three_bssids_same_ssid():
    """Three BSSIDs for one SSID: all three flagged by rule 1."""
    aps = [
        {"ssid": "MallWifi", "bssid": "AA:AA:AA:AA:AA:01", "security": "WPA2", "signal": -50},
        {"ssid": "MallWifi", "bssid": "AA:AA:AA:AA:AA:02", "security": "WPA2", "signal": -55},
        {"ssid": "MallWifi", "bssid": "AA:AA:AA:AA:AA:03", "security": "WPA2", "signal": -60},
    ]
    result = impl.solve(aps)
    assert result == ["AA:AA:AA:AA:AA:01", "AA:AA:AA:AA:AA:02", "AA:AA:AA:AA:AA:03"]


def test_downgrade_only_open_flagged_when_no_dup():
    """Rule 2 alone (same SSID, two BSSIDs, different sec).
    Since two BSSIDs are present, rule 1 also fires, but let's verify both are flagged."""
    aps = [
        {"ssid": "LibraryNet", "bssid": "BB:CC:DD:EE:FF:01", "security": "WPA3", "signal": -55},
        {"ssid": "LibraryNet", "bssid": "BB:CC:DD:EE:FF:02", "security": "OPEN",  "signal": -40},
    ]
    result = impl.solve(aps)
    assert "BB:CC:DD:EE:FF:02" in result  # weaker + dup SSID
    assert "BB:CC:DD:EE:FF:01" in result  # dup SSID (rule 1)


def test_single_ap_no_flag():
    """One AP, unique SSID -> nothing flagged."""
    aps = [{"ssid": "OnlyNet", "bssid": "11:22:33:44:55:66", "security": "WPA2", "signal": -70}]
    assert impl.solve(aps) == []


def test_output_sorted_and_deduped():
    """Output must be sorted ascending and contain no duplicate BSSIDs."""
    aps = [
        {"ssid": "Net", "bssid": "CC:CC:CC:CC:CC:CC", "security": "WPA2", "signal": -50},
        {"ssid": "Net", "bssid": "AA:AA:AA:AA:AA:AA", "security": "OPEN",  "signal": -45},
        {"ssid": "Net", "bssid": "BB:BB:BB:BB:BB:BB", "security": "WPA",   "signal": -55},
    ]
    result = impl.solve(aps)
    assert result == sorted(set(result))
    assert len(result) == len(set(result))
