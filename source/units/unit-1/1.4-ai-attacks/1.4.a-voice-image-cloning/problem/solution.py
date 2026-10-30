from typing import Dict


def solve(signals: Dict[str, bool]) -> str:
    g = signals.get

    if g("no_shared_secret"):
        return "suspect"

    if g("refused_callback"):
        return "suspect"

    if g("audio_artifact") and g("urgent_money_request"):
        return "suspect"

    if g("caller_id_spoofed") and g("unverified_channel"):
        return "suspect"

    if g("video_face_mismatch"):
        return "suspect"

    if g("urgent_money_request") and g("unverified_channel"):
        return "suspect"

    return "ok"
