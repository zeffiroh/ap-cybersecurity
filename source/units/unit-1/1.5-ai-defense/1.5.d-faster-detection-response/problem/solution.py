from typing import List, Dict, Any


def solve(incidents: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not incidents:
        return {"mttr": 0.0, "auto_resolved": 0}

    total_time = sum(inc["resolved_at"] - inc["detected_at"] for inc in incidents)
    auto_count = sum(1 for inc in incidents if inc.get("auto") is True)

    return {
        "mttr": total_time / len(incidents),
        "auto_resolved": auto_count,
    }
