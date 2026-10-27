"""Starter code for 3.4.b. Student completes the TODO.
This file intentionally FAILS the tests until implemented.
"""
from typing import List, Dict


def solve(rules: List[Dict], packets: List[Dict]) -> List[str]:
    """Evaluate each packet against the ACL using first-match-wins logic.

    Args:
        rules:   Ordered list of ACL rule dicts (action, src, dst, port, proto).
        packets: List of packet dicts (src, dst, port, proto).

    Returns:
        List of 'allow' / 'deny' verdicts, one per packet, in order.
    """
    # TODO: implement per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
