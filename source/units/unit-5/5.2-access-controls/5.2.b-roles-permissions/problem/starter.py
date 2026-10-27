"""Starter code for 5.2.b. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import Dict, List


def solve(
    roles: Dict[str, List[str]],
    user_roles: Dict[str, List[str]],
    job_requirements: Dict[str, List[str]],
) -> Dict[str, List[str]]:
    """Flag users whose role-derived permissions exceed their job requirements.

    Args:
        roles: role name -> list of permissions it grants.
        user_roles: user name -> list of role names assigned to them.
        job_requirements: user name -> list of permissions their job requires.
    Returns:
        dict of user -> sorted list of excess (unauthorized) permissions.
        Users with no excess permissions are omitted entirely.
    """
    # TODO: for each user, union the permissions of their assigned roles, subtract
    #       their job_requirements, and include them in the result only if the
    #       excess set is non-empty (sorted list).
    raise NotImplementedError("implement solve() — see prompt.md")
