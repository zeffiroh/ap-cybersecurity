# Coding problem, 4.2.b: Classify a login attempt's MFA strength

**Skill:** Mitigate Risk · **Maps to:** 4.2.A, 4.2.B · **Language:** Python 3 (pytest)

## Problem
A security analyst receives, for each login attempt, the list of authentication factors that were
presented (e.g. `["password", "sms_code"]`). Build the classifier that determines whether the
attempt satisfies true multi-factor authentication, and if so, whether it relies on a
phishing-resistant possession factor or a phishable one.

Categories of result:
- `"single_factor"`, the presented factors, once mapped to their factor category (knowledge /
  possession / inherence), cover fewer than two distinct categories. This includes presenting only
  one factor, presenting several factors from the *same* category (e.g. two passwords), an empty
  list, or a list of only unrecognized factor strings.
- `"mfa_phishing_resistant"`, two or more distinct factor categories are present, and at least one
  of the presented factors is a phishing-resistant possession factor (`hardware_key` or `fido2`).
- `"mfa_phishable"`, two or more distinct factor categories are present, but no phishing-resistant
  possession factor was used (e.g. it relies on `sms_code`, `totp_code`, `authenticator_app`,
  `push_approved`, or `backup_code` for the possession factor).

The exact factor-to-category mapping and full rule set are defined in `interface.md`, implementations must follow it precisely.

## Function contract
Implement `solve(factors: list[str]) -> str` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
A list of strings, each a recognized or unrecognized factor name. May be empty.

## Output
One of: `"single_factor"`, `"mfa_phishable"`, `"mfa_phishing_resistant"`.

## Examples
```
["password"]                          -> "single_factor"
["password", "password"]              -> "single_factor"
["password", "security_question"]     -> "single_factor"
["password", "sms_code"]              -> "mfa_phishable"
["password", "push_approved"]         -> "mfa_phishable"
["password", "hardware_key"]          -> "mfa_phishing_resistant"
["password", "sms_code", "hardware_key"] -> "mfa_phishing_resistant"
["biometric", "password"]             -> "mfa_phishable"
[]                                     -> "single_factor"
```

## Constraints
- Deterministic, offline, standard library only.
- Follow the exact factor -> category mapping in `interface.md`.
- Unrecognized factor strings must not raise an error; they are simply ignored.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
