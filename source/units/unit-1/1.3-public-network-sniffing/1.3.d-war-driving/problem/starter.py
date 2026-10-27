"""Starter code for 1.3.d. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import List


def solve(network: dict) -> List[str]:
    """Return the sorted, de-duplicated risk flags for one network description.

    Flags: "open-network", "unverified-ssid", "no-vpn".
    See prompt.md and interface.md for the rules.

    Args:
        network: dict with optional keys "encryption" (str), "verified" (bool), "vpn" (bool).
    Returns:
        sorted list of the risk-flag strings that apply ([] if none).
    """
    # TODO: flag "open-network" when encryption is open/missing,
    #       "unverified-ssid" when not verified, "no-vpn" when no VPN active.
    #       Return the flags sorted and de-duplicated.
    raise NotImplementedError("implement solve() — see prompt.md")
