def solve(request: dict) -> str:
    justification_present = bool(request.get("justification_present", False))
    time_bound = request.get("time_bound", False)
    last_reviewed_days_ago = request.get("last_reviewed_days_ago", 0)

    if not justification_present:
        return "deny_no_justification"

    if last_reviewed_days_ago > 365:
        return "flag_privilege_creep"

    if time_bound is True:
        return "approve_time_bound"

    return "approve"
