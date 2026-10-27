"""Starter code for 5.1.d. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import Dict, List


def solve(report: Dict[str, object]) -> Dict[str, object]:
    """Score a data breach report's severity.

    Args:
        report: {"categories": list[str], "record_count": int, "days_to_detect": int}
    Returns:
        {"score": int, "label": str} where label is one of
        "low", "medium", "high", "critical" per the rubric in prompt.md.
    """
    # TODO: sum data-category points + scale points + detection-speed points,
    #       then map the total to a label per the thresholds in prompt.md.
    raise NotImplementedError("implement solve() — see prompt.md")
