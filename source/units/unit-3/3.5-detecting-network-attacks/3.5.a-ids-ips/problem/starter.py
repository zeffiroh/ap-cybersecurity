"""Starter code for 3.5.a. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import List, Dict, Any


def solve(logs: List[Dict[str, Any]], rules: List[Dict[str, Any]]) -> List[str]:
    """Return sorted list of log-entry IDs whose dst_port and payload match at least one rule.

    Args:
        logs:  list of dicts with keys 'id' (str), 'dst_port' (int), 'payload' (str)
        rules: list of dicts with keys 'port' (int), 'keyword' (str)
    Returns:
        Sorted list of matching log entry IDs (de-duplicated).
    """
    # TODO: implement per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
