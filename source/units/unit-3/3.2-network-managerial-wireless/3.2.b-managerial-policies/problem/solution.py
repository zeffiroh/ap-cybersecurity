"""Reference solution for 3.2.b. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import Dict, List

_MANAGERIAL = {"policy_document", "training_program", "access_review_process"}
_TECHNICAL = {"software_or_hardware_enforcement"}
_PHYSICAL = {"physical_barrier"}


def classify_controls(scenarios: List[Dict]) -> List[str]:
    """Classify each scenario's control family by its 'mechanism' field.

    Rules (see interface.md):
      - policy_document / training_program / access_review_process -> managerial
      - software_or_hardware_enforcement -> technical
      - physical_barrier -> physical
    """
    result = []
    for s in scenarios:
        mech = s["mechanism"]
        if mech in _MANAGERIAL:
            result.append("managerial")
        elif mech in _TECHNICAL:
            result.append("technical")
        elif mech in _PHYSICAL:
            result.append("physical")
        else:
            raise ValueError(f"unknown mechanism: {mech}")
    return result
