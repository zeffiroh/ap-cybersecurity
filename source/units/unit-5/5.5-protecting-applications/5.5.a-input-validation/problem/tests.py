"""Test suite for 5.5.a — the blackbox acceptance contract.
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
def test_all_valid_none_blocked():
    subs = [
        {"field": "zip", "type": "zip", "value": "94107"},
        {"field": "email", "type": "email", "value": "user@example.com"},
        {"field": "qty", "type": "quantity", "value": "5"},
    ]
    assert impl.solve(subs) == []


def test_bad_zip_blocked():
    subs = [{"field": "zip", "type": "zip", "value": "9410"}]
    assert impl.solve(subs) == ["9410"]


def test_sql_injection_blocked_even_if_type_matches_shape():
    subs = [{"field": "username", "type": "username", "value": "admin'--"}]
    assert impl.solve(subs) == ["admin'--"]


def test_xss_payload_blocked():
    subs = [{"field": "username", "type": "username", "value": "<script>x</script>"}]
    assert impl.solve(subs) == ["<script>x</script>"]


def test_order_preserved_and_only_blocked_returned():
    subs = [
        {"field": "zip", "type": "zip", "value": "94107"},
        {"field": "zip", "type": "zip", "value": "abcde"},
        {"field": "qty", "type": "quantity", "value": "150"},
        {"field": "email", "type": "email", "value": "a@b.com"},
    ]
    assert impl.solve(subs) == ["abcde", "150"]


# ---- hidden / edge cases -------------------------------------------------
def test_quantity_zero_and_out_of_range_blocked():
    subs = [
        {"field": "qty", "type": "quantity", "value": "0"},
        {"field": "qty", "type": "quantity", "value": "100"},
        {"field": "qty", "type": "quantity", "value": "99"},
    ]
    assert impl.solve(subs) == ["0", "100"]


def test_union_select_blocked_regardless_of_case():
    subs = [{"field": "search", "type": "username", "value": "foo union select 1"}]
    assert impl.solve(subs) == ["foo union select 1"]


def test_path_traversal_blocked():
    subs = [{"field": "file", "type": "username", "value": "../etc/passwd"}]
    assert impl.solve(subs) == ["../etc/passwd"]


def test_empty_input():
    assert impl.solve([]) == []
