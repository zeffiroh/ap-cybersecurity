# Coding problem, 3.2.a: Wi-Fi configuration security evaluator

**Skill:** Mitigate Risk · **Maps to:** 3.2.A · **Language:** Python 3 (pytest)

## Problem
You are building an automated Wi-Fi configuration checker for Crestfield Analytics, mirroring what
enterprise wireless assessment tools do. Given a dictionary describing one access point's
configuration, return the sorted list of security gap codes that configuration has, based on the
criteria from the lesson (protocol strength, PSK password length, guest network isolation, admin
interface password strength, and firmware currency).

## Function contract
Implement `evaluate_wifi_config(cfg)` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
- `cfg`: `dict` with:
  - `"protocol"`: `str`, one of `"WPA3"`, `"WPA2-AES"`, `"WPA2-TKIP"`, `"WEP"`, `"OPEN"`
  - `"mode"`: `str`, `"personal"` or `"enterprise"`
  - `"psk_length"`: `int`, length of the pre-shared key/password (only meaningful when
    `mode == "personal"`)
  - `"guest_network_isolated"`: `bool`, whether guest devices are on a separate, isolated SSID/VLAN
  - `"admin_password_strong"`: `bool`, whether the AP's management interface has a strong unique
    password
  - `"firmware_current"`: `bool`, whether the AP is running current (patched) firmware

## Output
A sorted `list[str]` of gap codes present in the configuration (empty list if there are no gaps).
Possible gap codes:
- `"insecure_protocol"`, protocol is `"WEP"`, `"WPA2-TKIP"`, or `"OPEN"`
- `"weak_psk"`, `mode == "personal"` and `psk_length < 20`
- `"no_guest_isolation"`, `guest_network_isolated` is `False`
- `"weak_admin_password"`, `admin_password_strong` is `False`
- `"outdated_firmware"`, `firmware_current` is `False`

## Examples
```python
cfg = {
    "protocol": "WPA2-TKIP", "mode": "personal", "psk_length": 12,
    "guest_network_isolated": True, "admin_password_strong": True, "firmware_current": True,
}
evaluate_wifi_config(cfg)
# -> ["insecure_protocol", "weak_psk"]

cfg2 = {
    "protocol": "WPA3", "mode": "enterprise", "psk_length": 0,
    "guest_network_isolated": True, "admin_password_strong": True, "firmware_current": True,
}
evaluate_wifi_config(cfg2)
# -> []
```

## Constraints
- Deterministic, offline, standard library only.
- `psk_length` is only checked when `mode == "personal"`; ignore it entirely for `"enterprise"`
  mode (enterprise mode uses per-user 802.1X credentials, not a shared PSK).
- Gap codes in the output list must be sorted alphabetically and contain no duplicates.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
