"""Test suite for 4.4.b — the blackbox acceptance contract.
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
def test_example_1_prompt_scenario():
    entries = [
        {"ts": 0, "user": "jsmith", "result": "FAILED"},
        {"ts": 13, "user": "jsmith", "result": "FAILED"},
        {"ts": 21, "user": "jsmith", "result": "FAILED"},
        {"ts": 30, "user": "jsmith", "result": "FAILED"},
        {"ts": 38, "user": "jsmith", "result": "FAILED"},
        {"ts": 46, "user": "jsmith", "result": "SUCCESS"},
        {"ts": 100, "user": "agarcia", "result": "FAILED"},
        {"ts": 1662, "user": "agarcia", "result": "FAILED"},
    ]
    assert impl.solve(entries) == ["jsmith"]


def test_example_2_no_flags():
    entries = [
        {"ts": 0, "user": "mchen", "result": "SUCCESS"},
        {"ts": 500, "user": "rpatel", "result": "FAILED"},
        {"ts": 1700, "user": "rpatel", "result": "FAILED"},
    ]
    assert impl.solve(entries) == []


# ---- hidden / edge cases -------------------------------------------------
def test_edge_empty_entries():
    assert impl.solve([]) == []


def test_fewer_than_five_failures_never_flagged():
    entries = [
        {"ts": t, "user": "twilson", "result": "FAILED"} for t in [0, 5, 10, 15]
    ]
    assert impl.solve(entries) == []


def test_five_failures_exactly_at_60s_boundary_flags():
    entries = [
        {"ts": t, "user": "bwright", "result": "FAILED"} for t in [0, 15, 30, 45, 60]
    ]
    assert impl.solve(entries) == ["bwright"]


def test_five_failures_just_over_60s_does_not_flag():
    entries = [
        {"ts": t, "user": "bwright", "result": "FAILED"} for t in [0, 15, 30, 45, 61]
    ]
    assert impl.solve(entries) == []


def test_out_of_order_input_still_correlated_correctly():
    entries = [
        {"ts": 46, "user": "jsmith", "result": "SUCCESS"},
        {"ts": 21, "user": "jsmith", "result": "FAILED"},
        {"ts": 0, "user": "jsmith", "result": "FAILED"},
        {"ts": 38, "user": "jsmith", "result": "FAILED"},
        {"ts": 13, "user": "jsmith", "result": "FAILED"},
        {"ts": 30, "user": "jsmith", "result": "FAILED"},
    ]
    assert impl.solve(entries) == ["jsmith"]


def test_sliding_window_finds_cluster_not_just_first_and_last():
    # 7 failures total; the FIRST-to-LAST span is 200s (too wide), but a 5-in-a-row
    # cluster from index 1..5 spans only 40s and should still trigger the flag.
    entries = [
        {"ts": 0, "user": "cluster", "result": "FAILED"},
        {"ts": 100, "user": "cluster", "result": "FAILED"},
        {"ts": 110, "user": "cluster", "result": "FAILED"},
        {"ts": 120, "user": "cluster", "result": "FAILED"},
        {"ts": 130, "user": "cluster", "result": "FAILED"},
        {"ts": 140, "user": "cluster", "result": "FAILED"},
        {"ts": 200, "user": "cluster", "result": "FAILED"},
    ]
    assert impl.solve(entries) == ["cluster"]


def test_multiple_users_result_sorted_alphabetically():
    entries = []
    for t in [0, 10, 20, 30, 40]:
        entries.append({"ts": t, "user": "zach", "result": "FAILED"})
    for t in [0, 10, 20, 30, 40]:
        entries.append({"ts": t, "user": "amy", "result": "FAILED"})
    assert impl.solve(entries) == ["amy", "zach"]


def test_success_entries_do_not_count_as_failures():
    entries = [
        {"ts": 0, "user": "user1", "result": "SUCCESS"},
        {"ts": 5, "user": "user1", "result": "FAILED"},
        {"ts": 10, "user": "user1", "result": "SUCCESS"},
        {"ts": 15, "user": "user1", "result": "FAILED"},
        {"ts": 20, "user": "user1", "result": "SUCCESS"},
        {"ts": 25, "user": "user1", "result": "FAILED"},
    ]
    assert impl.solve(entries) == []
