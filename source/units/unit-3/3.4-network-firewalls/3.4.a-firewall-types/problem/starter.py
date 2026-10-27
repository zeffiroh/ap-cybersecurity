"""Starter code for 3.4.a. Student completes the TODO.
This file intentionally FAILS the tests until implemented.
"""
from typing import List, Dict, Any


def solve(rules: List[Dict[str, Any]], packets: List[Dict[str, Any]], mode: str) -> List[str]:
    """Classify each packet as 'allow' or 'drop' using the given rule set.

    Args:
        rules:   Ordered list of rule dicts (action, proto, dport).
        packets: List of packet dicts (src, dst, sport, dport, proto, flags).
        mode:    'stateless' or 'stateful'.

    Returns:
        List of 'allow' / 'drop' verdicts, one per packet.
    """
    # TODO: implement per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
