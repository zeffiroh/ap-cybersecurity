"""Starter code for 1.5.d. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import List, Dict, Any


def solve(incidents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute MTTR and auto-resolved count for a list of SOC incidents.

    Args:
        incidents: list of dicts with keys:
            id (str), detected_at (int), resolved_at (int),
            severity (str), auto (bool).
    Returns:
        {"mttr": float, "auto_resolved": int}
        mttr = mean(resolved_at - detected_at) across all incidents.
        auto_resolved = count of incidents where auto is True.
        Return {"mttr": 0.0, "auto_resolved": 0} for empty input.
    """
    # TODO: implement per prompt.md
    raise NotImplementedError("implement solve() -- see prompt.md")
