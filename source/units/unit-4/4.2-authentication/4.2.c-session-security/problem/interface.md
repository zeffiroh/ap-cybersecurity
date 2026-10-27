# Interface, 4.2.c-session-incident-classifier (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(report: str) -> str
```

## Input (`report`)
A single string describing observed session behavior on a device, browser, or server.

## Output (`result`)
Exactly one string from
`{"hijacking", "fixation", "insecure_cookie", "timeout_issue", "secure", "unknown"}`.

## Indicator phrase sets (case-insensitive substring match)
- **fixation:** `fixation`, `pre-set session`, `attacker-supplied session`, `session id unchanged
  after login`, `id unchanged`, `session id before`, `known session id`, `id was already set`
- **hijacking:** `sniffed`, `sniffing`, `intercepted`, `stolen session`, `stole the session`,
  `replayed`, `captured token`, `plain http`, `plaintext`, `read by an injected script`,
  `read via injected`, `malware read the`, `xss` (only when paired with theft/read context, treated as a hijacking signal), `reused by an attacker`
- **insecure_cookie:** `missing httponly`, `no httponly`, `httponly flag`, `missing secure flag`,
  `no secure flag`, `missing samesite`, `no samesite`, `cookie has no`, `cookie is missing`,
  `readable from client-side javascript`, `not set to httponly`
- **timeout_issue:** `no idle timeout`, `no timeout`, `without a timeout`, `left unattended`,
  `no absolute timeout`, `never expires`, `does not expire`, `session never times out`,
  `unattended for`, `abandoned`, `kiosk`
- **secure:** `regenerated at login`, `session id regenerated`, `secure, httponly`, `all secure
  flags`, `properly secured`, `idle timeout` combined with `secure` context, `secure flags set`,
  `set secure`, `set httponly`, `samesite=strict`, `session expired automatically`
- If no indicator matches: return `"unknown"`.
- Priority order when multiple sets match (should not occur in well-formed test data, but if it
  does): fixation > hijacking > insecure_cookie > timeout_issue > secure > unknown.
  Rationale: fixation and hijacking describe an active compromise and must be surfaced first;
  insecure_cookie and timeout_issue describe latent misconfigurations; secure is the fallback
  "all clear" only when nothing else matched.

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Matching is case-insensitive substring match.
- Returns a single string (not a list).

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
