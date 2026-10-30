from typing import List, Set, FrozenSet, Dict
import datetime


def solve(entries: List[Dict], far_pairs: Set[FrozenSet]) -> List[str]:
    flagged = set()

    by_badge: Dict[str, List[Dict]] = {}
    for e in entries:
        by_badge.setdefault(e["badge"], []).append(e)

    after_hours = {22, 23, 0, 1, 2, 3, 4, 5}

    for badge, evts in by_badge.items():
        evts_sorted = sorted(evts, key=lambda x: x["ts"])

        denials = [e["ts"] for e in evts_sorted if e["outcome"] == "DENIED"]
        for i in range(len(denials)):
            window_end = denials[i] + 60
            count = sum(1 for ts in denials[i:] if ts <= window_end)
            if count >= 5:
                flagged.add(badge)
                break

        for e in evts_sorted:
            if e["outcome"] == "GRANTED" and e["door"].startswith("restricted-"):
                hour = datetime.datetime.utcfromtimestamp(e["ts"]).hour
                if hour in after_hours:
                    flagged.add(badge)
                    break

        granted = [e for e in evts_sorted if e["outcome"] == "GRANTED"]
        for i in range(len(granted) - 1):
            a, b = granted[i], granted[i + 1]
            if a["door"] != b["door"] and (b["ts"] - a["ts"]) <= 600:
                pair = frozenset({a["door"], b["door"]})
                if pair in far_pairs:
                    flagged.add(badge)
                    break

    return sorted(flagged)
