"""Starter code for 1.5.b. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import List


def solve(code: str) -> List[str]:
    """Return sorted, de-duplicated vulnerability tags for dangerous patterns in Python source code.

    Args:
        code: a string of Python source code to scan.
    Returns:
        Sorted list of finding tags such as "vuln:eval", "vuln:md5", etc.
        See interface.md for the full pattern rule set.
    """
    # TODO: search `code` for each dangerous pattern from interface.md.
    #       Note: "password =" matching is case-insensitive; others are case-sensitive.
    #       Return a sorted, de-duplicated list of finding tags.
    raise NotImplementedError("implement solve() — see prompt.md")
