"""Test suite for 1.5.b — the blackbox acceptance contract.
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
def test_eval_only():
    assert impl.solve("result = eval(user_input)") == ["vuln:eval"]


def test_os_system_and_shell_true():
    code = 'os.system("ls " + path)\nsubprocess.run(cmd, shell=True)'
    assert impl.solve(code) == ["vuln:os_system", "vuln:subprocess_shell"]


def test_md5_and_pickle():
    code = "import hashlib\nhashlib.md5(data)\npickle.loads(blob)"
    assert impl.solve(code) == ["vuln:md5", "vuln:pickle_loads"]


def test_clean_code():
    assert impl.solve("x = 1 + 2\nprint(x)") == []


# ---- hidden / edge cases -------------------------------------------------
def test_empty_string():
    assert impl.solve("") == []


def test_hardcoded_password_lowercase():
    assert impl.solve('password = "secret123"') == ["vuln:hardcoded_password"]


def test_hardcoded_password_mixed_case():
    assert impl.solve('Password = "abc"') == ["vuln:hardcoded_password"]


def test_hardcoded_password_uppercase():
    assert impl.solve('PASSWORD = "abc"') == ["vuln:hardcoded_password"]


def test_all_patterns():
    code = (
        "eval(x)\n"
        "os.system(cmd)\n"
        "subprocess.run(args, shell=True)\n"
        "hashlib.md5(data)\n"
        "pickle.loads(blob)\n"
        'password = "pw"\n'
    )
    assert impl.solve(code) == [
        "vuln:eval",
        "vuln:hardcoded_password",
        "vuln:md5",
        "vuln:os_system",
        "vuln:pickle_loads",
        "vuln:subprocess_shell",
    ]


def test_dedup():
    code = "eval(a)\neval(b)\neval(c)"
    result = impl.solve(code)
    assert result == sorted(set(result))
    assert result == ["vuln:eval"]


def test_sorted_output():
    code = "pickle.loads(x)\neval(y)"
    result = impl.solve(code)
    assert result == sorted(result)


def test_no_false_positive_md5_variable():
    # "md5_value" does not contain "md5(" so should not trigger
    assert impl.solve("md5_value = compute_hash()") == []


def test_shell_false_not_flagged():
    # shell=False is not dangerous — should not trigger
    assert impl.solve("subprocess.run(cmd, shell=False)") == []
