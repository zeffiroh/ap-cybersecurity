# Interface, 3.2.c-defense-layer-classifier (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def classify_layer(controls: list[dict]) -> list[str]
```

## Input (`controls`)
`list[dict]` where each dict has:
- `"name"`: `str`, flavor text, not used for classification logic
- `"category"`: `str`, one of 16 exact values, grouped as:
  - perimeter: `"firewall"`, `"ips"`, `"dns_filter"`
  - network: `"vlan_segmentation"`, `"internal_firewall"`, `"wifi_protocol"`
  - host: `"endpoint_av"`, `"host_firewall"`, `"os_patching"`
  - application: `"input_validation"`, `"waf"`, `"app_auth"`
  - data: `"encryption_at_rest"`, `"dlp"`, `"data_classification"`
  - human: `"awareness_training"`, `"aup"`, `"access_review"`, `"incident_response_policy"`

## Output (`result`)
A `list[str]` the same length as `controls`, in the **same order as the input**, where each element
is one of `"perimeter"`, `"network"`, `"host"`, `"application"`, `"data"`, `"human"`.

## Classification rule
Look up `"category"` in the grouping table above and return the corresponding layer name.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- `"category"` always contains one of the 16 listed values in test data.
- Output order matches input order exactly.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
