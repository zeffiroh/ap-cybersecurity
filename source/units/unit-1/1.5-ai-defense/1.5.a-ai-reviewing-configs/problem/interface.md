# Interface, 1.5.a-config-auditor (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(config_lines: list[str]) -> list[str]
```

## Input (`config_lines`)
A list of strings, each representing one line of a configuration file (e.g., SSH `sshd_config`
or a generic service config). Lines may include whitespace, inline comments, or blank lines.
Matching is case-insensitive and strips leading/trailing whitespace per line.

## Output (`result`)
A **sorted, de-duplicated** `list[str]` of finding tags drawn from the set below.
Return an empty list if no insecure settings are found.

## Rule set (case-insensitive substring match on each stripped line)

| Tag returned                      | Trigger substring(s)                              | Why it is insecure                          |
|-----------------------------------|---------------------------------------------------|---------------------------------------------|
| `"insecure:PermitRootLogin"`      | `permitrootlogin yes`                             | Allows direct root login over SSH           |
| `"insecure:PasswordAuthentication"` | `passwordauthentication yes`                    | Enables brute-force password attacks        |
| `"insecure:Port23"`               | `port 23`                                         | Port 23 = Telnet; cleartext credentials     |
| `"insecure:SSLDisabled"`          | `ssl false` OR `ssl off` OR `tls false` OR `tls off` | Disables transport encryption           |
| `"insecure:X11Forwarding"`        | `x11forwarding yes`                               | Unnecessary attack surface                  |
| `"insecure:PermitEmptyPasswords"` | `permitemptypasswords yes`                        | Allows accounts with no password            |

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Matching is case-insensitive. Output always sorted ascending (lexicographic) and de-duplicated.
- A single line may trigger at most one rule (rules are mutually exclusive by tag).
- Blank lines and lines whose stripped form starts with `#` are ignored.
- A config_lines value of `[]` returns `[]`.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
