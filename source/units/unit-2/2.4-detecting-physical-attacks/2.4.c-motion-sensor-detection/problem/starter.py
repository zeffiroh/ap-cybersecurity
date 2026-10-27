"""Starter code for 2.4.c. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import Dict, List, Set


def solve(events: List[Dict], false_positive_causes: Set[str]) -> List[str]:
    """Return a sorted, de-duplicated list of event IDs that classify as TRUE_DETECTION.

    Args:
        events: list of dicts. Single-technology sensors (sensor_type in
            {"pir", "microwave", "ultrasonic"}) have a "cause" key. Dual-technology sensors
            (sensor_type == "dual-tech") have "cause_pir" and "cause_mw" keys instead.
        false_positive_causes: set of cause-tag strings known to be false-positive causes.
    Returns:
        Sorted list of event ID strings classified as TRUE_DETECTION.
        See prompt.md and interface.md for the exact classification rules.
    """
    # TODO: implement the single-tech rule and the dual-tech AND-logic rule per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
