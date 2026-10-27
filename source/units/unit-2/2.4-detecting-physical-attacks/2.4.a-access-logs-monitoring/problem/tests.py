"""Test suite for 2.4.a — the blackbox acceptance contract.
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

# ---------------------------------------------------------------------------
# Helpers — seeded, deterministic test data
# ---------------------------------------------------------------------------
# Base timestamp: 2024-03-13 08:00:00 UTC = 1710316800
BASE = 1710316800
# After-hours base: 2024-03-13 23:00:00 UTC = 1710370800
AH = 1710370800


def _e(ts, badge, door, outcome):
    return {"ts": ts, "badge": badge, "door": door, "outcome": outcome}


# ---- visible cases -------------------------------------------------------

def test_rule0_burst_exactly_five():
    """Five denials within 60s triggers Rule 0."""
    entries = [_e(BASE + i * 10, "B-0001", "lobby", "DENIED") for i in range(5)]
    assert impl.solve(entries, set()) == ["B-0001"]


def test_rule0_four_denials_no_flag():
    """Four denials within 60s does NOT trigger Rule 0."""
    entries = [_e(BASE + i * 10, "B-0002", "lobby", "DENIED") for i in range(4)]
    assert impl.solve(entries, set()) == []


def test_rule1_after_hours_restricted():
    """GRANTED at restricted- door at 23:00 UTC triggers Rule 1."""
    entries = [_e(AH, "B-0003", "restricted-server-room", "GRANTED")]
    assert impl.solve(entries, set()) == ["B-0003"]


def test_rule1_after_hours_non_restricted_no_flag():
    """After-hours GRANTED at non-restricted door does NOT trigger Rule 1."""
    entries = [_e(AH, "B-0004", "lobby", "GRANTED")]
    assert impl.solve(entries, set()) == []


def test_rule2_location_inconsistency():
    """Same badge at two far doors within 600s triggers Rule 2."""
    fp = {frozenset({"door-A", "door-B"})}
    entries = [
        _e(BASE, "B-0005", "door-A", "GRANTED"),
        _e(BASE + 300, "B-0005", "door-B", "GRANTED"),
    ]
    assert impl.solve(entries, fp) == ["B-0005"]


def test_rule2_no_far_pair_no_flag():
    """Same badge at two doors within 600s but NOT a far pair does NOT flag."""
    entries = [
        _e(BASE, "B-0006", "door-A", "GRANTED"),
        _e(BASE + 300, "B-0006", "door-C", "GRANTED"),
    ]
    fp = {frozenset({"door-A", "door-B"})}  # door-C not paired with door-A
    assert impl.solve(entries, fp) == []


def test_empty_entries():
    """Empty log returns empty list."""
    assert impl.solve([], set()) == []


def test_multiple_badges_some_flagged():
    """Only the badge that crosses a threshold is returned; others are clean."""
    entries = (
        [_e(BASE + i * 10, "B-0007", "lobby", "DENIED") for i in range(6)]
        + [_e(BASE + 100, "B-0008", "lobby", "DENIED")]  # single denial — clean
    )
    assert impl.solve(entries, set()) == ["B-0007"]


# ---- hidden / edge cases -------------------------------------------------

def test_rule0_spread_across_61s_no_flag():
    """Five denials spread across 61s do NOT form a 60s window of 5."""
    entries = [_e(BASE + i * 16, "B-0009", "lobby", "DENIED") for i in range(5)]
    # deltas: 0,16,32,48,64 — last pair 0..64 = 64s > 60s; 16..64 = 48s but only 4 in window
    assert impl.solve(entries, set()) == []


def test_rule1_boundary_hour_22():
    """GRANTED at restricted- door at exactly hour 22 UTC triggers Rule 1."""
    ts_22 = 1710370800 - 3600  # 22:00 UTC on 2024-03-13
    entries = [_e(ts_22, "B-0010", "restricted-vault", "GRANTED")]
    assert impl.solve(entries, set()) == ["B-0010"]


def test_rule2_gap_exactly_600s():
    """Gap of exactly 600s between far-door GRANTEDs triggers Rule 2 (<=600)."""
    fp = {frozenset({"site-X", "site-Y"})}
    entries = [
        _e(BASE, "B-0011", "site-X", "GRANTED"),
        _e(BASE + 600, "B-0011", "site-Y", "GRANTED"),
    ]
    assert impl.solve(entries, fp) == ["B-0011"]


def test_output_sorted_multiple_flags():
    """Result is sorted when multiple badges are flagged."""
    entries = (
        [_e(BASE + i * 10, "B-0013", "lobby", "DENIED") for i in range(5)]
        + [_e(BASE + i * 10, "B-0012", "lobby", "DENIED") for i in range(5)]
    )
    result = impl.solve(entries, set())
    assert result == sorted(result)
    assert "B-0012" in result and "B-0013" in result
