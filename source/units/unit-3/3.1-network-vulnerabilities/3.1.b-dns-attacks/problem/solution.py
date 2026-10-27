"""Reference solution for 3.1.b. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import List, Dict


def solve(queries: List[Dict]) -> List[str]:
    """Classify each DNS query's resolver race outcome as WIN, POISON, or REJECT.

    Rules (see interface.md):
      1. A reply is a "valid candidate" iff tx_id, port, and qname all match the query.
      2. No valid candidates -> REJECT.
      3. Otherwise the valid candidate with the smallest 'arrival' wins the race:
         from == "authoritative" -> WIN, from == "attacker" -> POISON.
    """
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
