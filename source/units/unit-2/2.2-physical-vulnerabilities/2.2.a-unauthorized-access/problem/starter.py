"""Starter code for 2.2.a. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import List, Dict, Any

MAX_WALK_SPEED = 2.0  # meters per second


def solve(records: List[Dict[str, Any]]) -> List[str]:
    """Return sorted list of event IDs that indicate unauthorized physical access.

    Two detection rules (see prompt.md and interface.md):
      Rule 1 — Impossible speed: a badge appears at a second door faster than
               MAX_WALK_SPEED (2.0 m/s) allows given the distance.
      Rule 2 — Sensor mismatch: sensor_count >= 2 with a single badge swipe.

    Args:
        records: list of dicts with keys id, time, badge, door,
                 distance_from_prev, sensor_count (chronological order).
    Returns:
        Sorted, de-duplicated list of flagged event IDs.
    """
    # TODO: implement both detection rules and return sorted flagged IDs.
    raise NotImplementedError("implement solve() — see prompt.md")
