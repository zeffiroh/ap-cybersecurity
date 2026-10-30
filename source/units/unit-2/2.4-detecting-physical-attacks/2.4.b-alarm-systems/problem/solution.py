from typing import List, Dict


def solve(events: List[Dict], exit_delay_sec: int = 45, verify_window_sec: int = 120) -> List[str]:
    n = len(events)
    base = [None] * n

    for i, e in enumerate(events):
        if e["sensor"] == "panic":
            base[i] = "PANIC"
        elif e["arm_state"] == "DISARMED":
            base[i] = "SUPPRESSED"
        elif e["since_armed_sec"] < exit_delay_sec:
            base[i] = "FALSE_ALARM"
        else:
            base[i] = "REAL"

    real_indices = [i for i in range(n) if base[i] == "REAL"]

    result = [""] * n
    for i, e in enumerate(events):
        if base[i] == "PANIC":
            result[i] = "DISPATCH"
        elif base[i] == "SUPPRESSED":
            result[i] = "SUPPRESSED"
        elif base[i] == "FALSE_ALARM":
            result[i] = "FALSE_ALARM"
        else:
            corroborated = False
            for j in real_indices:
                if j == i:
                    continue
                if events[j]["zone"] == e["zone"]:
                    continue
                if abs(events[j]["ts"] - e["ts"]) <= verify_window_sec:
                    corroborated = True
                    break
            result[i] = "DISPATCH" if corroborated else "LOCAL_ONLY"

    return result
