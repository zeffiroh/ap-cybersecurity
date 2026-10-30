from typing import List, Dict, Any

MAX_WALK_SPEED = 2.0


def solve(records: List[Dict[str, Any]]) -> List[str]:
    flagged = set()
    last_time: Dict[str, int] = {}

    for rec in records:
        eid = rec["id"]
        badge = rec["badge"]
        t = rec["time"]
        dist = rec["distance_from_prev"]
        sensor = rec["sensor_count"]

        if badge is not None and dist is not None:
            if badge in last_time:
                elapsed = t - last_time[badge]
                if elapsed == 0 or dist / elapsed > MAX_WALK_SPEED:
                    flagged.add(eid)
            last_time[badge] = t
        elif badge is not None:
            last_time[badge] = t

        if badge is not None and sensor >= 2:
            flagged.add(eid)

    return sorted(flagged)
