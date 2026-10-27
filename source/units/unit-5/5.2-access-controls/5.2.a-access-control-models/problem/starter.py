"""Starter code for 5.2.a. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import Dict


def solve(request: Dict[str, object]) -> Dict[str, object]:
    """Decide ALLOW/DENY for a DAC, MAC, or RBAC access request.

    Args:
        request: {"subject": dict, "object": dict, "action": str}
    Returns:
        {"allowed": bool, "reason": str} per the rules in prompt.md / interface.md.
    """
    # TODO: branch on request["object"]["model"] ("dac" | "mac" | "rbac") and apply
    #       the corresponding rule from prompt.md. Unknown model -> "unknown_model".
    raise NotImplementedError("implement solve() — see prompt.md")
