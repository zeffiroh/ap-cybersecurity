"""Reference solution for 3.4.b. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml).

Implements a first-match-wins ACL evaluator with an implicit deny-all.
"""
from typing import List, Dict


def _rule_matches(rule: Dict, packet: Dict) -> bool:
    if rule["src"] != "any" and rule["src"] != packet["src"]:
        return False
    if rule["dst"] != "any" and rule["dst"] != packet["dst"]:
        return False
    if rule["port"] != 0 and rule["port"] != packet["port"]:
        return False
    if rule["proto"] != "any" and rule["proto"] != packet["proto"]:
        return False
    return True


def solve(rules: List[Dict], packets: List[Dict]) -> List[str]:
    """Evaluate each packet against the ACL using first-match-wins logic.

    Args:
        rules:   Ordered list of ACL rule dicts (action, src, dst, port, proto).
        packets: List of packet dicts (src, dst, port, proto).

    Returns:
        List of 'allow' / 'deny' verdicts, one per packet, in order.
    """
    verdicts: List[str] = []
    for pkt in packets:
        verdict = "deny"  # implicit deny-all
        for rule in rules:
            if _rule_matches(rule, pkt):
                verdict = rule["action"]
                break
        verdicts.append(verdict)
    return verdicts
