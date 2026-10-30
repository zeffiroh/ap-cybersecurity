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


def test_edge_empty_dict_is_secure():
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
    device = {"default_password": True, "firmware_outdated": True, "open_ports": [23, 21],
              "unauthenticated_api": True, "encrypted_traffic": False}
    assert impl.solve(device) == "default_credentials"

    device2 = {"default_password": False, "firmware_outdated": True, "open_ports": [23],
               "unauthenticated_api": True, "encrypted_traffic": False}
    assert impl.solve(device2) == "outdated_firmware"

    device3 = {"default_password": False, "firmware_outdated": False, "open_ports": [23],
               "unauthenticated_api": True, "encrypted_traffic": False}
    assert impl.solve(device3) == "exposed_port"
