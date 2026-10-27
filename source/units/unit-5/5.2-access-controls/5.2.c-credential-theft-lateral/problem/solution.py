"""Reference solution for 5.2.c. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from collections import defaultdict
from typing import Dict, List


def solve(events: List[Dict[str, object]], threshold: int, window_minutes: int) -> List[str]:
    """Flag accounts whose authentication events hit >= threshold distinct hosts
    within some rolling window of `window_minutes`."""
    by_account: Dict[str, List[Dict[str, object]]] = defaultdict(list)
    for ev in events:
        by_account[ev["account"]].append(ev)

    flagged = set()
    for account, evs in by_account.items():
        starts = sorted(set(e["ts"] for e in evs))
        for start in starts:
            window_hosts = set(
                e["host"] for e in evs if start <= e["ts"] <= start + window_minutes
            )
            if len(window_hosts) >= threshold:
                flagged.add(account)
                break

    return sorted(flagged)
