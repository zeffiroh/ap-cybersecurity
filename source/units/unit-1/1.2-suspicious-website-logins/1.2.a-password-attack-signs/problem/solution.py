"""Reference solution for 1.2.a. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from collections import defaultdict
from typing import List, Dict, Any


def solve(events: List[Dict[str, Any]]) -> List[str]:
    """Return sorted, de-duplicated usernames with >=5 failed logins in any 60s window."""
    # Group failure timestamps by user
    failures: Dict[str, List[int]] = defaultdict(list)
    for ev in events:
        if not ev.get("ok", True):
            failures[ev["user"]].append(ev["ts"])

    flagged = set()
    for user, timestamps in failures.items():
        timestamps.sort()
        # Sliding window of size 5: if ts[i+4] - ts[i] < 60, threshold met
        for i in range(len(timestamps) - 4):
            if timestamps[i + 4] - timestamps[i] < 60:
                flagged.add(user)
                break  # Already flagged; stop early

    return sorted(flagged)
