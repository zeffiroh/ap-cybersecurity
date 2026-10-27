"""Reference solution for 1.5.d. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml).

solve(incidents) -> {"mttr": float, "auto_resolved": int}
  mttr = mean(resolved_at - detected_at) across all incidents.
  auto_resolved = count of incidents with auto == True.
  Empty input returns {"mttr": 0.0, "auto_resolved": 0}.
"""
from typing import List, Dict, Any


def solve(incidents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute SOC MTTR and auto-resolved count from a list of incident records."""
    if not incidents:
        return {"mttr": 0.0, "auto_resolved": 0}

    total_time = sum(inc["resolved_at"] - inc["detected_at"] for inc in incidents)
    auto_count = sum(1 for inc in incidents if inc.get("auto") is True)

    return {
        "mttr": total_time / len(incidents),
        "auto_resolved": auto_count,
    }
