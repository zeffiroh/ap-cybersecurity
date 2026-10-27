"""Reference solution for 5.2.b. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import Dict, List


def solve(
    roles: Dict[str, List[str]],
    user_roles: Dict[str, List[str]],
    job_requirements: Dict[str, List[str]],
) -> Dict[str, List[str]]:
    """Flag users whose role-derived permissions exceed their job requirements."""
    result: Dict[str, List[str]] = {}
    for user, assigned_roles in user_roles.items():
        granted = set()
        for role in assigned_roles:
            granted.update(roles.get(role, []))
        required = set(job_requirements.get(user, []))
        excess = granted - required
        if excess:
            result[user] = sorted(excess)
    return result
