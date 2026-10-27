"""Reference solution for 5.6.b. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import Dict, List


def solve(
    transfers: List[Dict[str, object]],
    approved_destinations: List[str],
    volume_threshold_mb: int,
) -> List[str]:
    """DLP egress rule: flag transfer `id`s that exceed volume_threshold_mb AND whose
    destination is NOT in approved_destinations. Returns ids sorted ascending (as given,
    since ids are unique strings, sorted lexicographically)."""
    approved = set(approved_destinations)
    flagged = [
        t["id"]
        for t in transfers
        if t["bytes_mb"] > volume_threshold_mb and t["destination"] not in approved
    ]
    return sorted(flagged)
