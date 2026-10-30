from typing import List, Dict, Any


THRESHOLD = 5
WINDOW_SECS = 59


def solve(logs: List[Dict[str, Any]]) -> List[str]:
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
    best = 0
    n = len(timestamps)
    right = 0
    for left in range(n):
        while right < n and timestamps[right] <= timestamps[left] + WINDOW_SECS:
            right += 1
        count = right - left
        if count > best:
            best = count
    return best
