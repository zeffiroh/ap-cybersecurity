"""Starter code for 5.6.c. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import List


def solve(indicators: List[str]) -> str:
    """Classify an evidence bundle into the attack category its indicators most strongly
    support (highest count of matching known indicators for that category).

    Args:
        indicators: list[str] of evidence tags collected during an investigation.
    Returns:
        str — the best-supported category name ("brute-force", "sql-injection", "malware",
        "phishing"), or "unknown" if no indicator matches any known category. Ties are broken
        by choosing the alphabetically first category among the tied leaders. See
        interface.md for the exact indicator-to-category mapping.
    """
    # TODO: implement per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
