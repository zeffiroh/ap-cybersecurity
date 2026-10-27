"""Reference solution for 4.4.c. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""

WEIGHTS = {
    "known_malicious_hash": 6,
    "av_disabled": 5,
    "new_admin_account": 4,
    "unusual_outbound_traffic": 3,
    "unexpected_scheduled_task": 3,
    "registry_run_key_added": 2,
    "failed_login_cluster": 1,
}


def solve(iocs: list) -> str:
    """Sum the weights of unique observed IOCs and classify a compromise verdict.

    Args:
        iocs: list of str IOC type identifiers observed on one device.

    Returns:
        "clean" (score < 4), "suspicious" (4 <= score < 8), or "compromised" (score >= 8).
    """
    unique_iocs = set(iocs)
    score = sum(WEIGHTS.get(ioc, 0) for ioc in unique_iocs)

    if score >= 8:
        return "compromised"
    if score >= 4:
        return "suspicious"
    return "clean"
