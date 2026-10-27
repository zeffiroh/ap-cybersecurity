"""Starter code for 2.4.a. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import List, Set, FrozenSet, Dict


def solve(entries: List[Dict], far_pairs: Set[FrozenSet]) -> List[str]:
    """Return a sorted, de-duplicated list of badge IDs that triggered alert rules.

    Args:
        entries: list of dicts with keys 'ts' (int Unix timestamp), 'badge' (str),
                 'door' (str), 'outcome' (str: 'GRANTED' or 'DENIED').
        far_pairs: set of frozensets, each containing two geographically separated door names.
    Returns:
        Sorted list of badge ID strings that triggered Rule 0, 1, or 2.
        See prompt.md and interface.md for rule definitions.
    """
    # TODO: implement the three detection rules per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
