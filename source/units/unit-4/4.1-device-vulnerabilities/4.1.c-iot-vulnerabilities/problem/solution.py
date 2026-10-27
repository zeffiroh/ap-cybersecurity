"""Reference solution for 4.1.c. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""

INSECURE_PORTS = {23, 21}


def solve(device: dict) -> str:
    """Audit an IoT device dict and return its single dominant vulnerability verdict.

    Args:
        device: dict with keys default_password (bool), firmware_outdated (bool),
            open_ports (list[int]), unauthenticated_api (bool), encrypted_traffic (bool).
            Missing keys default to the "safe" value for that key.

    Returns:
        One of: "default_credentials", "outdated_firmware", "exposed_port",
        "unauthenticated_api", "unencrypted_traffic", "secure".
    """
    if not isinstance(device, dict):
        return "secure"

    default_password = bool(device.get("default_password", False))
    firmware_outdated = bool(device.get("firmware_outdated", False))
    open_ports = device.get("open_ports", []) or []
    unauthenticated_api = bool(device.get("unauthenticated_api", False))
    encrypted_traffic = bool(device.get("encrypted_traffic", True))

    # Priority order: default_credentials > outdated_firmware > exposed_port >
    # unauthenticated_api > unencrypted_traffic > secure

    if default_password:
        return "default_credentials"

    if firmware_outdated:
        return "outdated_firmware"

    if any(port in INSECURE_PORTS for port in open_ports):
        return "exposed_port"

    if unauthenticated_api:
        return "unauthenticated_api"

    if not encrypted_traffic:
        return "unencrypted_traffic"

    return "secure"
