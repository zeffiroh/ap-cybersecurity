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


def test_worst_case_open_unverified_no_vpn():
    out = impl.solve({"ssid": "AirportFreeWifi", "encryption": "open",
                      "verified": False, "vpn": False})
    assert out == ["no-vpn", "open-network", "unverified-ssid"]


def test_fully_protected():
    assert impl.solve({"encryption": "wpa2", "verified": True, "vpn": True}) == []


def test_only_missing_vpn():
    assert impl.solve({"encryption": "wpa2", "verified": True, "vpn": False}) == ["no-vpn"]


def test_encrypted_but_unverified_with_vpn():
    assert impl.solve({"encryption": "WPA3", "verified": False, "vpn": True}) == ["unverified-ssid"]


def test_empty_dict_is_worst_case():
    assert impl.solve({}) == ["no-vpn", "open-network", "unverified-ssid"]


def test_encryption_case_insensitive():
    assert impl.solve({"encryption": "OpEn", "verified": True, "vpn": True}) == ["open-network"]


def test_encryption_none_and_empty_count_as_open():
    assert impl.solve({"encryption": None, "verified": True, "vpn": True}) == ["open-network"]
    assert impl.solve({"encryption": "", "verified": True, "vpn": True}) == ["open-network"]
    assert impl.solve({"encryption": "none", "verified": True, "vpn": True}) == ["open-network"]


def test_wep_is_not_open_network():
    assert impl.solve({"encryption": "wep", "verified": True, "vpn": True}) == []


def test_output_sorted_and_deduplicated():
    out = impl.solve({"encryption": "open"})
    assert out == ["no-vpn", "open-network", "unverified-ssid"]
    assert out == sorted(set(out))


def test_extra_keys_ignored():
    out = impl.solve({"encryption": "wpa2", "verified": True, "vpn": True,
                      "ssid": "Cafe", "signal": -42, "bssid": "aa:bb:cc"})
    assert out == []
