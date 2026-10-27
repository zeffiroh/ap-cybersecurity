"""Test suite for 4.2.c — the blackbox acceptance contract.
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
def test_example_1():
    assert impl.solve("Session token was sniffed over unencrypted HTTP and replayed by an attacker") == "hijacking"


def test_example_2():
    assert impl.solve("Attacker sent a link with a pre-set session id; victim logged in and id unchanged") == "fixation"


def test_example_3():
    assert impl.solve("Session cookie has no HttpOnly flag configured; automated scan flagged the missing attribute") == "insecure_cookie"


def test_example_4():
    assert impl.solve("Logged-in kiosk left unattended for hours with no idle timeout configured") == "timeout_issue"


def test_example_5():
    assert impl.solve("Session id regenerated at login; cookie set Secure, HttpOnly, SameSite=Strict") == "secure"


def test_example_6():
    assert impl.solve("User changed their display name in account settings") == "unknown"


# ---- hidden / edge cases -------------------------------------------------
def test_edge_empty():
    assert impl.solve("") == "unknown"


def test_case_insensitive():
    assert impl.solve("TOKEN WAS SNIFFED ON PUBLIC WIFI") == "hijacking"
    assert impl.solve("COOKIE IS MISSING THE SECURE FLAG") == "insecure_cookie"


def test_priority_fixation_over_hijacking():
    # contains "pre-set session" (fixation) and "sniffed" (hijacking).
    # fixation must win per interface.md priority order.
    assert impl.solve("Attacker used a pre-set session id; token was later sniffed too") == "fixation"


def test_priority_hijacking_over_insecure_cookie():
    # contains "intercepted" (hijacking) and "missing httponly" (insecure_cookie).
    # hijacking must win per interface.md priority order.
    assert impl.solve("Token was intercepted; cookie also missing httponly flag") == "hijacking"
