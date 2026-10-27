"""Reference solution for 3.5.a. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import List, Dict, Any


def solve(logs: List[Dict[str, Any]], rules: List[Dict[str, Any]]) -> List[str]:
    """Return sorted list of log entry IDs that match at least one IDS signature rule.

    A log entry matches a rule when its dst_port equals the rule's port AND
    the rule's keyword appears (case-insensitive) in the entry's payload.
    """
    matched = set()
    for entry in logs:
        port = entry["dst_port"]
        payload_lower = entry["payload"].lower()
        for rule in rules:
            if rule["port"] == port and rule["keyword"].lower() in payload_lower:
                matched.add(entry["id"])
                break  # one match is enough; avoid duplicates
    return sorted(matched)
