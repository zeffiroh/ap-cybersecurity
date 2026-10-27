"""Starter code for 1.2.a. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import List, Dict, Any


def solve(events: List[Dict[str, Any]]) -> List[str]:
    """Return sorted, de-duplicated usernames with >=5 failed logins in any 60s window.

    Args:
        events: list of dicts, each with keys:
                  ts   (int)  - Unix timestamp in seconds
                  user (str)  - username targeted
                  ok   (bool) - True=success, False=failure
    Returns:
        Sorted list of usernames flagged as brute-force targets.
        See prompt.md and interface.md for the exact detection rule.
    """
    # TODO: for each user, collect failure timestamps, sort them, then use a
    #       sliding window of size 5 to check if ts[i+4] - ts[i] < 60.
    #       Return a sorted list of flagged usernames.
    raise NotImplementedError("implement solve() — see prompt.md")
