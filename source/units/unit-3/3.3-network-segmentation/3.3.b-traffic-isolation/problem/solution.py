from typing import List, Dict, Any


def solve(requests: List[Dict[str, Any]], policy: Dict[str, Any]) -> List[str]:
    allowed_ids = []
    allowed_roles = policy.get("allowed_roles", {})
    requires_internal = policy.get("requires_internal", [])
    requires_posture = policy.get("requires_posture", [])
    internal_prefixes = policy.get("internal_prefixes", [])

    for req in requests:
        rid = req["id"]
        res = req["resource"]
        role = req["role"]
        ip = req["ip"]
        posture = req.get("device_posture", {})

        if res not in allowed_roles:
            continue
        if role not in allowed_roles[res]:
            continue

        if res in requires_internal:
            ip_ok = False
            for prefix in internal_prefixes:
                if ip.startswith(prefix):
                    ip_ok = True
                    break
            if not ip_ok:
                continue

        if res in requires_posture:
            posture_ok = True
            for val in posture.values():
                if not val:
                    posture_ok = False
                    break
            if not posture_ok:
                continue

        allowed_ids.append(rid)

    return allowed_ids
