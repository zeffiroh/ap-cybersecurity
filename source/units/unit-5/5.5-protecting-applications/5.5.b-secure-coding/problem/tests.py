"""Test suite for 5.5.b — the blackbox acceptance contract.
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
def test_all_secure_no_violations():
    config = {
        "debug_mode": False,
        "db_query_style": "parameterized",
        "secrets_in_code": False,
        "error_verbosity": "generic",
        "dependencies_pinned": True,
        "runs_as": "app_user",
        "code_review_required": True,
    }
    assert impl.solve(config) == []


def test_debug_mode_flagged():
    config = {"debug_mode": True}
    assert impl.solve(config) == ["debug-mode-enabled"]


def test_concatenated_query_flagged():
    config = {"db_query_style": "concatenated"}
    assert impl.solve(config) == ["non-parameterized-query"]


def test_hardcoded_secret_flagged():
    config = {"secrets_in_code": True}
    assert impl.solve(config) == ["hardcoded-secret"]


def test_multiple_violations_sorted():
    config = {
        "debug_mode": True,
        "runs_as": "root",
        "secrets_in_code": True,
    }
    assert impl.solve(config) == ["debug-mode-enabled", "excessive-privilege", "hardcoded-secret"]


# ---- hidden / edge cases -------------------------------------------------
def test_verbose_errors_flagged():
    config = {"error_verbosity": "verbose"}
    assert impl.solve(config) == ["verbose-error-messages"]


def test_unpinned_dependencies_flagged():
    config = {"dependencies_pinned": False}
    assert impl.solve(config) == ["unpinned-dependencies"]


def test_no_code_review_flagged():
    config = {"code_review_required": False}
    assert impl.solve(config) == ["no-code-review"]


def test_missing_keys_treated_as_not_violating():
    assert impl.solve({}) == []


def test_all_violations_at_once():
    config = {
        "debug_mode": True,
        "db_query_style": "concatenated",
        "secrets_in_code": True,
        "error_verbosity": "verbose",
        "dependencies_pinned": False,
        "runs_as": "root",
        "code_review_required": False,
    }
    assert impl.solve(config) == [
        "debug-mode-enabled",
        "excessive-privilege",
        "hardcoded-secret",
        "no-code-review",
        "non-parameterized-query",
        "unpinned-dependencies",
        "verbose-error-messages",
    ]
