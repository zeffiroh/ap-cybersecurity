from typing import List

OPEN_VALUES = {"open", "none", ""}


def solve(network: dict) -> List[str]:
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
