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


def test_dict_only_lc_short():
    result = impl.solve("password")
    assert result["weak"] is True
    assert result["reasons"] == ["in_dictionary", "only_lowercase", "too_short"]


def test_sequential_only():
    result = impl.solve("Tr0ub4dor&3abcde")
    assert result["weak"] is True
    assert result["reasons"] == ["sequential_or_repeated"]


def test_strong():
    result = impl.solve("mXk9#vLq2@nP")
    assert result["weak"] is False
    assert result["reasons"] == []


def test_dictionary_with_mangling():
    result = impl.solve("pa$$word")
    assert result["weak"] is True
    assert "in_dictionary" in result["reasons"]
    assert "too_short" in result["reasons"]


def test_empty_string():
    result = impl.solve("")
    assert result["weak"] is True
    assert result["reasons"] == ["too_short"]


def test_repeated_chars():
    result = impl.solve("HelloWorld111")
    assert result["weak"] is True
    assert result["reasons"] == ["sequential_or_repeated"]


def test_only_lowercase_flag():
    result = impl.solve("sunshine")
    assert "only_lowercase" in result["reasons"]
    assert "too_short" in result["reasons"]
    assert "in_dictionary" in result["reasons"]


def test_reasons_sorted():
    result = impl.solve("qwerty")
    assert result["reasons"] == sorted(result["reasons"])


def test_sequential_digits():
    result = impl.solve("Abcdef123456!")
    assert result["weak"] is True
    assert "sequential_or_repeated" in result["reasons"]


def test_exactly_12_chars_passes_length():
    result = impl.solve("zQm7!kLp3$Rw")
    assert "too_short" not in result["reasons"]


def test_weak_flag_matches_reasons():
    for pw in ["mXk9#vLq2@nP", "password", "HelloWorld111", ""]:
        result = impl.solve(pw)
        assert result["weak"] == (len(result["reasons"]) > 0)
