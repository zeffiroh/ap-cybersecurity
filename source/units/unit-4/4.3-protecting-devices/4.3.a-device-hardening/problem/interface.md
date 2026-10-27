# Interface, 4.3.a-device-hardening (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(data: dict) -> list[str]
```

## Input (`data`)
A dictionary with two keys: `"baseline"` and `"configuration"`.
The `"baseline"` dictionary contains the security requirements:
- `"min_password_length"` (int)
- `"disallowed_services"` (list of strings)
- `"firewall_enabled"` (bool)
- `"encryption_enabled"` (bool)
- `"allowed_accounts"` (list of strings)

The `"configuration"` dictionary contains the target device's actual settings:
- `"password_length"` (int, optional - default is `0` if missing)
- `"services"` (list of strings, optional - default is empty if missing)
- `"firewall_enabled"` (bool, optional - default is `False` if missing)
- `"encryption_enabled"` (bool, optional - default is `False` if missing)
- `"accounts"` (list of strings, optional - default is empty if missing)

## Output (`result`)
A list of strings representing the names of the checks from the baseline that failed.
The possible check names in the output list are:
- `"min_password_length"` (fails if configuration password length is less than baseline minimum)
- `"disallowed_services"` (fails if any service in the configuration is present in the baseline disallowed list)
- `"firewall_enabled"` (fails if baseline requires it but configuration has it set to False)
- `"encryption_enabled"` (fails if baseline requires it but configuration has it set to False)
- `"allowed_accounts"` (fails if configuration contains any accounts NOT present in the baseline allowed list)

The output list must be sorted alphabetically. If all checks pass, returns an empty list `[]`.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network.
- Standard library only.
- Case-sensitivity: comparisons for services and accounts are case-sensitive.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
