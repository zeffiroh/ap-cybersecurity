from typing import Dict, List

PHASE_ORDER = [
    "Preparation",
    "Identification",
    "Containment",
    "Eradication",
    "Recovery",
    "Lessons Learned",
]
_PHASE_RANK = {name: i for i, name in enumerate(PHASE_ORDER)}


def solve(actions: List[Dict]) -> List[str]:
    for entry in actions:
        if entry["phase"] not in _PHASE_RANK:
            raise ValueError(f"Unknown IR phase: {entry['phase']!r}")

    ordered = sorted(actions, key=lambda entry: _PHASE_RANK[entry["phase"]])
    return [entry["action"] for entry in ordered]
