"""Reference solution for 1.4.a. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import Dict


def solve(signals: Dict[str, bool]) -> str:
    """Classify an inbound call/video session as 'suspect' or 'ok'.

    Rules applied in order (first match wins); missing keys treated as False.
    See interface.md for full contract.
    """
    g = signals.get

    # Rule 1: failed shared-secret check is definitive
    if g("no_shared_secret"):
        return "suspect"

    # Rule 2: refusing a callback is a strong indicator
    if g("refused_callback"):
        return "suspect"

    # Rule 3: audio artifact + financial urgency together
    if g("audio_artifact") and g("urgent_money_request"):
        return "suspect"

    # Rule 4: spoofed caller-ID on an unexpected channel
    if g("caller_id_spoofed") and g("unverified_channel"):
        return "suspect"

    # Rule 5: visible video artifact
    if g("video_face_mismatch"):
        return "suspect"

    # Rule 6: financial urgency arriving on an unexpected channel
    if g("urgent_money_request") and g("unverified_channel"):
        return "suspect"

    return "ok"
