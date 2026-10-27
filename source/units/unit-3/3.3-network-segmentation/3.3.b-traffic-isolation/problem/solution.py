"""Reference solution for 3.3.b. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml).
"""
from typing import List, Dict, Any


def solve(requests: List[Dict[str, Any]], policy: Dict[str, Any]) -> List[str]:
    """Evaluate Zero Trust connection requests against access policy rules.

    Args:
        requests: list of request dictionaries.
        policy: policy dictionary.

    Returns:
        List of request IDs that are allowed.
    """
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

        # Rule 1: Role Authorization
        if res not in allowed_roles:
            continue
        if role not in allowed_roles[res]:
            continue

        # Rule 2: Network Isolation (Implicit trust is not granted, must verify prefix)
        if res in requires_internal:
            ip_ok = False
            for prefix in internal_prefixes:
                if ip.startswith(prefix):
                    ip_ok = True
                    break
            if not ip_ok:
                continue

        # Rule 3: Posture Check
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
