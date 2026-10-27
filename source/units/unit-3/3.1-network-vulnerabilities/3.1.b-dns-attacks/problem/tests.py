"""Test suite for 3.1.b — the blackbox acceptance contract.
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


def _r(frm, tx_id, port, qname, arrival):
    return {"from": frm, "tx_id": tx_id, "port": port, "qname": qname, "arrival": arrival}


def _q(qname, tx_id, port, replies):
    return {"qname": qname, "tx_id": tx_id, "port": port, "replies": replies}


# ---- visible cases -------------------------------------------------------

def test_poison_attacker_arrives_first():
    queries = [_q("bank.example", 48291, 33412, [
        _r("attacker", 48291, 33412, "bank.example", 1),
        _r("authoritative", 48291, 33412, "bank.example", 2),
    ])]
    assert impl.solve(queries) == ["POISON"]


def test_win_attacker_wrong_tx_id():
    queries = [_q("shop.example", 11020, 40500, [
        _r("attacker", 99999, 40500, "shop.example", 1),
        _r("authoritative", 11020, 40500, "shop.example", 2),
    ])]
    assert impl.solve(queries) == ["WIN"]


def test_reject_wrong_port():
    queries = [_q("mail.example", 5551, 21999, [
        _r("attacker", 5551, 9999, "mail.example", 1),
    ])]
    assert impl.solve(queries) == ["REJECT"]


def test_win_legit_arrives_first():
    queries = [_q("vpn.example", 7000, 51234, [
        _r("authoritative", 7000, 51234, "vpn.example", 1),
        _r("attacker", 7000, 51234, "vpn.example", 2),
    ])]
    assert impl.solve(queries) == ["WIN"]


def test_reject_wrong_qname():
    queries = [_q("cdn.example", 6002, 60111, [
        _r("attacker", 6002, 60111, "cdn-fake.example", 1),
    ])]
    assert impl.solve(queries) == ["REJECT"]


def test_empty_replies_is_reject():
    queries = [_q("sync.example", 3300, 22222, [])]
    assert impl.solve(queries) == ["REJECT"]


def test_empty_queries_list():
    assert impl.solve([]) == []


def test_mixed_batch_order_preserved():
    queries = [
        _q("z9.example", 1, 1, []),
        _q("front.example", 5, 5, [_r("authoritative", 5, 5, "front.example", 1)]),
        _q("vault.example", 9, 9, [_r("attacker", 9, 9, "vault.example", 1)]),
    ]
    assert impl.solve(queries) == ["REJECT", "WIN", "POISON"]


# ---- hidden / edge cases -------------------------------------------------

def test_flood_of_guessed_ids_all_miss_then_real_wins():
    """Kaminsky-style flood: multiple attacker guesses miss tx_id, real reply wins eventually."""
    queries = [_q("portal.example", 8123, 15000, [
        _r("attacker", 100, 15000, "portal.example", 1),
        _r("attacker", 200, 15000, "portal.example", 2),
        _r("authoritative", 8123, 15000, "portal.example", 3),
    ])]
    assert impl.solve(queries) == ["WIN"]


def test_flood_where_one_guess_hits_first():
    """One attacker guess matches all three fields and arrives before the real reply -> POISON."""
    queries = [_q("hr.example", 9500, 44210, [
        _r("attacker", 9500, 44210, "hr.example", 1),
        _r("attacker", 9500, 44210, "hr.example", 2),
        _r("authoritative", 9500, 44210, "hr.example", 3),
    ])]
    assert impl.solve(queries) == ["POISON"]


def test_replies_out_of_list_order_still_use_arrival_field():
    """Replies list is not sorted by arrival; arrival field (not list position) determines winner."""
    queries = [_q("late.example", 42, 42, [
        _r("authoritative", 42, 42, "late.example", 5),
        _r("attacker", 42, 42, "late.example", 2),
    ])]
    assert impl.solve(queries) == ["POISON"]


def test_only_qname_mismatch_among_otherwise_valid_replies():
    queries = [_q("real.example", 3, 3, [
        _r("attacker", 3, 3, "notreal.example", 1),
        _r("authoritative", 3, 3, "real.example", 2),
    ])]
    assert impl.solve(queries) == ["WIN"]


def test_multiple_valid_candidates_from_both_sides_lowest_arrival_wins():
    queries = [_q("multi.example", 7, 7, [
        _r("authoritative", 7, 7, "multi.example", 3),
        _r("attacker", 7, 7, "multi.example", 1),
        _r("attacker", 7, 7, "multi.example", 2),
    ])]
    assert impl.solve(queries) == ["POISON"]


def test_large_batch_deterministic():
    queries = []
    expected = []
    for i in range(20):
        if i % 3 == 0:
            queries.append(_q(f"q{i}.example", i, i, []))
            expected.append("REJECT")
        elif i % 3 == 1:
            queries.append(_q(f"q{i}.example", i, i, [_r("authoritative", i, i, f"q{i}.example", 1)]))
            expected.append("WIN")
        else:
            queries.append(_q(f"q{i}.example", i, i, [_r("attacker", i, i, f"q{i}.example", 1)]))
            expected.append("POISON")
    assert impl.solve(queries) == expected
