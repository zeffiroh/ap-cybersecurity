"""Reference solution for 3.4.a. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml).

Implements a stateless and stateful packet classifier demonstrating the core difference
between the two firewall inspection models.
"""
from typing import List, Dict, Any


def _match_rules(rules: List[Dict], packet: Dict) -> str:
    """Apply rule list top-to-bottom; return first matched action, or 'drop'."""
    for rule in rules:
        proto_ok = rule["proto"] == "any" or rule["proto"] == packet["proto"]
        dport_ok = rule["dport"] == 0 or rule["dport"] == packet["dport"]
        if proto_ok and dport_ok:
            return rule["action"]
    return "drop"


def solve(rules: List[Dict], packets: List[Dict], mode: str) -> List[str]:
    """Classify each packet as 'allow' or 'drop' using the given rule set.

    Args:
        rules:   Ordered list of rule dicts (action, proto, dport).
        packets: List of packet dicts (src, dst, sport, dport, proto, flags).
        mode:    'stateless' or 'stateful'.

    Returns:
        List of 'allow' / 'drop' verdicts, one per packet.
    """
    if mode == "stateless":
        return [_match_rules(rules, pkt) for pkt in packets]

    # Stateful mode: maintain a connection-tracking table.
    # Key: (src, dst, sport, dport, proto)  Value: state string
    table: Dict[tuple, str] = {}
    verdicts: List[str] = []

    for pkt in packets:
        proto = pkt["proto"]
        flags = pkt.get("flags", "")
        key = (pkt["src"], pkt["dst"], pkt["sport"], pkt["dport"], proto)
        rev = (pkt["dst"], pkt["src"], pkt["dport"], pkt["sport"], proto)

        if proto != "tcp":
            # Non-TCP: rule matching only.
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
                # No established session for this exact endpoint pair: a stateful
                # firewall drops it even if a static rule would otherwise permit
                # the port, because it cannot verify the packet belongs to a real
                # connection.
                verdicts.append("drop")

        elif flags in ("RST", "FIN"):
            if key in table or rev in table:
                table.pop(key, None)
                table.pop(rev, None)
                verdicts.append("allow")
            else:
                verdicts.append("drop")

        else:
            # Unknown flag: rule matching.
            verdicts.append(_match_rules(rules, pkt))

    return verdicts
