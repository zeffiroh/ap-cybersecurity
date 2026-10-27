"""Reference solution for 3.3.a. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml).
"""
from typing import List, Tuple, Dict


def solve(vlan_map: Dict[str, int], flows: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """Determine which traffic flows are blocked by VLAN segmentation rules.

    Args:
        vlan_map: dict mapping host name to its VLAN ID.
        flows: list of tuples (src_host, dst_host).

    Returns:
        List of blocked flows in the same order.
    """
    blocked = []
    for src, dst in flows:
        v_src = vlan_map[src]
        v_dst = vlan_map[dst]
        # Rule 1: Same VLAN is allowed
        if v_src == v_dst:
            continue
        # Rule 2: VLAN 20 (Employee) to VLAN 30 (Server) is allowed
        if v_src == 20 and v_dst == 30:
            continue
        # Otherwise blocked
        blocked.append((src, dst))
    return blocked
