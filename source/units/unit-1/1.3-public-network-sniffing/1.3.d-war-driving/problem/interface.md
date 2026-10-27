# Interface, 1.3.d-wifi-risk-flagger (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(network: dict) -> list[str]
```

## Input (`network`)
A `dict` describing one Wi-Fi network and the user's posture toward it. Recognized keys
(any may be absent; extra keys such as `"ssid"` are ignored):

- `"encryption"`: `str`, Wi-Fi security type (`"open"`, `"wpa2"`, `"wpa3"`...). Compared
  case-insensitively. Missing, `None`, or `""` counts as **open**.
- `"verified"`: `bool`, `True` if the SSID was confirmed with an authoritative source.
  Missing counts as `False`.
- `"vpn"`: `bool`, `True` if a VPN tunnel is active. Missing counts as `False`.

## Output (`result`)
A **sorted, de-duplicated** `list[str]` drawn from
`{"no-vpn", "open-network", "unverified-ssid"}`. Empty list if no risk applies.

## Risk rules
- **open-network**, `encryption`, lowercased, is one of `{"open", "none", ""}` (or the key is
  absent / `None`). Encrypted types (`wpa`, `wpa2`, `wpa3`, anything else non-empty) do not flag.
- **unverified-ssid**, `verified` is not truthy.
- **no-vpn**, `vpn` is not truthy.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- `encryption` matching is case-insensitive.
- Output always sorted ascending and de-duplicated.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
