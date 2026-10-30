from typing import List, Tuple, Dict


def solve(vlan_map: Dict[str, int], flows: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    blocked = []
    for src, dst in flows:
        v_src = vlan_map[src]
        v_dst = vlan_map[dst]
        if v_src == v_dst:
            continue
        if v_src == 20 and v_dst == 30:
            continue
        blocked.append((src, dst))
    return blocked
