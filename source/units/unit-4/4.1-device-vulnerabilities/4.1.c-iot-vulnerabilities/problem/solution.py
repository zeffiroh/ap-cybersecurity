INSECURE_PORTS = {23, 21}


def solve(device: dict) -> str:
    if not isinstance(device, dict):
        return "secure"

    default_password = bool(device.get("default_password", False))
    firmware_outdated = bool(device.get("firmware_outdated", False))
    open_ports = device.get("open_ports", []) or []
    unauthenticated_api = bool(device.get("unauthenticated_api", False))
    encrypted_traffic = bool(device.get("encrypted_traffic", True))


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
