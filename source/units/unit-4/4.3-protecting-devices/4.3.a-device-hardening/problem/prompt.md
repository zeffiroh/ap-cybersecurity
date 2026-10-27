# Coding problem, 4.3.a: Device hardening configuration auditor

**Skill:** Mitigate Risk · **Maps to:** 4.3.A · **Language:** Python 3 (pytest)

## Problem
In a secure enterprise environment, devices must be configured according to strict security baselines before deployment. Over time, administrators or software installers may change settings, resulting in "configuration drift" that increases the device's attack surface.

Your task is to write a python function `solve(data)` that takes a target device's actual configuration and audit it against a security baseline. The function must return a list of all check names that the configuration fails, sorted alphabetically.

## Function contract
Implement `solve(data)` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
A dictionary with keys `"baseline"` and `"configuration"`.
Example:
```json
{
  "baseline": {
    "min_password_length": 12,
    "disallowed_services": ["ftp", "telnet"],
    "firewall_enabled": true,
    "encryption_enabled": true,
    "allowed_accounts": ["admin", "operator"]
  },
  "configuration": {
    "password_length": 8,
    "services": ["ssh", "ftp"],
    "firewall_enabled": false,
    "encryption_enabled": true,
    "accounts": ["admin", "guest", "operator"]
  }
}
```

## Output
A list of strings representing the names of the failing checks from the baseline, sorted alphabetically.
Example output for the input above:
```json
["allowed_accounts", "disallowed_services", "firewall_enabled", "min_password_length"]
```
*(Explanation: password length 8 is less than 12; ftp service is disallowed; firewall is false; guest account is not allowed)*

## Constraints
- If an expected configuration field is missing, default values apply:
  - `password_length`: `0`
  - `services`: `[]`
  - `firewall_enabled`: `False`
  - `encryption_enabled`: `False`
  - `accounts`: `[]`
- Standard library only.
- Case-sensitive string matching for services and accounts.

## How to run
```
cd problem && python -m pytest tests.py -q
```
