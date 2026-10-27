"""Test suite for 1.1.b — the blackbox acceptance contract.
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

def test_lookalike_domain():
    assert impl.solve("http://paypa1.com/verify?id=38291") == ["lookalike-domain"]


def test_ip_url():
    assert impl.solve("http://192.168.4.99/reset?user=jsmith") == ["ip-url"]


def test_dangerous_extension_filename():
    assert impl.solve("new_hire_form.pdf.exe") == ["dangerous-extension"]


def test_lookalike_and_mismatched():
    # bankofamerica.com.secure-login.xyz: reg domain is secure-login.xyz (not trusted),
    # but bankofamerica appears in the URL outside the reg domain => mismatched-link.
    # secure-login.xyz is not in LOOKALIKE_DOMAINS so no lookalike-domain here.
    result = impl.solve("http://bankofamerica.com.secure-login.xyz/stmt/2026-05.pdf")
    assert "mismatched-link" in result


def test_clean_url():
    assert impl.solve("http://shop.example/track/44821") == []


def test_lookalike_and_dangerous_extension_url():
    result = impl.solve("http://dropbx.com/s/Q3.scr")
    assert result == ["dangerous-extension", "lookalike-domain"]


# ---- hidden / edge cases -------------------------------------------------

def test_empty_string():
    assert impl.solve("") == []


def test_scr_extension_filename():
    assert impl.solve("Q3_Report.scr") == ["dangerous-extension"]


def test_ps1_extension():
    assert impl.solve("http://company.example/setup.ps1") == ["dangerous-extension"]


def test_case_insensitive_extension():
    assert impl.solve("malware.EXE") == ["dangerous-extension"]


def test_ip_url_with_port():
    assert impl.solve("http://10.0.0.1:8080/admin") == ["ip-url"]


def test_clean_filename():
    assert impl.solve("report.pdf") == []


def test_sorted_output():
    result = impl.solve("http://dropbx.com/s/Q3.scr")
    assert result == sorted(result)


def test_dedup():
    # Even if multiple rules could fire the same indicator, it appears once
    result = impl.solve("http://paypa1.com/path.exe")
    assert result == sorted(set(result))
