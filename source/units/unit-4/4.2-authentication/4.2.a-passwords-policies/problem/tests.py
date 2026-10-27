"""Test suite for 4.2.a — the blackbox acceptance contract.
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


# ---- visible cases (from prompt.md) --------------------------------------
def test_example_1_multiple_violations():
    result = impl.validate_password(
        "abc", {"min_length": 12, "require_upper": True, "require_digit": True}
    )
    assert result == ["too_short", "no_upper", "no_digit"]


def test_example_2_banned_list():
    result = impl.validate_password("Password123", {"banned_list": ["password123"]})
    assert result == ["in_banned_list"]


def test_example_3_fully_compliant():
    policy = {
        "min_length": 12,
        "require_upper": True,
        "require_lower": True,
        "require_digit": True,
        "require_symbol": True,
        "banned_list": ["password123"],
        "history": ["OldPass2023!"],
    }
    result = impl.validate_password("Tr0ub4dor&3xtra!", policy)
    assert result == []


# ---- hidden / edge cases ---------------------------------------------------
def test_edge_empty_password_with_requirements():
    policy = {
        "min_length": 8,
        "require_upper": True,
        "require_lower": True,
        "require_digit": True,
        "require_symbol": True,
    }
    result = impl.validate_password("", policy)
    assert result == ["too_short", "no_upper", "no_lower", "no_digit", "no_symbol"]


def test_edge_empty_policy_dict():
    # No keys at all -> everything defaults to "not required" -> compliant.
    assert impl.validate_password("anything", {}) == []
    assert impl.validate_password("", {}) == []


def test_reused_password_case_sensitive():
    policy = {"history": ["OldPass2023!", "OldPass2024!"]}
    assert impl.validate_password("OldPass2023!", policy) == ["reused_password"]
    # Different case does not count as reused (history is case-sensitive exact match).
    assert impl.validate_password("oldpass2023!", policy) == []


def test_banned_list_case_insensitive():
    policy = {"banned_list": ["LetMeIn"]}
    assert impl.validate_password("letmein", policy) == ["in_banned_list"]
    assert impl.validate_password("LETMEIN", policy) == ["in_banned_list"]


def test_require_symbol_definition():
    policy = {"require_symbol": True}
    assert impl.validate_password("abcXYZ123", policy) == ["no_symbol"]
    assert impl.validate_password("abcXYZ123!", policy) == []
    assert impl.validate_password("abc XYZ123", policy) == []  # space counts as a symbol


def test_exact_ordering_multiple_violations():
    # Violates every rule at once; asserts EXACT order per interface.md.
    policy = {
        "min_length": 20,
        "require_upper": True,
        "require_lower": True,
        "require_digit": True,
        "require_symbol": True,
        "banned_list": ["short"],
        "history": ["short"],
    }
    result = impl.validate_password("short", policy)
    assert result == [
        "too_short",
        "no_upper",
        "no_digit",
        "no_symbol",
        "in_banned_list",
        "reused_password",
    ]


def test_only_min_length_enforced():
    policy = {"min_length": 6}
    assert impl.validate_password("abc", policy) == ["too_short"]
    assert impl.validate_password("abcdef", policy) == []
