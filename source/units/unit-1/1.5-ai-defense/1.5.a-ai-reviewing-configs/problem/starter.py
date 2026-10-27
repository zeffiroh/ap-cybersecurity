"""Starter code for 1.5.a. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import List


def solve(config_lines: List[str]) -> List[str]:
    """Return sorted, de-duplicated security finding tags for insecure config directives.

    Args:
        config_lines: list of strings, each one line of a configuration file.
    Returns:
        Sorted list of finding tags such as "insecure:PermitRootLogin".
        See interface.md for the full rule set.
    """
    # TODO: iterate config_lines (case-insensitive, strip whitespace, skip blank/#-comment lines)
    #       apply each rule from interface.md, collect matching tags, return sorted+deduped.
    raise NotImplementedError("implement solve() — see prompt.md")
