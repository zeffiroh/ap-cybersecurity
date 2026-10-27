# Interface, 3.2.a-wifi-config-evaluator (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def evaluate_wifi_config(cfg: dict) -> list[str]
```

## Input (`cfg`)
`dict` with:
- `"protocol"`: `str`, one of `"WPA3"`, `"WPA2-AES"`, `"WPA2-TKIP"`, `"WEP"`, `"OPEN"`
- `"mode"`: `str`, `"personal"` or `"enterprise"`
- `"psk_length"`: `int`, PSK/password length (meaningful only when `mode == "personal"`)
- `"guest_network_isolated"`: `bool`
- `"admin_password_strong"`: `bool`
- `"firmware_current"`: `bool`

## Output (`result`)
A sorted `list[str]` (no duplicates) of gap codes:
- `"insecure_protocol"`, `protocol` in `{"WEP", "WPA2-TKIP", "OPEN"}`
- `"weak_psk"`, `mode == "personal"` and `psk_length < 20`
- `"no_guest_isolation"`, `guest_network_isolated is False`
- `"weak_admin_password"`, `admin_password_strong is False`
- `"outdated_firmware"`, `firmware_current is False`

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- `psk_length` is ignored (never triggers `"weak_psk"`) when `mode == "enterprise"`.
- Output is sorted alphabetically with no duplicates; empty list if no gaps apply.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
