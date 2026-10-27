"""Reference solution for 2.4.b. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import List, Dict


def solve(events: List[Dict], exit_delay_sec: int = 45, verify_window_sec: int = 120) -> List[str]:
    """Classify each alarm event as SUPPRESSED, FALSE_ALARM, LOCAL_ONLY, or DISPATCH.

    Rules (see interface.md):
      1. sensor == "panic"          -> DISPATCH (always, overrides everything else)
      2. arm_state == "DISARMED"    -> SUPPRESSED
      3. since_armed_sec < exit_delay_sec -> FALSE_ALARM
      4. otherwise a "real trip": DISPATCH if another real trip in a DIFFERENT zone
         occurs within verify_window_sec seconds, else LOCAL_ONLY.
    """
    n = len(events)
    base = [None] * n  # per-index: "PANIC", "SUPPRESSED", "FALSE_ALARM", or "REAL"

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
