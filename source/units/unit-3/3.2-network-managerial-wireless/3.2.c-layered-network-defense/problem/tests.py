"""Test suite for 3.2.c — the blackbox acceptance contract.
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


def _c(name, category):
    return {"name": name, "category": category}


# ---- visible cases -------------------------------------------------------

def test_perimeter_categories():
    controls = [_c("Border FW", "firewall"), _c("IPS sensor", "ips"), _c("DNS filter", "dns_filter")]
    assert impl.classify_layer(controls) == ["perimeter", "perimeter", "perimeter"]


def test_network_categories():
    controls = [_c("VLANs", "vlan_segmentation"), _c("Internal FW", "internal_firewall"), _c("WPA3", "wifi_protocol")]
    assert impl.classify_layer(controls) == ["network", "network", "network"]


def test_host_categories():
    controls = [_c("AV", "endpoint_av"), _c("Host FW", "host_firewall"), _c("Patching", "os_patching")]
    assert impl.classify_layer(controls) == ["host", "host", "host"]


def test_application_categories():
    controls = [_c("Input validation", "input_validation"), _c("WAF", "waf"), _c("App auth", "app_auth")]
    assert impl.classify_layer(controls) == ["application", "application", "application"]


def test_data_categories():
    controls = [_c("Encryption", "encryption_at_rest"), _c("DLP", "dlp"), _c("Classification", "data_classification")]
    assert impl.classify_layer(controls) == ["data", "data", "data"]


def test_human_categories():
    controls = [
        _c("Training", "awareness_training"), _c("AUP", "aup"),
        _c("Access review", "access_review"), _c("IR policy", "incident_response_policy"),
    ]
    assert impl.classify_layer(controls) == ["human", "human", "human", "human"]


def test_mixed_batch_order_preserved():
    controls = [_c("a", "firewall"), _c("b", "awareness_training"), _c("c", "encryption_at_rest")]
    assert impl.classify_layer(controls) == ["perimeter", "human", "data"]


def test_empty_controls():
    assert impl.classify_layer([]) == []


# ---- hidden / edge cases -------------------------------------------------

def test_name_text_does_not_affect_classification():
    """Even if name mentions 'firewall', category decides classification."""
    controls = [_c("The awareness firewall training program", "awareness_training")]
    assert impl.classify_layer(controls) == ["human"]


def test_all_sixteen_categories_full_batch():
    mapping = [
        ("firewall", "perimeter"), ("ips", "perimeter"), ("dns_filter", "perimeter"),
        ("vlan_segmentation", "network"), ("internal_firewall", "network"), ("wifi_protocol", "network"),
        ("endpoint_av", "host"), ("host_firewall", "host"), ("os_patching", "host"),
        ("input_validation", "application"), ("waf", "application"), ("app_auth", "application"),
        ("encryption_at_rest", "data"), ("dlp", "data"), ("data_classification", "data"),
        ("awareness_training", "human"), ("aup", "human"), ("access_review", "human"),
        ("incident_response_policy", "human"),
    ]
    controls = [_c(f"n{i}", cat) for i, (cat, _) in enumerate(mapping)]
    expected = [layer for _, layer in mapping]
    assert impl.classify_layer(controls) == expected


def test_large_repeated_batch_deterministic():
    controls = [_c(f"n{i}", "firewall") for i in range(10)]
    assert impl.classify_layer(controls) == ["perimeter"] * 10
