# Coding problem, 1.3.d: Public Wi-Fi risk flagger

**Skill:** Mitigate Risk · **Maps to:** 1.3.B, 1.3.C · **Language:** Python 3 (pytest)

## Problem
You are building the risk-assessment routine a network-policy tool runs before letting a device
connect to a public Wi-Fi network. Given a description of one network and the user's current
posture, return the **risk flags** that apply, so the user (or an administrator) can make an
informed decision. This is exactly the three-step personal protocol from the lesson, expressed
as code: verify the SSID, avoid open networks, always use a VPN.

The function is pure and deterministic, no network, no I/O.

## Function contract
Implement `solve(network: dict) -> list[str]` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
`network`, a `dict` describing one network and the user's posture toward it. Recognized keys:

| Key | Type | Meaning |
|-----|------|---------|
| `"encryption"` | `str` | Wi-Fi security type, e.g. `"open"`, `"wpa2"`, `"wpa3"`. Case-insensitive. Missing / `None` / `""` is treated as open (worst case). |
| `"verified"` | `bool` | `True` if the SSID was confirmed with venue staff / an official source. Missing is treated as `False`. |
| `"vpn"` | `bool` | `True` if a VPN tunnel is active on the device. Missing is treated as `False`. |

Example:
```python
{"ssid": "AirportFreeWifi", "encryption": "open", "verified": False, "vpn": False}
```

## Output
A **sorted, de-duplicated** `list[str]` of the risk flags that apply, drawn from:

- `"open-network"`, the network is open (no Wi-Fi-layer encryption).
- `"unverified-ssid"`, the SSID has not been confirmed with an authoritative source.
- `"no-vpn"`, no VPN is protecting the user's traffic.

Return `[]` when none apply (a verified, encrypted network used over a VPN).

## Examples
```
{"encryption": "open", "verified": False, "vpn": False}   -> ["no-vpn", "open-network", "unverified-ssid"]
{"encryption": "wpa2", "verified": True,  "vpn": True}     -> []
{"encryption": "wpa2", "verified": True,  "vpn": False}    -> ["no-vpn"]
{"encryption": "WPA3", "verified": False, "vpn": True}     -> ["unverified-ssid"]
{}                                                         -> ["no-vpn", "open-network", "unverified-ssid"]
```

## Constraints
- Deterministic, offline, standard library only.
- Matching of `encryption` is case-insensitive.
- Output always sorted ascending and de-duplicated.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
