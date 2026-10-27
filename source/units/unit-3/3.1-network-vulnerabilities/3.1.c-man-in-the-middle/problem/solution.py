"""Reference solution for 3.1.c. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import List, Dict


def solve(replies: List[Dict]) -> List[str]:
    """Flag IP addresses that show the ARP spoofing signature.

    Rule (see interface.md):
      1. The reply with the smallest 'ts' for a given IP establishes the trusted MAC binding.
      2. Any other reply for that IP with a DIFFERENT mac flags the IP as spoofed.
    """
    by_ip = {}
    for r in replies:
        by_ip.setdefault(r["ip"], []).append(r)

    flagged = set()
    for ip, rs in by_ip.items():
        trusted = min(rs, key=lambda r: r["ts"])
        for r in rs:
            if r["mac"] != trusted["mac"]:
                flagged.add(ip)
                break

    return sorted(flagged)
