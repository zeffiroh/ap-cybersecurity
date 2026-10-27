"""Starter code for 4.3.c. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""


def solve(vulns: list) -> list:
    """Assign an urgency label to each vulnerability per the patch-triage priority rules.

    Args:
        vulns: list of dicts with keys id (str), cvss (float), exploited_in_wild (bool),
            internet_facing (bool), end_of_life (bool).

    Returns:
        list of dicts, same order, each {"id": ..., "urgency": ...} where urgency is one of
        "emergency", "scheduled", "routine", "compensate".
    """
    # TODO: implement per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
