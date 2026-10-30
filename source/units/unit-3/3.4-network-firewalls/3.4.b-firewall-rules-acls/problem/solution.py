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
    verdicts: List[str] = []
    for pkt in packets:
        verdict = "deny"
        for rule in rules:
            if _rule_matches(rule, pkt):
                verdict = rule["action"]
                break
        verdicts.append(verdict)
    return verdicts
