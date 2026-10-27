"""Reference solution for 4.2.d. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""


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
    justification_present = bool(request.get("justification_present", False))
    time_bound = request.get("time_bound", False)
    last_reviewed_days_ago = request.get("last_reviewed_days_ago", 0)

    # Rule 1: missing justification overrides everything else.
    if not justification_present:
        return "deny_no_justification"

    # Rule 2: stale access review (strictly more than 365 days).
    if last_reviewed_days_ago > 365:
        return "flag_privilege_creep"

    # Rule 3: time-bound (just-in-time) access.
    if time_bound is True:
        return "approve_time_bound"

    # Rule 4: default approval.
    return "approve"
