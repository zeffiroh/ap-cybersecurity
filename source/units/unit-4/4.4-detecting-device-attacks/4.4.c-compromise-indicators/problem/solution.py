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
    unique_iocs = set(iocs)
    score = sum(WEIGHTS.get(ioc, 0) for ioc in unique_iocs)

    if score >= 8:
        return "compromised"
    if score >= 4:
        return "suspicious"
    return "clean"
