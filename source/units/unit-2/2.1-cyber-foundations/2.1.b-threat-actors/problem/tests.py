"""Test suite for 2.1.b — the blackbox acceptance contract."""
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

def test_basic_script_kiddie():
    logs = [{"id": "A", "log": "Detected automated scan on port 21. FTP exploit attempt."}]
    res = impl.solve(logs)
    assert res == {"A": "Script Kiddie"}

def test_basic_cybercriminal():
    logs = [{"id": "B", "log": "Ransomware locked user database. Send payment to local address."}]
    res = impl.solve(logs)
    assert res == {"B": "Cybercriminal"}

def test_basic_hacktivist():
    logs = [{"id": "C", "log": "Main landing page was defaced in protest of policy."}]
    res = impl.solve(logs)
    assert res == {"C": "Hacktivist"}

def test_basic_insider():
    logs = [{"id": "D", "log": "Disgruntled employee suspected of downloading sensitive files."}]
    res = impl.solve(logs)
    assert res == {"D": "Insider Threat"}

def test_basic_nation_state():
    logs = [{"id": "E", "log": "Quiet rootkit installation detected using zero-day exploit."}]
    res = impl.solve(logs)
    assert res == {"E": "Nation-State / APT"}

def test_priority_conflict():
    # Matches Nation-state (zero-day) and Script kiddie (port scan) -> priority Nation-state
    logs = [{"id": "F", "log": "Zero-day exploit was deployed during a noisy port scan."}]
    res = impl.solve(logs)
    assert res == {"F": "Nation-State / APT"}
    
    # Matches Cybercriminal (ransomware) and Hacktivist (protest) -> priority Cybercriminal
    logs = [{"id": "G", "log": "Ransomware deployed during political protest."}]
    res = impl.solve(logs)
    assert res == {"G": "Cybercriminal"}

def test_unknown_log():
    logs = [{"id": "H", "log": "Normal login attempt succeeded."}]
    res = impl.solve(logs)
    assert res == {"H": "Unknown"}

def test_case_insensitive():
    logs = [{"id": "I", "log": "EXFILTRATION OF HR DATABASE TO EXTERNAL IP ADDRESS"}]
    res = impl.solve(logs)
    assert res == {"I": "Nation-State / APT"}

def test_empty_logs():
    assert impl.solve([]) == {}

def test_multiple_logs():
    logs = [
        {"id": "1", "log": "Zero-day rootkit staged."},
        {"id": "2", "log": "A disgruntled worker exit interview logged."},
        {"id": "3", "log": "Anonymous post criticizing company on public forum defaced website."}
    ]
    res = impl.solve(logs)
    assert res == {
        "1": "Nation-State / APT",
        "2": "Insider Threat",
        "3": "Hacktivist"
    }
