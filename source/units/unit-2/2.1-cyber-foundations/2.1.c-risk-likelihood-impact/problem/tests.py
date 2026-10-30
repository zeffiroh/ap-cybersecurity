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


def test_avoid():
    data = [
        {"name": "r1", "likelihood": 5, "impact": 4, "cost": 61, "value": 100}
    ]
    assert impl.solve(data) == {"r1": "Avoid"}


def test_mitigate_high():
    data = [
        {"name": "r1", "likelihood": 3, "impact": 5, "cost": 30, "value": 100}
    ]
    assert impl.solve(data) == {"r1": "Mitigate"}


def test_transfer():
    data = [
        {"name": "r1", "likelihood": 3, "impact": 5, "cost": 31, "value": 100}
    ]
    assert impl.solve(data) == {"r1": "Transfer"}


def test_mitigate_low():
    data = [
        {"name": "r1", "likelihood": 2, "impact": 3, "cost": 10, "value": 100}
    ]
    assert impl.solve(data) == {"r1": "Mitigate"}


def test_accept():
    data = [
        {"name": "r1", "likelihood": 2, "impact": 2, "cost": 5, "value": 100},
        {"name": "r2", "likelihood": 2, "impact": 3, "cost": 11, "value": 100}
    ]
    assert impl.solve(data) == {"r1": "Accept", "r2": "Accept"}


def test_edge_empty():
    assert impl.solve([]) == {}


def test_multiple():
    data = [
        {"name": "avoid_it", "likelihood": 5, "impact": 5, "cost": 80, "value": 100},
        {"name": "mitigate_high", "likelihood": 4, "impact": 4, "cost": 25, "value": 100},
        {"name": "transfer_it", "likelihood": 3, "impact": 5, "cost": 40, "value": 100},
        {"name": "mitigate_low", "likelihood": 2, "impact": 4, "cost": 8, "value": 100},
        {"name": "accept_low", "likelihood": 1, "impact": 3, "cost": 10, "value": 100},
        {"name": "accept_costly", "likelihood": 3, "impact": 4, "cost": 50, "value": 100}
    ]
    expected = {
        "avoid_it": "Avoid",
        "mitigate_high": "Mitigate",
        "transfer_it": "Transfer",
        "mitigate_low": "Mitigate",
        "accept_low": "Accept",
        "accept_costly": "Accept"
    }
    assert impl.solve(data) == expected

