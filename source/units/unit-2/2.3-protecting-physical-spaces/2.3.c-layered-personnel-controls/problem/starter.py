"""Starter code for 2.3.c. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""
from typing import Dict, List

VALID_CATEGORIES = {"perimeter", "personnel", "electronic", "barrier", "monitoring"}


def solve(layers: List[Dict]) -> Dict:
    """Audit a facility's layer list and return a defense-in-depth report.

    Args:
        layers: list of dicts with keys 'name' (str) and 'category' (str). 'category'
            should be one of VALID_CATEGORIES; anything else must be ignored.
    Returns:
        dict with keys 'depth_score' (int), 'categories_present' (sorted list[str]),
        'redundant_categories' (dict[str, int]), and 'recommendation' (str: STRONG /
        ADEQUATE / WEAK). See prompt.md and interface.md for exact rules and thresholds.
    """
    # TODO: implement per prompt.md
    raise NotImplementedError("implement solve() — see prompt.md")
