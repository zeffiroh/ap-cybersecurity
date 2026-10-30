from typing import Dict, List, Set


def solve(events: List[Dict], false_positive_causes: Set[str]) -> List[str]:
    true_detections = []

    for e in events:
        sensor_type = e["sensor_type"]

        if sensor_type == "dual-tech":
            pir_ok = e["cause_pir"] not in false_positive_causes
            mw_ok = e["cause_mw"] not in false_positive_causes
            is_true = pir_ok and mw_ok
        else:
            is_true = e["cause"] not in false_positive_causes

        if is_true:
            true_detections.append(e["id"])

    return sorted(set(true_detections))
