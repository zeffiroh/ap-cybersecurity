"""Test suite for 2.3.c — the blackbox acceptance contract.
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


def _layer(name, category):
    return {"name": name, "category": category}


# ---- visible cases -------------------------------------------------------

def test_three_distinct_categories_adequate():
    layers = [
        _layer("chain-link fence + lighting", "perimeter"),
        _layer("badge reader on server room", "electronic"),
        _layer("lobby reception guard", "personnel"),
    ]
    result = impl.solve(layers)
    assert result == {
        "depth_score": 3,
        "categories_present": ["electronic", "perimeter", "personnel"],
        "redundant_categories": {},
        "recommendation": "ADEQUATE",
    }


def test_redundant_personnel_weak():
    layers = [
        _layer("lobby guard", "personnel"),
        _layer("roving night patrol", "personnel"),
        _layer("badge reader", "electronic"),
    ]
    result = impl.solve(layers)
    assert result == {
        "depth_score": 2,
        "categories_present": ["electronic", "personnel"],
        "redundant_categories": {"personnel": 1},
        "recommendation": "WEAK",
    }


def test_all_five_categories_strong():
    layers = [
        _layer("perimeter fence", "perimeter"),
        _layer("lobby guard", "personnel"),
        _layer("badge reader", "electronic"),
        _layer("mantrap", "barrier"),
        _layer("cctv feed", "monitoring"),
    ]
    result = impl.solve(layers)
    assert result["depth_score"] == 5
    assert result["categories_present"] == [
        "barrier", "electronic", "monitoring", "perimeter", "personnel",
    ]
    assert result["redundant_categories"] == {}
    assert result["recommendation"] == "STRONG"


def test_empty_layers():
    result = impl.solve([])
    assert result == {
        "depth_score": 0,
        "categories_present": [],
        "redundant_categories": {},
        "recommendation": "WEAK",
    }


def test_single_category_weak():
    layers = [_layer("badge reader", "electronic")]
    result = impl.solve(layers)
    assert result["depth_score"] == 1
    assert result["categories_present"] == ["electronic"]
    assert result["redundant_categories"] == {}
    assert result["recommendation"] == "WEAK"


def test_invalid_category_ignored():
    layers = [
        _layer("badge reader", "electronic"),
        _layer("lobby guard", "personnel"),
        _layer("guard dog", "canine"),  # invalid category, must be ignored
    ]
    result = impl.solve(layers)
    assert result["depth_score"] == 2
    assert result["categories_present"] == ["electronic", "personnel"]
    assert "canine" not in result["categories_present"]
    assert result["recommendation"] == "WEAK"


# ---- hidden / edge cases -------------------------------------------------

def test_four_categories_adequate_boundary():
    layers = [
        _layer("fence", "perimeter"),
        _layer("guard", "personnel"),
        _layer("badge reader", "electronic"),
        _layer("mantrap", "barrier"),
    ]
    result = impl.solve(layers)
    assert result["depth_score"] == 4
    assert result["recommendation"] == "ADEQUATE"


def test_two_categories_multiple_redundancies():
    layers = [
        _layer("guard A", "personnel"),
        _layer("guard B", "personnel"),
        _layer("guard C", "personnel"),
        _layer("cctv 1", "monitoring"),
        _layer("cctv 2", "monitoring"),
    ]
    result = impl.solve(layers)
    assert result["depth_score"] == 2
    assert result["categories_present"] == ["monitoring", "personnel"]
    assert result["redundant_categories"] == {"personnel": 2, "monitoring": 1}
    assert result["recommendation"] == "WEAK"


def test_only_invalid_categories_is_weak_empty():
    layers = [_layer("unicorn detector", "magic"), _layer("weather vane", "meteorology")]
    result = impl.solve(layers)
    assert result == {
        "depth_score": 0,
        "categories_present": [],
        "redundant_categories": {},
        "recommendation": "WEAK",
    }


def test_categories_present_sorted_regardless_of_input_order():
    layers = [
        _layer("cctv", "monitoring"),
        _layer("fence", "perimeter"),
        _layer("mantrap", "barrier"),
    ]
    result = impl.solve(layers)
    assert result["categories_present"] == ["barrier", "monitoring", "perimeter"]
