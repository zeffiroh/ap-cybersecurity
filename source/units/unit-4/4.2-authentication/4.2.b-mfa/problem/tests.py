"""Test suite for 4.2.b — the blackbox acceptance contract.
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
def test_example_password_only():
    assert impl.solve(["password"]) == "single_factor"


def test_example_two_passwords():
    assert impl.solve(["password", "password"]) == "single_factor"


def test_example_password_security_question():
    assert impl.solve(["password", "security_question"]) == "single_factor"


def test_example_password_sms():
    assert impl.solve(["password", "sms_code"]) == "mfa_phishable"


def test_example_password_push():
    assert impl.solve(["password", "push_approved"]) == "mfa_phishable"


def test_example_password_hardware_key():
    assert impl.solve(["password", "hardware_key"]) == "mfa_phishing_resistant"


# ---- hidden / edge cases -------------------------------------------------
def test_edge_empty_list():
    assert impl.solve([]) == "single_factor"


def test_edge_unknown_factor_only():
    assert impl.solve(["carrier_pigeon"]) == "single_factor"


def test_edge_unknown_plus_known_single_category():
    # unrecognized factor is ignored; only "password" (knowledge) remains -> single_factor
    assert impl.solve(["password", "carrier_pigeon"]) == "single_factor"


def test_biometric_plus_password_is_phishable_not_resistant():
    # knowledge + inherence = 2 distinct categories, but no phishing-resistant possession
    # factor was used, so it falls to mfa_phishable per the spec.
    assert impl.solve(["biometric", "password"]) == "mfa_phishable"


def test_fido2_string_variant():
    assert impl.solve(["password", "fido2"]) == "mfa_phishing_resistant"


def test_priority_hardware_key_wins_over_phishable_factor():
    # hardware_key present alongside a phishable sms_code -> still phishing-resistant result
    assert impl.solve(["password", "sms_code", "hardware_key"]) == "mfa_phishing_resistant"
