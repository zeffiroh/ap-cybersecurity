"""Starter code for 5.5.a. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import Dict, List


def solve(submissions: List[Dict[str, str]]) -> List[str]:
    """Classify each submission against per-field allowlist rules and known injection
    meta-character signatures; return the `value`s that are BLOCKED, in input order.

    Args:
        submissions: list of {"field": str, "type": str, "value": str}. `type` is one of
            "zip", "email", "quantity", "username".
    Returns:
        list[str] of the `value`s that fail validation (blocked), preserving input order.
    """
    # TODO: implement per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
