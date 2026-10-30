from collections import defaultdict
from typing import List, Dict, Any


def solve(events: List[Dict[str, Any]]) -> List[str]:
    failures: Dict[str, List[int]] = defaultdict(list)
    for ev in events:
        if not ev.get("ok", True):
            failures[ev["user"]].append(ev["ts"])

    flagged = set()
    for user, timestamps in failures.items():
        timestamps.sort()
        for i in range(len(timestamps) - 4):
            if timestamps[i + 4] - timestamps[i] < 60:
                flagged.add(user)
                break

    return sorted(flagged)
