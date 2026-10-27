# Interface, 4.1.c-iot-device-audit (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(device: dict) -> str
```

## Input (`device`)
A dictionary with keys:
- `default_password` (bool), True if the factory default password is still in use.
- `firmware_outdated` (bool), True if the firmware is out of date.
- `open_ports` (list[int]), open network ports on the device.
- `unauthenticated_api` (bool), True if the device's API requires no authentication.
- `encrypted_traffic` (bool), True if the device's traffic is encrypted (False = the risk
  condition: traffic is unencrypted).

Insecure/exposed management ports: `{23, 21}` (Telnet, FTP). Any other port does not count as
"exposed" for this problem.

## Output (`result`)
Exactly one string from:
`{"default_credentials", "outdated_firmware", "exposed_port", "unauthenticated_api",
"unencrypted_traffic", "secure"}`

## Priority order (highest severity first)
When a device matches more than one condition, return only the highest-priority match:
1. `default_password is True` -> `"default_credentials"`
2. `firmware_outdated is True` -> `"outdated_firmware"`
3. any of `{23, 21}` present in `open_ports` -> `"exposed_port"`
4. `unauthenticated_api is True` -> `"unauthenticated_api"`
5. `encrypted_traffic is False` -> `"unencrypted_traffic"`
6. none of the above -> `"secure"`

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- `open_ports` may be empty or contain any integers; only `23` and `21` trigger `"exposed_port"`.
- Missing keys should be treated as the "safe" default for that key (`False` for booleans,
  `[]` for `open_ports`, and `True` for `encrypted_traffic`, i.e. "assume secure/encrypted if
  not specified").
- Returns a single string (not a list).

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
