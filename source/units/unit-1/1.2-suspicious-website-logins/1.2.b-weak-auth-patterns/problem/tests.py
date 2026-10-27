"""Test suite for 1.2.b -- the blackbox acceptance contract.
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

def test_dict_only_lc_short():
    """'password' is short, in dictionary, and only lowercase."""
    result = impl.solve("password")
    assert result["weak"] is True
    assert result["reasons"] == ["in_dictionary", "only_lowercase", "too_short"]


def test_sequential_only():
    """'Tr0ub4dor&3abcde' is long, mixed, not in dictionary, but has 'abc'."""
    result = impl.solve("Tr0ub4dor&3abcde")
    assert result["weak"] is True
    assert result["reasons"] == ["sequential_or_repeated"]


def test_strong():
    """'mXk9#vLq2@nP' passes all rules."""
    result = impl.solve("mXk9#vLq2@nP")
    assert result["weak"] is False
    assert result["reasons"] == []


def test_dictionary_with_mangling():
    """'P@ssword!2024' is long and mixed but base 'passw0rd' is in dictionary."""
    # Note: 'passw0rd' IS in COMMON_WORDS; 'P@ssword!2024'.lower() = 'p@ssword!2024' is NOT.
    # However 'pa$$word' IS: test a direct dictionary hit with symbols.
    result = impl.solve("pa$$word")
    assert result["weak"] is True
    assert "in_dictionary" in result["reasons"]
    assert "too_short" in result["reasons"]


# ---- hidden / edge cases -------------------------------------------------

def test_empty_string():
    """Empty string is too_short only (not only_lowercase, not in dictionary)."""
    result = impl.solve("")
    assert result["weak"] is True
    assert result["reasons"] == ["too_short"]


def test_repeated_chars():
    """'HelloWorld111' triggers sequential_or_repeated due to '111'."""
    result = impl.solve("HelloWorld111")
    assert result["weak"] is True
    assert result["reasons"] == ["sequential_or_repeated"]


def test_only_lowercase_flag():
    """All-lowercase short word triggers both too_short and only_lowercase."""
    result = impl.solve("sunshine")
    assert "only_lowercase" in result["reasons"]
    assert "too_short" in result["reasons"]
    assert "in_dictionary" in result["reasons"]


def test_reasons_sorted():
    """Reasons list is always sorted ascending regardless of check order."""
    result = impl.solve("qwerty")
    assert result["reasons"] == sorted(result["reasons"])


def test_sequential_digits():
    """'Abcdef123456!' is long and mixed but contains '123' sequential run."""
    result = impl.solve("Abcdef123456!")
    assert result["weak"] is True
    assert "sequential_or_repeated" in result["reasons"]


def test_exactly_12_chars_passes_length():
    """A 12-character password that is otherwise clean should not trigger too_short."""
    # 'zQm7!kLp3$Rw' -- 12 chars, mixed, not in dictionary, no sequences
    result = impl.solve("zQm7!kLp3$Rw")
    assert "too_short" not in result["reasons"]


def test_weak_flag_matches_reasons():
    """'weak' must be True iff reasons is non-empty."""
    for pw in ["mXk9#vLq2@nP", "password", "HelloWorld111", ""]:
        result = impl.solve(pw)
        assert result["weak"] == (len(result["reasons"]) > 0)
