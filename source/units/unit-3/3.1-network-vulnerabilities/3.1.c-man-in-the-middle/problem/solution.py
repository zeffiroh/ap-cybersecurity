from typing import List, Dict


def solve(replies: List[Dict]) -> List[str]:
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
