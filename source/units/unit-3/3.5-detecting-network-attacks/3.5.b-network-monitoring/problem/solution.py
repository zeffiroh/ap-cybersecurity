"""Reference solution for 3.5.b. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml).

Implements a simplified per-host traffic-anomaly detector: flags hosts exceeding a baseline
byte-volume threshold or using a destination port outside the baseline's allowed set.
"""
from typing import Dict, List


def solve(baseline: Dict, flows: List[Dict]) -> List[str]:
    """Flag hosts whose observed traffic deviates from their baseline profile.

    Args:
        baseline: host IP -> {"max_bytes": int, "allowed_ports": list[int]}
        flows:    list of {"host": str, "dst_port": int, "bytes": int}

    Returns:
        Sorted list of anomalous host IPs (no duplicates).
    """
    totals: Dict[str, int] = {}
    port_violation: Dict[str, bool] = {}
    unknown_hosts = set()

    for flow in flows:
        host = flow["host"]
        if host not in baseline:
            unknown_hosts.add(host)
            continue
        totals[host] = totals.get(host, 0) + flow["bytes"]
        allowed_ports = baseline[host]["allowed_ports"]
        if flow["dst_port"] not in allowed_ports:
            port_violation[host] = True

    flagged = set(unknown_hosts)
    for host, total in totals.items():
        if total > baseline[host]["max_bytes"]:
            flagged.add(host)
    for host in port_violation:
        flagged.add(host)

    return sorted(flagged)
