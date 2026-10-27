"""Starter code for 3.2.b. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import Dict, List


def classify_controls(scenarios: List[Dict]) -> List[str]:
    """Classify each scenario's control family by its 'mechanism' field.

    Args:
        scenarios: list of dicts with keys 'id' (str), 'description' (str),
                   'mechanism' (str: 'policy_document', 'training_program',
                   'access_review_process', 'software_or_hardware_enforcement',
                   'physical_barrier').
    Returns:
        List of classification strings, same length and order as `scenarios`, each one of
        "managerial", "technical", "physical".
        See prompt.md and interface.md for the exact rules.
    """
    # TODO: implement the classification rules per prompt.md
    raise NotImplementedError("implement classify_controls() — see prompt.md")
