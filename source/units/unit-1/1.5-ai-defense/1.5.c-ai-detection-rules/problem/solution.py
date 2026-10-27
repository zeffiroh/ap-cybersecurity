"""Reference solution for 1.5.c. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml).

solve(logs) -> sorted list of detection-rule strings.
Rule fires when an IP has >= 5 login_fail events within any 60-second window.
Rule string format: 'ALERT brute_force src=<IP> count=<N> window=60s'
"""
from typing import List, Dict, Any


THRESHOLD = 5
WINDOW_SECS = 59  # inclusive: events[i].ts + 59 covers a 60-second span


def solve(logs: List[Dict[str, Any]]) -> List[str]:
    """Return sorted detection-rule strings for IPs exceeding the brute-force threshold."""
    # Group login_fail timestamps by source IP
    failures: Dict[str, List[int]] = {}
    for entry in logs:
        if entry.get("event") == "login_fail":
            src = entry["src"]
            failures.setdefault(src, []).append(entry["ts"])

    rules = []
    for src, timestamps in failures.items():
        timestamps.sort()
        max_window = _max_window_count(timestamps)
        if max_window >= THRESHOLD:
            rules.append(f"ALERT brute_force src={src} count={max_window} window=60s")

    return sorted(rules)


def _max_window_count(timestamps: List[int]) -> int:
    """Return the maximum number of events within any 60-second window (sliding window)."""
    best = 0
    n = len(timestamps)
    right = 0
    for left in range(n):
        # advance right while timestamps[right] <= timestamps[left] + WINDOW_SECS
        while right < n and timestamps[right] <= timestamps[left] + WINDOW_SECS:
            right += 1
        count = right - left
        if count > best:
            best = count
    return best
