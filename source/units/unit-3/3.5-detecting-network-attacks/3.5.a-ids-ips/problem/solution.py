from typing import List, Dict, Any


def solve(logs: List[Dict[str, Any]], rules: List[Dict[str, Any]]) -> List[str]:
    matched = set()
    for entry in logs:
        port = entry["dst_port"]
        payload_lower = entry["payload"].lower()
        for rule in rules:
            if rule["port"] == port and rule["keyword"].lower() in payload_lower:
                matched.add(entry["id"])
                break
    return sorted(matched)
