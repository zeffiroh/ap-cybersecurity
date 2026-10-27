"""Starter code for 3.5.b. Student completes the TODO.
This file intentionally FAILS the tests until implemented.
"""
from typing import Dict, List


def solve(baseline: Dict, flows: List[Dict]) -> List[str]:
    """Flag hosts whose observed traffic deviates from their baseline profile.

    Args:
        baseline: host IP -> {"max_bytes": int, "allowed_ports": list[int]}
        flows:    list of {"host": str, "dst_port": int, "bytes": int}

    Returns:
        Sorted list of anomalous host IPs (no duplicates).
    """
    # TODO: implement per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
