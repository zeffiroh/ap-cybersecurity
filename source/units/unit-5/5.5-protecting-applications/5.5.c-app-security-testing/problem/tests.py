"""Test suite for 5.5.c — the blackbox acceptance contract.
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
def test_mixed_findings():
    lines = [
        'query = "SELECT * FROM users WHERE name = \'" + user_input + "\'"',
        'password = "hunter2"',
        'eval(user_expr)',
    ]
    assert impl.solve(lines) == [
        {"line": 1, "category": "sql-injection-risk"},
        {"line": 2, "category": "hardcoded-secret"},
        {"line": 3, "category": "eval-use"},
    ]


def test_safe_lines_no_findings():
    lines = ['password = os.environ["DB_PASSWORD"]', 'db.query(stmt, params)']
    assert impl.solve(lines) == []


def test_clean_code_no_findings():
    lines = ["def add(a, b):", "    return a + b", "", "result = add(1, 2)"]
    assert impl.solve(lines) == []


def test_parameterized_sql_not_flagged():
    lines = ['cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))']
    assert impl.solve(lines) == []


def test_exec_flagged_same_as_eval():
    lines = ["exec(payload)"]
    assert impl.solve(lines) == [{"line": 1, "category": "eval-use"}]


# ---- hidden / edge cases -------------------------------------------------
def test_multiple_categories_same_line():
    lines = ['token = "abc123"; eval(token)']
    result = impl.solve(lines)
    assert result == [
        {"line": 1, "category": "eval-use"},
        {"line": 1, "category": "hardcoded-secret"},
    ]


def test_case_insensitive_secret_keyword_and_sql():
    lines = ['API_KEY = "sk_live_xyz"', 'q = "select * from t where x=" + v']
    assert impl.solve(lines) == [
        {"line": 1, "category": "hardcoded-secret"},
        {"line": 2, "category": "sql-injection-risk"},
    ]


def test_fstring_sql_flagged():
    lines = ['q = f"SELECT * FROM t WHERE id={uid}"']
    assert impl.solve(lines) == [{"line": 1, "category": "sql-injection-risk"}]


def test_empty_input():
    assert impl.solve([]) == []
