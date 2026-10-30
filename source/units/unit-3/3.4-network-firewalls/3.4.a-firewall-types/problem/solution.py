from typing import List, Dict, Any


def _match_rules(rules: List[Dict], packet: Dict) -> str:
    for rule in rules:
        proto_ok = rule["proto"] == "any" or rule["proto"] == packet["proto"]
        dport_ok = rule["dport"] == 0 or rule["dport"] == packet["dport"]
        if proto_ok and dport_ok:
            return rule["action"]
    return "drop"


def solve(rules: List[Dict], packets: List[Dict], mode: str) -> List[str]:
    if mode == "stateless":
        return [_match_rules(rules, pkt) for pkt in packets]

    table: Dict[tuple, str] = {}
    verdicts: List[str] = []

    for pkt in packets:
        proto = pkt["proto"]
        flags = pkt.get("flags", "")
        key = (pkt["src"], pkt["dst"], pkt["sport"], pkt["dport"], proto)
        rev = (pkt["dst"], pkt["src"], pkt["dport"], pkt["sport"], proto)

        if proto != "tcp":
            verdicts.append(_match_rules(rules, pkt))
            continue

        if flags == "SYN":
            rule_verdict = _match_rules(rules, pkt)
            if rule_verdict == "allow":
                table[key] = "SYN_SENT"
                verdicts.append("allow")
            else:
                verdicts.append("drop")

        elif flags == "SYN-ACK":
            if rev in table:
                table[rev] = "ESTABLISHED"
                verdicts.append("allow")
            else:
                verdicts.append("drop")

        elif flags in ("ACK", "DATA"):
            if table.get(key) == "ESTABLISHED" or table.get(rev) == "ESTABLISHED":
                verdicts.append("allow")
            else:
                verdicts.append("drop")

        elif flags in ("RST", "FIN"):
            if key in table or rev in table:
                table.pop(key, None)
                table.pop(rev, None)
                verdicts.append("allow")
            else:
                verdicts.append("drop")

        else:
            verdicts.append(_match_rules(rules, pkt))

    return verdicts
