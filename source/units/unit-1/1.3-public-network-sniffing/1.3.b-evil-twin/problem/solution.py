"""Reference solution for 1.3.b. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import List

# Security strength: higher index = stronger
_SEC_ORDER = ["OPEN", "WEP", "WPA", "WPA2", "WPA3"]


def _sec_rank(sec: str) -> int:
    try:
        return _SEC_ORDER.index(sec.upper())
    except ValueError:
        return -1


def solve(aps: List[dict]) -> List[str]:
    """Return a sorted, de-duplicated list of suspicious BSSIDs.

    Rule 1 — Duplicate SSID: SSID seen with >1 distinct BSSID -> flag all BSSIDs for it.
    Rule 2 — Security downgrade: SSID seen with multiple security levels ->
              flag any BSSID whose security is not the maximum for that SSID.
    """
    if not aps:
        return []

    # Group by SSID
    from collections import defaultdict
    ssid_entries = defaultdict(list)  # ssid -> list of (bssid, security)
    for ap in aps:
        ssid_entries[ap["ssid"]].append((ap["bssid"], ap["security"]))

    suspicious = set()

    for ssid, entries in ssid_entries.items():
        bssids = [e[0] for e in entries]
        secs = [e[1] for e in entries]

        # Rule 1: more than one BSSID for this SSID
        if len(set(bssids)) > 1:
            suspicious.update(bssids)

        # Rule 2: security downgrade — flag entries without max security
        ranks = [_sec_rank(s) for s in secs]
        max_rank = max(ranks)
        if len(set(ranks)) > 1:
            for bssid, rank in zip(bssids, ranks):
                if rank < max_rank:
                    suspicious.add(bssid)

    return sorted(suspicious)
