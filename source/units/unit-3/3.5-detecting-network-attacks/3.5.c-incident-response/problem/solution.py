"""Reference solution for 3.5.c. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml).

Implements a stable sort of incident-response actions into NIST SP 800-61 phase order.
"""
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
    """Sort action records into canonical NIST IR phase order (stable within a phase).

    Args:
        actions: list of {"action": str, "phase": str} dicts, phase must be one of
                 the six canonical NIST SP 800-61 phase names.

    Returns:
        List of "action" strings, reordered by phase.

    Raises:
        ValueError: if any action's phase is not a canonical phase name.
    """
    for entry in actions:
        if entry["phase"] not in _PHASE_RANK:
            raise ValueError(f"Unknown IR phase: {entry['phase']!r}")

    # sorted() is stable, so entries with equal rank keep their original relative order.
    ordered = sorted(actions, key=lambda entry: _PHASE_RANK[entry["phase"]])
    return [entry["action"] for entry in ordered]
