"""Starter code for 1.3.b. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import List


def solve(aps: List[dict]) -> List[str]:
    """Return a sorted, de-duplicated list of suspicious BSSIDs from a wireless scan.

    An AP is suspicious if:
      1. Its SSID is advertised by more than one BSSID (duplicate-SSID rule), OR
      2. Its SSID appears with multiple security levels and this AP does not have
         the strongest security level seen for that SSID (security-downgrade rule).

    Security strength order (weakest -> strongest): OPEN < WEP < WPA < WPA2 < WPA3

    Args:
        aps: list of dicts with keys ssid, bssid, security, signal
    Returns:
        sorted list of suspicious BSSIDs (empty list if none)
    """
    # TODO: implement the two detection rules described above and in interface.md
    raise NotImplementedError("implement solve() — see prompt.md")
