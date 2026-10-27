"""Test suite for 5.6.b — the blackbox acceptance contract.
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
def test_large_transfer_to_unapproved_flagged():
    transfers = [{"id": "t1", "bytes_mb": 500, "destination": "unknown-cloud.example"}]
    assert impl.solve(transfers, ["corp-backup.internal"], volume_threshold_mb=100) == ["t1"]


def test_large_transfer_to_approved_not_flagged():
    transfers = [{"id": "t2", "bytes_mb": 500, "destination": "corp-backup.internal"}]
    assert impl.solve(transfers, ["corp-backup.internal"], volume_threshold_mb=100) == []


def test_small_transfer_to_unapproved_not_flagged():
    transfers = [{"id": "t3", "bytes_mb": 5, "destination": "unknown-cloud.example"}]
    assert impl.solve(transfers, ["corp-backup.internal"], volume_threshold_mb=100) == []


def test_multiple_transfers_only_matching_flagged():
    transfers = [
        {"id": "a", "bytes_mb": 200, "destination": "evil.example"},
        {"id": "b", "bytes_mb": 50, "destination": "evil.example"},
        {"id": "c", "bytes_mb": 300, "destination": "partner.trusted"},
        {"id": "d", "bytes_mb": 400, "destination": "another-evil.example"},
    ]
    result = impl.solve(transfers, ["partner.trusted"], volume_threshold_mb=100)
    assert result == ["a", "d"]


def test_results_sorted():
    transfers = [
        {"id": "zeta", "bytes_mb": 200, "destination": "bad.example"},
        {"id": "alpha", "bytes_mb": 200, "destination": "bad.example"},
    ]
    assert impl.solve(transfers, [], volume_threshold_mb=100) == ["alpha", "zeta"]


# ---- hidden / edge cases -------------------------------------------------
def test_boundary_exactly_at_threshold_not_flagged():
    transfers = [{"id": "t4", "bytes_mb": 100, "destination": "unapproved.example"}]
    assert impl.solve(transfers, [], volume_threshold_mb=100) == []


def test_boundary_one_over_threshold_flagged():
    transfers = [{"id": "t5", "bytes_mb": 101, "destination": "unapproved.example"}]
    assert impl.solve(transfers, [], volume_threshold_mb=100) == ["t5"]


def test_empty_approved_list_means_everything_unapproved():
    transfers = [{"id": "t6", "bytes_mb": 999, "destination": "anywhere.example"}]
    assert impl.solve(transfers, [], volume_threshold_mb=100) == ["t6"]


def test_empty_transfers():
    assert impl.solve([], ["ok.example"], volume_threshold_mb=100) == []
