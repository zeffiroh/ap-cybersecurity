from typing import List

_SEC_ORDER = ["OPEN", "WEP", "WPA", "WPA2", "WPA3"]


def _sec_rank(sec: str) -> int:
    try:
        return _SEC_ORDER.index(sec.upper())
    except ValueError:
        return -1


def solve(aps: List[dict]) -> List[str]:
    if not aps:
        return []

    from collections import defaultdict
    ssid_entries = defaultdict(list)
    for ap in aps:
        ssid_entries[ap["ssid"]].append((ap["bssid"], ap["security"]))

    suspicious = set()

    for ssid, entries in ssid_entries.items():
        bssids = [e[0] for e in entries]
        secs = [e[1] for e in entries]

        if len(set(bssids)) > 1:
            suspicious.update(bssids)

        ranks = [_sec_rank(s) for s in secs]
        max_rank = max(ranks)
        if len(set(ranks)) > 1:
            for bssid, rank in zip(bssids, ranks):
                if rank < max_rank:
                    suspicious.add(bssid)

    return sorted(suspicious)
