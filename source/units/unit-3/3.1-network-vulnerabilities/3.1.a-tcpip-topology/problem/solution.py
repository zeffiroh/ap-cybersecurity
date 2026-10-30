import ipaddress
from typing import Any

def solve(data: Any) -> list[int]:
    if not isinstance(data, list):
        return []
    
    suspicious = []
    for idx, packet in enumerate(data):
        if not isinstance(packet, dict):
            continue
        src_ip = packet.get("src_ip")
        expected_subnet = packet.get("expected_subnet")
        if not src_ip or not expected_subnet:
            continue
        try:
            ip = ipaddress.ip_address(src_ip)
            net = ipaddress.ip_network(expected_subnet, strict=False)
            if ip not in net:
                suspicious.append(idx)
        except ValueError:
            suspicious.append(idx)
            
    return sorted(suspicious)
