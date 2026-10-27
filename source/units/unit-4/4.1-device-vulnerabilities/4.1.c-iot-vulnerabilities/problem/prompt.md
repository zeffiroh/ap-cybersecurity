# Coding problem, 4.1.c: Audit an IoT device for its dominant vulnerability

**Skill:** Analyze Risk · **Maps to:** 4.1.A, 4.1.C · **Language:** Python 3 (pytest)

## Problem
A security analyst is auditing smart devices on a network. Each device is described by a
dictionary of attributes. Build the classifier that inspects a device and returns its single most
severe vulnerability category, or `"secure"` if none of the checked issues are present.

A device can technically have more than one issue at once; when it does, report only the most
severe one, using this fixed priority order (highest severity first):

1. `"default_credentials"`, the device still uses its factory default password
2. `"outdated_firmware"`, the device's firmware is out of date
3. `"exposed_port"`, the device has an insecure management port open (23 = Telnet, 21 = FTP)
4. `"unauthenticated_api"`, the device's API accepts requests with no authentication
5. `"unencrypted_traffic"`, the device's network traffic is not encrypted
6. `"secure"`, none of the above apply

## Function contract
Implement `solve(device: dict) -> str` in `starter.py` (see `interface.md` / `blackbox.yaml`).
Return the single verdict label string.

## Input
A dictionary with the following keys:
- `default_password` (bool), True if the factory default password is still in use
- `firmware_outdated` (bool), True if the firmware is out of date
- `open_ports` (list[int]), list of open network ports on the device
- `unauthenticated_api` (bool), True if the device's API requires no authentication
- `encrypted_traffic` (bool), True if the device's traffic is encrypted (note: False means
  traffic is UNencrypted, which is the risk condition)

An insecure management port is any of `23` (Telnet) or `21` (FTP) appearing in `open_ports`.

## Output
One of: `"default_credentials"`, `"outdated_firmware"`, `"exposed_port"`,
`"unauthenticated_api"`, `"unencrypted_traffic"`, `"secure"`.

## Examples
```
{"default_password": True, "firmware_outdated": True, "open_ports": [23], "unauthenticated_api": True, "encrypted_traffic": False}  ->  "default_credentials"
{"default_password": False, "firmware_outdated": True, "open_ports": [443], "unauthenticated_api": False, "encrypted_traffic": True}  ->  "outdated_firmware"
{"default_password": False, "firmware_outdated": False, "open_ports": [23, 443], "unauthenticated_api": False, "encrypted_traffic": True}  ->  "exposed_port"
{"default_password": False, "firmware_outdated": False, "open_ports": [443], "unauthenticated_api": True, "encrypted_traffic": True}  ->  "unauthenticated_api"
{"default_password": False, "firmware_outdated": False, "open_ports": [443], "unauthenticated_api": False, "encrypted_traffic": False}  ->  "unencrypted_traffic"
{"default_password": False, "firmware_outdated": False, "open_ports": [443], "unauthenticated_api": False, "encrypted_traffic": True}  ->  "secure"
```

## Constraints
- Deterministic, offline, standard library only.
- Priority order is fixed as listed above and must be applied exactly.
- Only ports `23` and `21` count as insecure/exposed management ports.
- Exactly one label returned (string, not list).
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
