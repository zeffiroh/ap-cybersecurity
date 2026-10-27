"""Starter code for 5.1.c. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import Dict


def solve(request: Dict[str, str], ownership: Dict[str, str]) -> Dict[str, object]:
    """Decide whether an API request is authorized (BOLA check).

    Args:
        request: {"user_id": str, "role": str, "object_id": str}
        ownership: dict mapping object_id -> owner user_id
    Returns:
        {"allowed": bool, "reason": str} where reason is one of
        "owner", "admin", "not_owner", "not_found".
    """
    # TODO: look up request["object_id"] in ownership.
    #   - not present -> {"allowed": False, "reason": "not_found"}
    #   - owner matches request["user_id"] -> {"allowed": True, "reason": "owner"}
    #   - else if request["role"] == "admin" -> {"allowed": True, "reason": "admin"}
    #   - else -> {"allowed": False, "reason": "not_owner"}
    raise NotImplementedError("implement solve() — see prompt.md")
