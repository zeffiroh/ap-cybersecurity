def solve(data: dict) -> list[str]:
    """Audit a device's configuration against a security baseline.

    Args:
        data: A dict with keys "baseline" and "configuration".

    Returns:
        A list of failing baseline check names, sorted alphabetically.
    """
    baseline = data.get("baseline", {})
    config = data.get("configuration", {})

    failed = []

    # Check 1: min_password_length
    min_pw = baseline.get("min_password_length", 0)
    actual_pw = config.get("password_length", 0)
    if actual_pw < min_pw:
        failed.append("min_password_length")

    # Check 2: disallowed_services
    disallowed_srv = set(baseline.get("disallowed_services", []))
    actual_srv = config.get("services", [])
    if any(s in disallowed_srv for s in actual_srv):
        failed.append("disallowed_services")

    # Check 3: firewall_enabled
    fw_required = baseline.get("firewall_enabled", False)
    fw_actual = config.get("firewall_enabled", False)
    if fw_required and not fw_actual:
        failed.append("firewall_enabled")

    # Check 4: encryption_enabled
    enc_required = baseline.get("encryption_enabled", False)
    enc_actual = config.get("encryption_enabled", False)
    if enc_required and not enc_actual:
        failed.append("encryption_enabled")

    # Check 5: allowed_accounts
    allowed_acc = set(baseline.get("allowed_accounts", []))
    actual_acc = config.get("accounts", [])
    if any(a not in allowed_acc for a in actual_acc):
        failed.append("allowed_accounts")

    return sorted(failed)
