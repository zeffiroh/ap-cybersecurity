"""Starter code for 3.5.c. Student completes the TODO.
This file intentionally FAILS the tests until implemented.
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
    # TODO: implement per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
