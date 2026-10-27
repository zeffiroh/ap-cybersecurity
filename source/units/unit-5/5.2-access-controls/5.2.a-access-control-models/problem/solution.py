"""Reference solution for 5.2.a. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import Dict

_LEVELS = {"public": 0, "confidential": 1, "secret": 2, "top_secret": 3}


def solve(request: Dict[str, object]) -> Dict[str, object]:
    """Decide ALLOW/DENY for a DAC, MAC, or RBAC access request."""
    subject = request["subject"]
    obj = request["object"]
    action = request["action"]
    model = obj.get("model")

    if model == "dac":
        if subject.get("name") == obj.get("owner"):
            return {"allowed": True, "reason": "owner"}
        grants = obj.get("grants", {})
        if subject.get("name") in grants.get(action, []):
            return {"allowed": True, "reason": "granted"}
        return {"allowed": False, "reason": "dac_denied"}

    if model == "mac":
        sub_level = _LEVELS.get(subject.get("clearance"), -1)
        obj_level = _LEVELS.get(obj.get("classification"), 99)
        if sub_level >= obj_level:
            return {"allowed": True, "reason": "clearance_sufficient"}
        return {"allowed": False, "reason": "clearance_insufficient"}

    if model == "rbac":
        allowed_roles = obj.get("allowed_roles", {}).get(action, [])
        subject_roles = subject.get("roles", [])
        if any(r in allowed_roles for r in subject_roles):
            return {"allowed": True, "reason": "role_match"}
        return {"allowed": False, "reason": "rbac_denied"}

    return {"allowed": False, "reason": "unknown_model"}
