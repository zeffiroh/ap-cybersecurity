from typing import Dict, List

_INSECURE_PROTOCOLS = {"WEP", "WPA2-TKIP", "OPEN"}


def evaluate_wifi_config(cfg: Dict) -> List[str]:
    gaps = []

    if cfg["protocol"] in _INSECURE_PROTOCOLS:
        gaps.append("insecure_protocol")

    if cfg["mode"] == "personal" and cfg["psk_length"] < 20:
        gaps.append("weak_psk")

    if not cfg["guest_network_isolated"]:
        gaps.append("no_guest_isolation")

    if not cfg["admin_password_strong"]:
        gaps.append("weak_admin_password")

    if not cfg["firmware_current"]:
        gaps.append("outdated_firmware")

    return sorted(gaps)
