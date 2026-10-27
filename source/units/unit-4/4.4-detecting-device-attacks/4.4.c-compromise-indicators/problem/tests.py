"""Test suite for 4.4.c — the blackbox acceptance contract.
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
def test_example_1_compromised():
    assert impl.solve(["av_disabled", "new_admin_account"]) == "compromised"


def test_example_2_clean():
    assert impl.solve(["failed_login_cluster"]) == "clean"


def test_example_3_suspicious():
    assert impl.solve(["new_admin_account", "failed_login_cluster"]) == "suspicious"


# ---- hidden / edge cases -------------------------------------------------
def test_edge_empty_list_is_clean():
    assert impl.solve([]) == "clean"


def test_unknown_ioc_contributes_zero():
    assert impl.solve(["unrecognized_ioc_type"]) == "clean"


def test_duplicate_iocs_not_double_counted():
    # av_disabled alone = 5 (suspicious). If duplicated and double-counted it would
    # wrongly become 10 (compromised).
    assert impl.solve(["av_disabled", "av_disabled", "av_disabled"]) == "suspicious"


def test_boundary_score_exactly_four_is_suspicious():
    assert impl.solve(["new_admin_account"]) == "suspicious"


def test_boundary_score_just_below_four_is_clean():
    assert impl.solve(["unusual_outbound_traffic"]) == "clean"


def test_boundary_score_exactly_eight_is_compromised():
    assert impl.solve(["av_disabled", "unusual_outbound_traffic"]) == "compromised"


def test_boundary_score_seven_is_suspicious():
    assert impl.solve(["unusual_outbound_traffic", "unexpected_scheduled_task",
                        "failed_login_cluster"]) == "suspicious"


def test_high_severity_combination_is_compromised():
    assert impl.solve(["known_malicious_hash", "unusual_outbound_traffic",
                        "registry_run_key_added"]) == "compromised"


def test_all_iocs_combined_is_compromised():
    all_iocs = ["known_malicious_hash", "av_disabled", "new_admin_account",
                "unusual_outbound_traffic", "unexpected_scheduled_task",
                "registry_run_key_added", "failed_login_cluster"]
    assert impl.solve(all_iocs) == "compromised"
