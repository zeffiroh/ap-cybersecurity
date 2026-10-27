"""Reference solution for 2.4.c. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import Dict, List, Set


def solve(events: List[Dict], false_positive_causes: Set[str]) -> List[str]:
    """Return sorted list of event IDs that classify as TRUE_DETECTION.

    Single-technology sensors (pir, microwave, ultrasonic): TRUE_DETECTION iff "cause" is
    NOT in false_positive_causes.

    Dual-technology sensors (dual-tech): AND-logic. TRUE_DETECTION iff BOTH "cause_pir" and
    "cause_mw" are NOT in false_positive_causes. Either element reporting a known
    false-positive cause makes the whole event a FALSE_POSITIVE.
    """
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
