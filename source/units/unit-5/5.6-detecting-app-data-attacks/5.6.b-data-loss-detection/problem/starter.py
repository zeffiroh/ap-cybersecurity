"""Starter code for 5.6.b. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import Dict, List


def solve(
    transfers: List[Dict[str, object]],
    approved_destinations: List[str],
    volume_threshold_mb: int,
) -> List[str]:
    """DLP egress rule: flag outbound transfers that exceed a volume threshold AND go to a
    destination that is not on the approved list.

    Args:
        transfers: list of {"id": str, "bytes_mb": int, "destination": str}.
        approved_destinations: list[str] of known-good destination names.
        volume_threshold_mb: int — a transfer must exceed this size (strictly greater than)
            to be eligible for flagging.
    Returns:
        sorted list[str] of the transfer `id`s that should be flagged.
    """
    # TODO: implement per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
