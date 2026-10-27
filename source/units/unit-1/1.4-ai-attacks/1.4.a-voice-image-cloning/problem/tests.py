"""Test suite for 1.4.a — the blackbox acceptance contract.
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
def test_no_shared_secret_suspect():
    assert impl.solve({"no_shared_secret": True}) == "suspect"


def test_refused_callback_suspect():
    assert impl.solve({"refused_callback": True}) == "suspect"


def test_audio_plus_money_suspect():
    assert impl.solve({"audio_artifact": True, "urgent_money_request": True}) == "suspect"


def test_spoofed_plus_unverified_suspect():
    assert impl.solve({"caller_id_spoofed": True, "unverified_channel": True}) == "suspect"


def test_video_face_mismatch_suspect():
    assert impl.solve({"video_face_mismatch": True}) == "suspect"


def test_money_plus_unverified_suspect():
    assert impl.solve({"urgent_money_request": True, "unverified_channel": True}) == "suspect"


def test_empty_ok():
    assert impl.solve({}) == "ok"


def test_single_money_ok():
    # urgent money alone (no second signal) is NOT enough under rules 3 or 6
    assert impl.solve({"urgent_money_request": True}) == "ok"


def test_audio_only_ok():
    # audio artifact alone does not trigger without money request
    assert impl.solve({"audio_artifact": True}) == "ok"


# ---- hidden / edge cases -------------------------------------------------
def test_missing_keys_treated_false():
    # caller_id_spoofed True but unverified_channel absent -> rule 4 does not fire
    assert impl.solve({"caller_id_spoofed": True}) == "ok"


def test_all_false_ok():
    signals = {k: False for k in [
        "unverified_channel", "urgent_money_request", "audio_artifact",
        "no_shared_secret", "caller_id_spoofed", "video_face_mismatch", "refused_callback",
    ]}
    assert impl.solve(signals) == "ok"


def test_rule1_takes_priority():
    # even if other signals are also set, rule 1 should still fire first
    assert impl.solve({
        "no_shared_secret": True,
        "audio_artifact": True,
        "urgent_money_request": True,
        "refused_callback": True,
    }) == "suspect"


def test_unverified_channel_alone_ok():
    assert impl.solve({"unverified_channel": True}) == "ok"
