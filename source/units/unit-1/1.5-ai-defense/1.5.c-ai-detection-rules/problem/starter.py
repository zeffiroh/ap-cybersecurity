"""Starter code for 1.5.c. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import List, Dict, Any


def solve(logs: List[Dict[str, Any]]) -> List[str]:
    """Generate detection-rule strings for IPs that exceed the brute-force threshold.

    Args:
        logs: list of dicts with keys ts (int), src (str), event (str), ok (bool).
              Only 'login_fail' events count toward the brute-force rule.
    Returns:
        Sorted list of rule strings of the form:
        'ALERT brute_force src=<IP> count=<N> window=60s'
        One entry per IP that has >= 5 login_fail events within any 60-second window.
    """
    # TODO: implement per prompt.md
    raise NotImplementedError("implement solve() -- see prompt.md")
