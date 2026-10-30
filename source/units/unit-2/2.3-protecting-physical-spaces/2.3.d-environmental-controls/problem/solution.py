from typing import List, Dict, Any


def solve(zones: List[Dict[str, Any]], policy: Dict[str, Dict[str, Any]]) -> List[str]:
    non_compliant = set()

    for zone in zones:
        rules = policy.get(zone["room_type"])
        if not rules:
            continue

        if rules.get("require_ups") and not zone.get("has_ups", False):
            non_compliant.add(zone["name"])
            continue

        min_hvac = rules.get("min_hvac_redundancy")
        if min_hvac is not None and zone.get("hvac_redundancy", 0) < min_hvac:
            non_compliant.add(zone["name"])
            continue

        allowed = rules.get("allowed_suppression")
        if allowed is not None and zone.get("suppression", "none") not in allowed:
            non_compliant.add(zone["name"])
            continue

        if rules.get("require_leak_sensor") and not zone.get("has_leak_sensor", False):
            non_compliant.add(zone["name"])
            continue

    return sorted(non_compliant)
