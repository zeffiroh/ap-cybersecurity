# Coding problem, 3.2.c: Defense-in-depth layer classifier

**Skill:** Mitigate Risk · **Maps to:** 3.2.B, 3.2.C · **Language:** Python 3 (pytest)

## Problem
You are building a defense-in-depth mapping tool for Crestfield Analytics' security architecture
review. Given a list of deployed controls, assign each one to its correct layer in the layered
defense model taught in the lesson: `"perimeter"`, `"network"`, `"host"`, `"application"`,
`"data"`, or `"human"`.

## Function contract
Implement `classify_layer(controls)` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
- `controls`: `list[dict]`, each with:
  - `"name"`: `str`, a human-readable control name (not used for classification)
  - `"category"`: `str`, one of the following exact values:
    - Perimeter: `"firewall"`, `"ips"`, `"dns_filter"`
    - Network: `"vlan_segmentation"`, `"internal_firewall"`, `"wifi_protocol"`
    - Host: `"endpoint_av"`, `"host_firewall"`, `"os_patching"`
    - Application: `"input_validation"`, `"waf"`, `"app_auth"`
    - Data: `"encryption_at_rest"`, `"dlp"`, `"data_classification"`
    - Human: `"awareness_training"`, `"aup"`, `"access_review"`, `"incident_response_policy"`

## Output
A `list[str]` of layer assignments, **one per input control, in the same order as the input**.
Each entry is one of `"perimeter"`, `"network"`, `"host"`, `"application"`, `"data"`, `"human"`.

## Examples
```python
controls = [
    {"name": "Border firewall", "category": "firewall"},
    {"name": "WPA3 wireless", "category": "wifi_protocol"},
    {"name": "Annual phishing training", "category": "awareness_training"},
]
classify_layer(controls)  ->  ["perimeter", "network", "human"]
```

## Constraints
- Deterministic, offline, standard library only.
- Classification depends only on `"category"`, never on `"name"` text.
- `"category"` always contains one of the 16 listed values in test data (no invalid values).
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
