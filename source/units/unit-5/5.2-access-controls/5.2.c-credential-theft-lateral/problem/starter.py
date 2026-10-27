"""Starter code for 5.2.c. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import Dict, List


def solve(events: List[Dict[str, object]], threshold: int, window_minutes: int) -> List[str]:
    """Flag accounts whose authentication events hit >= threshold distinct hosts
    within some rolling window of `window_minutes`.

    Args:
        events: list of {"account": str, "host": str, "ts": int}
        threshold: minimum distinct-host count within the window to flag an account
        window_minutes: size of the inclusive rolling window, in minutes
    Returns:
        sorted, de-duplicated list[str] of flagged account names.
    """
    # TODO: group events by account; for each account, for every event's ts as a
    #       candidate window start, count distinct hosts with ts in [start, start+window_minutes];
    #       flag the account if any window reaches `threshold`.
    raise NotImplementedError("implement solve() — see prompt.md")
