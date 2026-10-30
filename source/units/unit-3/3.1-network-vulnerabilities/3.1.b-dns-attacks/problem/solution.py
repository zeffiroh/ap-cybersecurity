from typing import List, Dict


def solve(queries: List[Dict]) -> List[str]:
    result = []
    for q in queries:
        candidates = [
            r for r in q["replies"]
            if r["tx_id"] == q["tx_id"] and r["port"] == q["port"] and r["qname"] == q["qname"]
        ]
        if not candidates:
            result.append("REJECT")
            continue
        winner = min(candidates, key=lambda r: r["arrival"])
        result.append("WIN" if winner["from"] == "authoritative" else "POISON")
    return result
