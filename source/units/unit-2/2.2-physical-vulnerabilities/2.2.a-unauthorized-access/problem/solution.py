"""Reference solution for 2.2.a. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import List, Dict, Any

MAX_WALK_SPEED = 2.0  # meters per second


def solve(records: List[Dict[str, Any]]) -> List[str]:
    """Return sorted list of event IDs that indicate unauthorized physical access.

    Rule 1 — Impossible speed: badge appears at a new door faster than MAX_WALK_SPEED.
    Rule 2 — Sensor mismatch: sensor_count >= 2 with a single badge swipe.
    """
    flagged = set()
    # Track last seen time per badge for Rule 1
    last_time: Dict[str, int] = {}

    for rec in records:
        eid = rec["id"]
        badge = rec["badge"]
        t = rec["time"]
        dist = rec["distance_from_prev"]
        sensor = rec["sensor_count"]

        # Rule 1: impossible speed
        if badge is not None and dist is not None:
            if badge in last_time:
                elapsed = t - last_time[badge]
                if elapsed == 0 or dist / elapsed > MAX_WALK_SPEED:
                    flagged.add(eid)
            last_time[badge] = t
        elif badge is not None:
            last_time[badge] = t

        # Rule 2: sensor mismatch (two or more bodies, only one badge)
        if badge is not None and sensor >= 2:
            flagged.add(eid)

    return sorted(flagged)
