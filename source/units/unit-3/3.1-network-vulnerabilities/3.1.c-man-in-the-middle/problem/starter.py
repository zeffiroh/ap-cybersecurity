"""Starter code for 3.1.c. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import List, Dict


def solve(replies: List[Dict]) -> List[str]:
    """Flag IP addresses that show the ARP spoofing signature.

    Args:
        replies: list of dicts with keys 'ts' (int), 'ip' (str), 'mac' (str).
    Returns:
        Sorted list (no duplicates) of IP addresses where a later reply's MAC differs from
        the MAC of the earliest (by 'ts') reply for that IP.
        See prompt.md and interface.md for the exact rules.
    """
    # TODO: implement the detection rule per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
