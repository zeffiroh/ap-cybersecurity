import importlib.util
import os
import pathlib

_HERE = pathlib.Path(__file__).parent
_TARGET = os.environ.get("IMPL", str(_HERE / "solution.py"))

RFC_SECRET = "3132333435363738393031323334353637383930"


def _load(path):
    spec = importlib.util.spec_from_file_location("impl", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


impl = _load(_TARGET)


def test_rfc_step1_correct():
    assert impl.solve(RFC_SECRET, "287082", 59) is True


def test_rfc_step2_correct():
    assert impl.solve(RFC_SECRET, "359152", 89) is True


def test_rfc_step3_correct():
    assert impl.solve(RFC_SECRET, "969429", 90) is True


def test_wrong_code_rejected():
    assert impl.solve(RFC_SECRET, "000000", 59) is False


def test_expired_code_rejected():
    assert impl.solve(RFC_SECRET, "287082", 60) is False


def test_same_step_different_timestamp():
    assert impl.solve(RFC_SECRET, "287082", 30) is True
    assert impl.solve(RFC_SECRET, "287082", 59) is True


def test_step_boundary():
    assert impl.solve(RFC_SECRET, "359152", 60) is True
    assert impl.solve(RFC_SECRET, "287082", 60) is False


def test_t_zero():
    result_true = impl.solve("0a1b2c3d", "497680", 0)
    result_false = impl.solve("0a1b2c3d", "000000", 0)
    assert result_true is True
    assert result_false is False


def test_different_key_same_time():
    assert impl.solve("0a1b2c3d", "497680", 0) is True
    assert impl.solve("deadbeef", "057490", 0) is True
    assert impl.solve("deadbeef", "497680", 0) is False


def test_replay_blocked():
    valid_code = "287082"
    assert impl.solve(RFC_SECRET, valid_code, 59) is True
    assert impl.solve(RFC_SECRET, valid_code, 60) is False
    assert impl.solve(RFC_SECRET, valid_code, 119) is False


def test_code_must_be_exact_string():
    assert impl.solve(RFC_SECRET, "28708", 59) is False
    assert impl.solve(RFC_SECRET, " 287082", 59) is False
