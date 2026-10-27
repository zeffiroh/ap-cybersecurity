# Interface, 4.2.b-mfa-classifier (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(factors: list[str]) -> str
```

## Input (`factors`)
A list of strings, each naming an authentication factor presented during one login attempt, e.g.
`["password", "hardware_key"]`. Order does not matter. The list may be empty.

## Factor -> category mapping (exact, case-sensitive strings)
| factor string | category | phishing-resistant? |
|---|---|---|
| `password` | knowledge | n/a |
| `pin` | knowledge | n/a |
| `security_question` | knowledge | n/a |
| `sms_code` | possession | no |
| `totp_code` | possession | no |
| `authenticator_app` | possession | no |
| `push_approved` | possession | no (unverified push approval; MFA-fatigue risk) |
| `backup_code` | possession | no |
| `hardware_key` | possession | **yes** |
| `fido2` | possession | **yes** |
| `biometric` | inherence | no |

Any string not in this table is an **unrecognized factor** and is ignored when determining
categories (it does not count toward the category set and does not trigger phishing-resistant
status), but it does not cause an error.

## Output (`result`)
Exactly one string from `{"single_factor", "mfa_phishable", "mfa_phishing_resistant"}`.

## Classification rules
1. Map every string in `factors` to a category using the table above; unrecognized strings map to
   no category and are skipped.
2. Let `distinct_categories` be the set of distinct categories (`knowledge`, `possession`,
   `inherence`) actually present among recognized factors.
3. If `len(distinct_categories) < 2` (this includes an empty list, an all-unrecognized list, and a
   list where every recognized factor maps to the same single category, e.g. two knowledge
   credentials): return `"single_factor"`.
4. Otherwise (2 or more distinct categories are present):
   - If any recognized factor is a phishing-resistant possession factor (`hardware_key` or
     `fido2`): return `"mfa_phishing_resistant"`.
   - Otherwise: return `"mfa_phishable"`.

Phishing-resistance takes priority: if a phishing-resistant possession factor is present alongside
any number of phishable factors, the result is still `"mfa_phishing_resistant"`.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Does not raise on empty lists or unrecognized factor strings.
- Returns a single string (not a list).

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
