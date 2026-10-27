"""Starter code for 1.1.c. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import List


def solve(message: dict) -> List[str]:
    """Return sorted, de-duplicated phishing indicator labels for `message`.

    Args:
        message: dict with keys channel, sender, text, link (all strings).
    Returns:
        Sorted list of triggered indicator label strings (may be empty).
        Labels: "lookalike-domain", "urgent-money-request", "credential-request",
                "mismatched-sender", "shortened-link".
        See prompt.md and interface.md for the precise detection rules.
    """
    # TODO: check each indicator rule against message["sender"], message["text"],
    #       and message["link"] (all case-insensitive), collect triggered labels,
    #       and return them sorted and de-duplicated.
    raise NotImplementedError("implement solve() — see prompt.md")
