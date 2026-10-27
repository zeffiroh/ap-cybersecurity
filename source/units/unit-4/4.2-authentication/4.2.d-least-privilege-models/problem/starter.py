"""Starter code for 4.2.d. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import Any


def solve(request: dict) -> str:
    """Audit a single access request per the least-privilege priority rules.

    Args:
        request: dict with keys current_role (str), requested_access (str),
            justification_present (bool), time_bound (bool or None),
            last_reviewed_days_ago (int). Optional keys default per interface.md.

    Returns:
        One of: "approve", "deny_no_justification", "flag_privilege_creep",
        "approve_time_bound".
    """
    # TODO: implement per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
