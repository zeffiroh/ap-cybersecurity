"""Test suite for 1.2.c -- the blackbox acceptance contract.
Imports the implementation under test via IMPL env var so the SAME tests grade:
  - solution.py   (reference, must be green)
  - starter.py    (must be red until completed)
Default target is solution.py.

All expected values are derived from the algorithm in interface.md using Python's hmac+hashlib.
RFC 4226 test vectors are used for the core correctness cases to ensure determinism.

RFC 4226 test vector key (ASCII "12345678901234567890"):
  secret = "3132333435363738393031323334353637383930"
Known codes:
  step=1 (t=30..59)  -> "287082"
  step=2 (t=60..89)  -> "359152"
  step=3 (t=90..119) -> "969429"
"""
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


# ---- visible cases (RFC 4226 test vectors) ----------------------------------

def test_rfc_step1_correct():
    """RFC 4226 step=1: t=59 -> code '287082'."""
    assert impl.solve(RFC_SECRET, "287082", 59) is True


def test_rfc_step2_correct():
    """RFC 4226 step=2: t=89 -> code '359152'."""
    assert impl.solve(RFC_SECRET, "359152", 89) is True


def test_rfc_step3_correct():
    """RFC 4226 step=3: t=90 -> code '969429'."""
    assert impl.solve(RFC_SECRET, "969429", 90) is True


def test_wrong_code_rejected():
    """A wrong code for a valid step must return False."""
    assert impl.solve(RFC_SECRET, "000000", 59) is False


def test_expired_code_rejected():
    """Code for step=1 must be rejected at t=60 (step=2)."""
    # step=1 code is "287082"; at t=60 step=2 expects "359152"
    assert impl.solve(RFC_SECRET, "287082", 60) is False


# ---- hidden / edge cases ----------------------------------------------------

def test_same_step_different_timestamp():
    """t=30 and t=59 share step=1; both should accept the same code."""
    assert impl.solve(RFC_SECRET, "287082", 30) is True
    assert impl.solve(RFC_SECRET, "287082", 59) is True


def test_step_boundary():
    """t=60 is exactly the start of step=2; must accept step=2 code only."""
    assert impl.solve(RFC_SECRET, "359152", 60) is True
    assert impl.solve(RFC_SECRET, "287082", 60) is False  # step=1 code rejected at step=2


def test_t_zero():
    """t=0 is step=0; computed value must be deterministic."""
    # Compute expected: step=0, verify True/False is consistent
    result_true = impl.solve("0a1b2c3d", "497680", 0)
    result_false = impl.solve("0a1b2c3d", "000000", 0)
    assert result_true is True
    assert result_false is False


def test_different_key_same_time():
    """Different keys produce different codes at the same timestamp."""
    # Both at t=0 (step=0)
    # key "0a1b2c3d" -> "497680"; key "deadbeef" -> "057490"
    assert impl.solve("0a1b2c3d", "497680", 0) is True
    assert impl.solve("deadbeef", "057490", 0) is True
    # Cross-key: "0a1b2c3d" code must fail for "deadbeef" key
    assert impl.solve("deadbeef", "497680", 0) is False


def test_replay_blocked():
    """Code valid at t=59 (step=1) must be rejected at t=60 (step=2)."""
    # This is the core replay-prevention property
    valid_code = "287082"  # step=1
    assert impl.solve(RFC_SECRET, valid_code, 59) is True
    assert impl.solve(RFC_SECRET, valid_code, 60) is False
    assert impl.solve(RFC_SECRET, valid_code, 119) is False  # step=3 also wrong


def test_code_must_be_exact_string():
    """Code matching is an exact string comparison after zero-padding."""
    # "287082" passes; "28708" (5 digits) or "2870820" (7) should not match
    assert impl.solve(RFC_SECRET, "28708", 59) is False
    assert impl.solve(RFC_SECRET, " 287082", 59) is False
