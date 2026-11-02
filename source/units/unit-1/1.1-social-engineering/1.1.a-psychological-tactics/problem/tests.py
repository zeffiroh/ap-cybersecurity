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


def test_urgency_and_intimidation():
    assert impl.solve("Your account will be locked in 24 hours. Act now.") == ["intimidation", "urgency"]


def test_authority_and_scarcity():
    assert impl.solve("This is the IT department. Limited spots - last chance.") == ["authority", "scarcity"]


def test_intimidation_and_urgency():
    assert impl.solve("Pay the penalty or we will take legal action immediately") == ["intimidation", "urgency"]


def test_none():
    assert impl.solve("Lunch is in the kitchen, help yourself.") == []


def test_case_insensitive():
    assert impl.solve("URGENT: the CEO needs this ASAP") == ["authority", "urgency"]


def test_dedup_sorted():
    out = impl.solve("urgent urgent act now - exclusive offer, only a few left")
    assert out == ["scarcity", "urgency"]
    assert out == sorted(set(out))


def test_empty_string():
    assert impl.solve("") == []
