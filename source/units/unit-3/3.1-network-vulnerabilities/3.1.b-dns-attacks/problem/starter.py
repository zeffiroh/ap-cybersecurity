"""Starter code for 3.1.b. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import List, Dict


def solve(queries: List[Dict]) -> List[str]:
    """Classify each DNS query's resolver race outcome as WIN, POISON, or REJECT.

    Args:
        queries: list of dicts with keys 'qname' (str), 'tx_id' (int), 'port' (int),
                 'replies' (list of dicts with 'from', 'tx_id', 'port', 'qname', 'arrival').
    Returns:
        List of classification strings, same length and order as `queries`, each one of
        "WIN", "POISON", "REJECT".
        See prompt.md and interface.md for the exact rules.
    """
    # TODO: implement the classification rules per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
