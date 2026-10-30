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


def test_clear_brute_force():
    indicators = ["multiple_401_responses", "single_source_ip", "many_usernames_targeted"]
    assert impl.solve(indicators) == "brute-force"


def test_clear_sql_injection():
    indicators = ["sql_meta_characters_in_request", "database_error_in_response"]
    assert impl.solve(indicators) == "sql-injection"


def test_clear_malware():
    indicators = ["known_malware_file_hash", "outbound_c2_connection", "persistence_mechanism_installed"]
    assert impl.solve(indicators) == "malware"


def test_clear_phishing():
    indicators = ["suspicious_email_attachment", "credential_harvesting_url", "spoofed_sender_domain"]
    assert impl.solve(indicators) == "phishing"


def test_no_matching_indicators_unknown():
    indicators = ["server_restarted", "disk_space_low"]
    assert impl.solve(indicators) == "unknown"


def test_mixed_weak_signals_highest_score_wins():
    indicators = [
        "multiple_401_responses",
        "sql_meta_characters_in_request",
        "database_error_in_response",
        "union_select_pattern",
    ]
    assert impl.solve(indicators) == "sql-injection"


def test_tie_broken_alphabetically():
    indicators = ["multiple_401_responses", "known_malware_file_hash"]
    assert impl.solve(indicators) == "brute-force"


def test_empty_indicators_unknown():
    assert impl.solve([]) == "unknown"


def test_unrelated_indicators_ignored():
    indicators = ["unexpected_process_spawned", "server_restarted", "disk_space_low"]
    assert impl.solve(indicators) == "malware"


def test_duplicate_indicators_not_double_counted():
    indicators = ["multiple_401_responses", "multiple_401_responses", "known_malware_file_hash"]
    assert impl.solve(indicators) == "brute-force"
