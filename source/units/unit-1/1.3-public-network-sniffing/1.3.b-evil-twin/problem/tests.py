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


def test_duplicate_ssid_flags_all():
    aps = [
        {"ssid": "CafeGuest", "bssid": "AA:BB:CC:11:22:33", "security": "WPA2", "signal": -55},
        {"ssid": "CafeGuest", "bssid": "DE:AD:BE:EF:00:01", "security": "WPA2", "signal": -42},
        {"ssid": "HotelLobby", "bssid": "11:22:33:44:55:66", "security": "WPA2", "signal": -65},
    ]
    result = impl.solve(aps)
    assert result == ["AA:BB:CC:11:22:33", "DE:AD:BE:EF:00:01"]


def test_security_downgrade_flags_weaker():
    aps = [
        {"ssid": "Airport-Free", "bssid": "00:11:22:33:44:55", "security": "WPA2", "signal": -70},
        {"ssid": "Airport-Free", "bssid": "FF:EE:DD:CC:BB:AA", "security": "OPEN", "signal": -48},
        {"ssid": "SafeNet", "bssid": "AA:00:BB:11:CC:22", "security": "WPA3", "signal": -60},
    ]
    result = impl.solve(aps)
    assert "FF:EE:DD:CC:BB:AA" in result
    assert "00:11:22:33:44:55" in result
    assert "AA:00:BB:11:CC:22" not in result


def test_clean_scan_empty_result():
    aps = [
        {"ssid": "HomeNet", "bssid": "00:11:22:33:44:55", "security": "WPA3", "signal": -50},
        {"ssid": "OfficeNet", "bssid": "66:77:88:99:AA:BB", "security": "WPA2", "signal": -60},
    ]
    assert impl.solve(aps) == []


def test_empty_input():
    assert impl.solve([]) == []


def test_three_bssids_same_ssid():
    aps = [
        {"ssid": "MallWifi", "bssid": "AA:AA:AA:AA:AA:01", "security": "WPA2", "signal": -50},
        {"ssid": "MallWifi", "bssid": "AA:AA:AA:AA:AA:02", "security": "WPA2", "signal": -55},
        {"ssid": "MallWifi", "bssid": "AA:AA:AA:AA:AA:03", "security": "WPA2", "signal": -60},
    ]
    result = impl.solve(aps)
    assert result == ["AA:AA:AA:AA:AA:01", "AA:AA:AA:AA:AA:02", "AA:AA:AA:AA:AA:03"]


def test_downgrade_only_open_flagged_when_no_dup():
    aps = [
        {"ssid": "LibraryNet", "bssid": "BB:CC:DD:EE:FF:01", "security": "WPA3", "signal": -55},
        {"ssid": "LibraryNet", "bssid": "BB:CC:DD:EE:FF:02", "security": "OPEN",  "signal": -40},
    ]
    result = impl.solve(aps)
    assert "BB:CC:DD:EE:FF:02" in result
    assert "BB:CC:DD:EE:FF:01" in result


def test_single_ap_no_flag():
    aps = [{"ssid": "OnlyNet", "bssid": "11:22:33:44:55:66", "security": "WPA2", "signal": -70}]
    assert impl.solve(aps) == []


def test_output_sorted_and_deduped():
    aps = [
        {"ssid": "Net", "bssid": "CC:CC:CC:CC:CC:CC", "security": "WPA2", "signal": -50},
        {"ssid": "Net", "bssid": "AA:AA:AA:AA:AA:AA", "security": "OPEN",  "signal": -45},
        {"ssid": "Net", "bssid": "BB:BB:BB:BB:BB:BB", "security": "WPA",   "signal": -55},
    ]
    result = impl.solve(aps)
    assert result == sorted(set(result))
    assert len(result) == len(set(result))
