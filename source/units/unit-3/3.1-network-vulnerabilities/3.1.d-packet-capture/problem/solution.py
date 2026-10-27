"""Reference solution for 3.1.d. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import List, Dict

_ENCRYPTED_PORTS = {443, 22}
_CLEARTEXT_PORTS = {80, 23, 21}
_INDICATORS = ("password=", "Password:", "PASS ")


def solve(packets: List[Dict]) -> List[str]:
    """Classify each packet as LEAK (cleartext credential exposed) or SAFE.

    Rules (see interface.md):
      1. port in {443, 22} -> always SAFE.
      2. port in {80, 23, 21} -> LEAK if payload contains any credential indicator, else SAFE.
      3. any other port -> SAFE.
    """
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
