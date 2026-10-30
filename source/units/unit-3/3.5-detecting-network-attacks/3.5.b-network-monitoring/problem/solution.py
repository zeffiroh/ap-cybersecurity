from typing import Dict, List


def solve(baseline: Dict, flows: List[Dict]) -> List[str]:
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
