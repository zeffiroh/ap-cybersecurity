"""Reference solution for 1.3.d. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml).

Applies the three-step public-Wi-Fi protocol as risk flags: verify the SSID, avoid open
networks, always use a VPN. Pure, deterministic, stdlib only."""
from typing import List

OPEN_VALUES = {"open", "none", ""}


def solve(network: dict) -> List[str]:
    """Return the sorted, de-duplicated risk flags for one network description.

    Flags: "open-network", "unverified-ssid", "no-vpn".
    See prompt.md / interface.md for the rules.
    """
    network = network or {}
    flags = set()

    encryption = network.get("encryption")
    if encryption is None or str(encryption).strip().lower() in OPEN_VALUES:
        flags.add("open-network")

    if not network.get("verified", False):
        flags.add("unverified-ssid")

    if not network.get("vpn", False):
        flags.add("no-vpn")

    return sorted(flags)
