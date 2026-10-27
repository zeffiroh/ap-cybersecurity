"""Starter code for 3.2.a. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import Dict, List


def evaluate_wifi_config(cfg: Dict) -> List[str]:
    """Return the sorted list of security gap codes in a Wi-Fi AP configuration.

    Args:
        cfg: dict with keys 'protocol' (str), 'mode' (str: 'personal'/'enterprise'),
             'psk_length' (int), 'guest_network_isolated' (bool),
             'admin_password_strong' (bool), 'firmware_current' (bool).
    Returns:
        Sorted list (no duplicates) of gap codes; see prompt.md / interface.md for the exact
        codes and rules.
    """
    # TODO: implement the gap-detection rules per prompt.md
    raise NotImplementedError("implement evaluate_wifi_config() — see prompt.md")
