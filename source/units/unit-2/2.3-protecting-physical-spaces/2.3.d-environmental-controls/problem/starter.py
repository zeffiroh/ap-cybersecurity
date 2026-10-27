"""Starter code for 2.3.d. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import List, Dict, Any


def solve(zones: List[Dict[str, Any]], policy: Dict[str, Dict[str, Any]]) -> List[str]:
    """Return a sorted, de-duplicated list of zone names that are non-compliant with the
    control policy for their room type.

    Args:
        zones: list of dicts with keys 'name' (str), 'room_type' (str), 'has_ups' (bool),
               'hvac_redundancy' (int), 'suppression' (str), 'has_leak_sensor' (bool).
        policy: dict mapping room_type -> requirements dict (see interface.md for keys:
                require_ups, min_hvac_redundancy, allowed_suppression, require_leak_sensor).
    Returns:
        Sorted list of zone name strings that fail one or more applicable requirements.
        See prompt.md and interface.md for the compliance rules.
    """
    # TODO: implement the compliance check per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
