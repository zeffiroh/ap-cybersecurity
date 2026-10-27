"""Reference solution for 5.6.a. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from collections import defaultdict
from typing import Dict, List


def solve(entries: List[Dict[str, object]], threshold: int, window_seconds: int) -> List[str]:
    """Flag source IPs whose failed-login count reaches >= threshold within some rolling
    window of window_seconds, per the SIEM brute-force rule described in the lesson."""
    by_ip: Dict[str, List[int]] = defaultdict(list)
    for e in entries:
        if e.get("status") == 401:
            by_ip[e["ip"]].append(e["ts"])

    flagged = set()
    for ip, times in by_ip.items():
        times = sorted(times)
        for start in times:
            count = sum(1 for t in times if start <= t <= start + window_seconds)
            if count >= threshold:
                flagged.add(ip)
                break

    return sorted(flagged)
