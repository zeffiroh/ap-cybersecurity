"""Test suite for 3.1.c — the blackbox acceptance contract.
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


def _r(ts, ip, mac):
    return {"ts": ts, "ip": ip, "mac": mac}


# ---- visible cases -------------------------------------------------------

def test_no_spoof_same_mac_refresh():
    replies = [
        _r(0, "192.168.1.1", "aa:01"),
        _r(30, "192.168.1.1", "aa:01"),
    ]
    assert impl.solve(replies) == []


def test_single_reply_not_flagged():
    replies = [_r(0, "192.168.1.50", "11:22")]
    assert impl.solve(replies) == []


def test_spoof_different_mac_flagged():
    replies = [
        _r(0, "192.168.1.1", "aa:01"),
        _r(15, "192.168.1.1", "de:ad"),
    ]
    assert impl.solve(replies) == ["192.168.1.1"]


def test_multiple_ips_only_spoofed_flagged():
    replies = [
        _r(0, "192.168.1.1", "aa:01"),
        _r(15, "192.168.1.1", "de:ad"),
        _r(0, "192.168.1.2", "bb:02"),
        _r(60, "192.168.1.2", "bb:02"),
    ]
    assert impl.solve(replies) == ["192.168.1.1"]


def test_sorted_output_no_duplicates():
    replies = [
        _r(0, "192.168.1.9", "aa:01"),
        _r(5, "192.168.1.9", "bb:02"),
        _r(10, "192.168.1.9", "cc:03"),
        _r(0, "192.168.1.2", "ff:00"),
        _r(5, "192.168.1.2", "ee:01"),
    ]
    assert impl.solve(replies) == ["192.168.1.2", "192.168.1.9"]


def test_empty_replies():
    assert impl.solve([]) == []


# ---- hidden / edge cases -------------------------------------------------

def test_replies_out_of_ts_order_in_list():
    """List order is not sorted by ts; the 'ts' field, not position, determines trust."""
    replies = [
        _r(50, "10.0.0.5", "attacker-mac"),
        _r(10, "10.0.0.5", "trusted-mac"),
    ]
    assert impl.solve(replies) == ["10.0.0.5"]


def test_three_replies_same_mac_after_first_change():
    """Once flagged (differs from trusted), further same-mac repeats don't un-flag it."""
    replies = [
        _r(0, "10.0.0.9", "trusted"),
        _r(5, "10.0.0.9", "attacker"),
        _r(10, "10.0.0.9", "attacker"),
    ]
    assert impl.solve(replies) == ["10.0.0.9"]


def test_stable_binding_many_refreshes():
    replies = [_r(t, "10.0.0.20", "stable-mac") for t in range(0, 100, 10)]
    assert impl.solve(replies) == []


def test_large_mixed_batch():
    replies = []
    expected = []
    for i in range(10):
        ip = f"10.0.1.{i}"
        replies.append(_r(0, ip, "m0"))
        if i % 2 == 0:
            replies.append(_r(10, ip, "m1"))  # different -> spoofed
            expected.append(ip)
        else:
            replies.append(_r(10, ip, "m0"))  # same -> not spoofed
    assert impl.solve(replies) == sorted(expected)
