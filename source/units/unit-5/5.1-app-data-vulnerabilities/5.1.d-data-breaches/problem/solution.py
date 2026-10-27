"""Reference solution for 5.1.d. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import Dict

CATEGORY_POINTS = {
    "pii": 40,
    "financial": 40,
    "health": 40,
    "auth_plaintext": 40,
    "auth_hashed": 15,
    "email": 10,
    "public": 0,
}


def _scale_points(record_count: int) -> int:
    if record_count >= 1_000_000:
        return 30
    if record_count >= 10_000:
        return 20
    if record_count >= 100:
        return 10
    return 0


def _detect_points(days_to_detect: int) -> int:
    if days_to_detect > 30:
        return 20
    if days_to_detect >= 2:
        return 10
    return 0


def _label(score: int) -> str:
    if score >= 80:
        return "critical"
    if score >= 50:
        return "high"
    if score >= 20:
        return "medium"
    return "low"


def solve(report: Dict[str, object]) -> Dict[str, object]:
    """Score a data breach report's severity per the rubric."""
    categories = report.get("categories", [])
    record_count = report.get("record_count", 0)
    days_to_detect = report.get("days_to_detect", 0)

    score = sum(CATEGORY_POINTS.get(cat, 0) for cat in categories)
    score += _scale_points(record_count)
    score += _detect_points(days_to_detect)

    return {"score": score, "label": _label(score)}
