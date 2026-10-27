"""Reference solution for 2.4.a. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import List, Set, FrozenSet, Dict
import datetime


def solve(entries: List[Dict], far_pairs: Set[FrozenSet]) -> List[str]:
    """Return sorted list of badge IDs that triggered one or more alert rules.

    Rule 0: >=5 DENIED events for same badge within any 60-second window.
    Rule 1: GRANTED at a 'restricted-' door during UTC hour in {22,23,0,1,2,3,4,5}.
    Rule 2: same badge GRANTED at two far-apart doors within 600 seconds.
    """
    flagged = set()

    # Group entries by badge
    by_badge: Dict[str, List[Dict]] = {}
    for e in entries:
        by_badge.setdefault(e["badge"], []).append(e)

    after_hours = {22, 23, 0, 1, 2, 3, 4, 5}

    for badge, evts in by_badge.items():
        evts_sorted = sorted(evts, key=lambda x: x["ts"])

        # Rule 0: repeated denial burst (>= 5 DENIED in 60s sliding window)
        denials = [e["ts"] for e in evts_sorted if e["outcome"] == "DENIED"]
        for i in range(len(denials)):
            window_end = denials[i] + 60
            count = sum(1 for ts in denials[i:] if ts <= window_end)
            if count >= 5:
                flagged.add(badge)
                break

        # Rule 1: after-hours restricted access (GRANTED at restricted- door, UTC hour in set)
        for e in evts_sorted:
            if e["outcome"] == "GRANTED" and e["door"].startswith("restricted-"):
                hour = datetime.datetime.utcfromtimestamp(e["ts"]).hour
                if hour in after_hours:
                    flagged.add(badge)
                    break

        # Rule 2: location inconsistency (GRANTED at two far doors within 600s)
        granted = [e for e in evts_sorted if e["outcome"] == "GRANTED"]
        for i in range(len(granted) - 1):
            a, b = granted[i], granted[i + 1]
            if a["door"] != b["door"] and (b["ts"] - a["ts"]) <= 600:
                pair = frozenset({a["door"], b["door"]})
                if pair in far_pairs:
                    flagged.add(badge)
                    break

    return sorted(flagged)
