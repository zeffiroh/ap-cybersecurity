from typing import Dict, List

_LAYER_MAP = {
    "firewall": "perimeter",
    "ips": "perimeter",
    "dns_filter": "perimeter",
    "vlan_segmentation": "network",
    "internal_firewall": "network",
    "wifi_protocol": "network",
    "endpoint_av": "host",
    "host_firewall": "host",
    "os_patching": "host",
    "input_validation": "application",
    "waf": "application",
    "app_auth": "application",
    "encryption_at_rest": "data",
    "dlp": "data",
    "data_classification": "data",
    "awareness_training": "human",
    "aup": "human",
    "access_review": "human",
    "incident_response_policy": "human",
}


def classify_layer(controls: List[Dict]) -> List[str]:
    result = []
    for c in controls:
        category = c["category"]
        if category not in _LAYER_MAP:
            raise ValueError(f"unknown category: {category}")
        result.append(_LAYER_MAP[category])
    return result
