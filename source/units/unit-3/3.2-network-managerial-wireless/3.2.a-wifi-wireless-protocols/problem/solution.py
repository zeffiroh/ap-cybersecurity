"""Reference solution for 3.2.a. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import Dict, List

_INSECURE_PROTOCOLS = {"WEP", "WPA2-TKIP", "OPEN"}


def evaluate_wifi_config(cfg: Dict) -> List[str]:
    """Return the sorted list of security gap codes in a Wi-Fi AP configuration.

    Rules (see interface.md):
      - insecure_protocol: protocol in {WEP, WPA2-TKIP, OPEN}
      - weak_psk: mode == "personal" and psk_length < 20 (ignored for enterprise mode)
      - no_guest_isolation: guest_network_isolated is False
      - weak_admin_password: admin_password_strong is False
      - outdated_firmware: firmware_current is False
    """
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
