"""Starter code for 2.3.b — Surveillance systems (CCTV, monitoring).
Student completes the TODO. This file intentionally FAILS the tests until implemented.

Task: implement solve(events) -> list[str]
See prompt.md for the full problem statement and interface.md for the contract.
"""


def solve(events: list[dict]) -> list[str]:
    """Analyze a camera event log and return sorted, de-duplicated alert strings.

    Args:
        events: list of dicts, each with keys:
                  camera_id (str), ts (int, Unix timestamp ascending),
                  motion (bool), person_detected (bool),
                  area (str), authorized_hours (tuple[int,int])
    Returns:
        Sorted, de-duplicated list of alert strings such as
        "AFTER_HOURS:CAM-01", "GHOST_MOTION:CAM-02", "CROWD_SERVER_ROOM".
    """
    # TODO: implement per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
