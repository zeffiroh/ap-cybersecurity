from typing import List, Dict

_ENCRYPTED_PORTS = {443, 22}
_CLEARTEXT_PORTS = {80, 23, 21}
_INDICATORS = ("password=", "Password:", "PASS ")


def solve(packets: List[Dict]) -> List[str]:
    result = []
    for p in packets:
        port = p["port"]
        if port in _ENCRYPTED_PORTS:
            result.append("SAFE")
        elif port in _CLEARTEXT_PORTS:
            payload = p["payload"]
            leaked = any(ind in payload for ind in _INDICATORS)
            result.append("LEAK" if leaked else "SAFE")
        else:
            result.append("SAFE")
    return result
