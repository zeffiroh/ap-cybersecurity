# Coding problem, 3.3.b: Zero Trust Access Proxy

**Skill:** Mitigate Risk · **Maps to:** 3.3.B, 3.3.C · **Language:** Python 3 (pytest)

## Problem
In a Zero Trust Network Architecture (ZTNA), network access is never implicitly granted based on a user's location. Instead, every request to access a corporate resource must be explicitly authenticated, authorized, and checked for health compliance.

You are tasked with implementing the evaluation logic for a Zero Trust access proxy. The proxy evaluates a batch of access requests against a central policy and filters out any requests that fail to meet authorization, location, or posture requirements.

## Function contract
Implement `solve(requests: list, policy: dict) -> list` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
- `requests`: A list of dictionaries representing connection requests.
  ```python
  requests = [
      {
          "id": "REQ-001",
          "user": "alice",
          "role": "doctor",
          "resource": "ehr_db",
          "ip": "192.168.1.50",
          "device_posture": {"antivirus_ok": True, "disk_encrypted": True}
      }
  ]
  ```
- `policy`: A dictionary detailing the security rules.
  ```python
  policy = {
      "allowed_roles": {
          "ehr_db": ["doctor", "admin"],
          "mri_machine": ["admin", "technician"]
      },
      "requires_internal": ["ehr_db", "mri_machine"],
      "requires_posture": ["ehr_db"],
      "internal_prefixes": ["192.168.1.", "10.0."]
  }
  ```

## Output
A list of strings representing the `id`s of requests that are **allowed**, maintaining their original order.

## Examples
```python
requests = [
    {
        "id": "REQ-001",
        "user": "alice",
        "role": "doctor",
        "resource": "ehr_db",
        "ip": "192.168.1.50",
        "device_posture": {"antivirus_ok": True, "disk_encrypted": True}
    },
    {
        "id": "REQ-002",
        "user": "bob",
        "role": "guest",
        "resource": "ehr_db",
        "ip": "192.168.1.60",
        "device_posture": {"antivirus_ok": True}
    }
]
# REQ-001 is allowed (role is doctor, IP matches internal prefix, posture checks are all True).
# REQ-002 is denied (guest role is not allowed on ehr_db).

solve(requests, policy) -> ["REQ-001"]
```

## Constraints
- Deterministic, offline, standard library only.
- All requests have the required keys.
- Must pass all cases in `tests.py`.
