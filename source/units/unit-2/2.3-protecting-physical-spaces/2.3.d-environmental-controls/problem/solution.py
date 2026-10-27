"""Reference solution for 2.3.d. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import List, Dict, Any


def solve(zones: List[Dict[str, Any]], policy: Dict[str, Dict[str, Any]]) -> List[str]:
    """Return sorted list of zone names that are non-compliant with their room type's policy.

    A zone is non-compliant if it fails any applicable requirement key present in the
    policy entry for its room_type:
      - require_ups (bool): zone.has_ups must be True
      - min_hvac_redundancy (int): zone.hvac_redundancy must be >= this value
      - allowed_suppression (list[str]): zone.suppression must be in this list
      - require_leak_sensor (bool): zone.has_leak_sensor must be True
    A room_type absent from policy has no requirements (always compliant).
    """
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
