"""Test suite for 4.1.c — the blackbox acceptance contract.
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
def test_example_default_credentials():
    device = {"default_password": True, "firmware_outdated": True, "open_ports": [23],
              "unauthenticated_api": True, "encrypted_traffic": False}
    assert impl.solve(device) == "default_credentials"


def test_example_outdated_firmware():
    device = {"default_password": False, "firmware_outdated": True, "open_ports": [443],
              "unauthenticated_api": False, "encrypted_traffic": True}
    assert impl.solve(device) == "outdated_firmware"


def test_example_exposed_port():
    device = {"default_password": False, "firmware_outdated": False, "open_ports": [23, 443],
              "unauthenticated_api": False, "encrypted_traffic": True}
    assert impl.solve(device) == "exposed_port"


def test_example_unauthenticated_api():
    device = {"default_password": False, "firmware_outdated": False, "open_ports": [443],
              "unauthenticated_api": True, "encrypted_traffic": True}
    assert impl.solve(device) == "unauthenticated_api"


def test_example_unencrypted_traffic():
    device = {"default_password": False, "firmware_outdated": False, "open_ports": [443],
              "unauthenticated_api": False, "encrypted_traffic": False}
    assert impl.solve(device) == "unencrypted_traffic"


def test_example_secure():
    device = {"default_password": False, "firmware_outdated": False, "open_ports": [443],
              "unauthenticated_api": False, "encrypted_traffic": True}
    assert impl.solve(device) == "secure"


# ---- hidden / edge cases -------------------------------------------------
def test_edge_empty_dict_is_secure():
    # missing keys default to the safe value for that key
    assert impl.solve({}) == "secure"


def test_edge_empty_open_ports():
    device = {"default_password": False, "firmware_outdated": False, "open_ports": [],
              "unauthenticated_api": False, "encrypted_traffic": True}
    assert impl.solve(device) == "secure"


def test_port_21_also_exposed():
    device = {"default_password": False, "firmware_outdated": False, "open_ports": [21, 8080],
              "unauthenticated_api": False, "encrypted_traffic": True}
    assert impl.solve(device) == "exposed_port"


def test_other_ports_do_not_count():
    device = {"default_password": False, "firmware_outdated": False, "open_ports": [80, 8080, 3389],
              "unauthenticated_api": False, "encrypted_traffic": True}
    assert impl.solve(device) == "secure"


def test_priority_order():
    # everything is wrong at once — must return the HIGHEST priority verdict
    device = {"default_password": True, "firmware_outdated": True, "open_ports": [23, 21],
              "unauthenticated_api": True, "encrypted_traffic": False}
    assert impl.solve(device) == "default_credentials"

    # no default password, but everything else wrong -> outdated_firmware wins next
    device2 = {"default_password": False, "firmware_outdated": True, "open_ports": [23],
               "unauthenticated_api": True, "encrypted_traffic": False}
    assert impl.solve(device2) == "outdated_firmware"

    # only port + api + traffic wrong -> exposed_port wins over the two below it
    device3 = {"default_password": False, "firmware_outdated": False, "open_ports": [23],
               "unauthenticated_api": True, "encrypted_traffic": False}
    assert impl.solve(device3) == "exposed_port"
