"""Reference solution for 5.6.c. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import List

# Known indicators per attack category (case-insensitive exact match against evidence tags).
_CATEGORY_INDICATORS = {
    "brute-force": {
        "multiple_401_responses",
        "single_source_ip",
        "many_usernames_targeted",
        "credential_guessing_pattern",
    },
    "sql-injection": {
        "sql_meta_characters_in_request",
        "database_error_in_response",
        "union_select_pattern",
        "unexpected_query_result_size",
    },
    "malware": {
        "known_malware_file_hash",
        "unexpected_process_spawned",
        "outbound_c2_connection",
        "persistence_mechanism_installed",
    },
    "phishing": {
        "suspicious_email_attachment",
        "credential_harvesting_url",
        "spoofed_sender_domain",
        "user_reported_suspicious_email",
    },
}


def solve(indicators: List[str]) -> str:
    """Classify an evidence bundle by scoring each category's matching indicator count.

    Returns the category name with the highest score. Ties are broken by choosing the
    alphabetically first category among the tied leaders. If no indicator matches any
    known category, returns "unknown".
    """
    evidence = set(indicators)
    scores = {
        category: len(evidence & known_indicators)
        for category, known_indicators in _CATEGORY_INDICATORS.items()
    }
    best_score = max(scores.values())
    if best_score == 0:
        return "unknown"
    winners = sorted(cat for cat, score in scores.items() if score == best_score)
    return winners[0]
