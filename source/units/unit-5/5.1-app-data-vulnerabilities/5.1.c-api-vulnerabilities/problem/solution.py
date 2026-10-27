"""Reference solution for 5.1.c. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import Dict


def solve(request: Dict[str, str], ownership: Dict[str, str]) -> Dict[str, object]:
    """Decide whether an API request is authorized (BOLA check)."""
    object_id = request.get("object_id")
    user_id = request.get("user_id")
    role = request.get("role")

    if object_id not in ownership:
        return {"allowed": False, "reason": "not_found"}

    owner = ownership[object_id]
    if owner == user_id:
        return {"allowed": True, "reason": "owner"}
    if role == "admin":
        return {"allowed": True, "reason": "admin"}
    return {"allowed": False, "reason": "not_owner"}
