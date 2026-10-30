from typing import Dict, List

_MANAGERIAL = {"policy_document", "training_program", "access_review_process"}
_TECHNICAL = {"software_or_hardware_enforcement"}
_PHYSICAL = {"physical_barrier"}


def classify_controls(scenarios: List[Dict]) -> List[str]:
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
