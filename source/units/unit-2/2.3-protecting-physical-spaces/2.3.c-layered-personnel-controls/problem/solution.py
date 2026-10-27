"""Reference solution for 2.3.c. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import Dict, List

VALID_CATEGORIES = {"perimeter", "personnel", "electronic", "barrier", "monitoring"}


def solve(layers: List[Dict]) -> Dict:
    """Audit a facility's layer list and return a defense-in-depth report.

    depth_score = number of distinct valid categories present.
    categories_present = sorted list of those categories.
    redundant_categories = {category: extra_count} for categories with >1 layer.
    recommendation = STRONG (depth>=5) / ADEQUATE (3-4) / WEAK (<=2).
    Invalid category strings are ignored entirely.
    """
    counts: Dict[str, int] = {}
    for layer in layers:
        category = layer.get("category")
        if category not in VALID_CATEGORIES:
            continue
        counts[category] = counts.get(category, 0) + 1

    depth_score = len(counts)
    categories_present = sorted(counts.keys())
    redundant_categories = {c: n - 1 for c, n in counts.items() if n > 1}

    if depth_score >= 5:
        recommendation = "STRONG"
    elif depth_score >= 3:
        recommendation = "ADEQUATE"
    else:
        recommendation = "WEAK"

    return {
        "depth_score": depth_score,
        "categories_present": categories_present,
        "redundant_categories": redundant_categories,
        "recommendation": recommendation,
    }
