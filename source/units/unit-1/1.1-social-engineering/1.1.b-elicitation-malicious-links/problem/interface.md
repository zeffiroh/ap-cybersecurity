# Interface, 1.1.b-link-file-analyzer (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(url_or_filename: str) -> list[str]
```

## Input (`url_or_filename`)
A single string. If it starts with `http://` or `https://` it is a URL; otherwise it is treated
as a bare filename.

## Output (`result`)
A **sorted, de-duplicated** `list[str]` drawn from
`{"dangerous-extension", "ip-url", "lookalike-domain", "mismatched-link"}`.
Empty list if no indicator is present.

## Detection rules (all case-insensitive)

### `ip-url`
The hostname portion of the URL matches an IPv4 address: four decimal octets separated by dots,
optionally followed by a port (e.g. `192.168.4.99`, `10.0.0.1:8080`).
Detection regex (applied to hostname only): `^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?$`

### `lookalike-domain`
The registrable domain (last two labels of the hostname, e.g. `paypa1.com`) matches any entry in
the LOOKALIKE_DOMAINS set below.

LOOKALIKE_DOMAINS (exact match after lowercasing the registrable domain):
```
paypa1.com, arnazon.com, dropbx.com, g00gle.com, faceb00k.com,
rn1crosoft.com, rnicrosott.com, rnicrosoft.com, linkedln.com,
app1e.com, twiitter.com, lnstagram.com
```

### `dangerous-extension`
The final extension of the string (extracted from the last path segment, or from the bare
filename if no URL) is in the DANGEROUS_EXTENSIONS set.

DANGEROUS_EXTENSIONS:
```
.exe, .scr, .bat, .cmd, .ps1, .vbs, .vbe, .js, .jse, .wsf, .wsh,
.jar, .pif, .com, .hta, .msi, .dll, .cpl, .reg
```

For double-extension filenames like `report.pdf.exe`, the final extension is `.exe`, that
extension alone triggers the indicator.

### `mismatched-link`
Applies only to URLs (not bare filenames).
A URL is a mismatched-link if:
1. The registrable domain is NOT in the TRUSTED_DOMAINS set below, AND
2. The URL contains at least one TRUSTED_BRAND keyword anywhere in the full URL string
   (scheme + host + path) EXCLUDING the registrable domain itself.

This models the pattern `http://bankofamerica.com.evil.net/...` where `bankofamerica.com`
appears as a subdomain of `evil.net`.

TRUSTED_DOMAINS (the real registrable domains):
```
paypal.com, amazon.com, dropbox.com, google.com, facebook.com,
microsoft.com, linkedin.com, apple.com, twitter.com, instagram.com,
bankofamerica.com, chase.com, wellsfargo.com, company.example,
shop.example, meridian-corp.example
```

TRUSTED_BRAND keywords (substring match in the full URL, case-insensitive):
```
paypal, amazon, dropbox, google, facebook, microsoft, linkedin,
apple, twitter, instagram, bankofamerica, chase, wellsfargo
```

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Matching is case-insensitive throughout.
- Output is always sorted ascending and de-duplicated.
- A single input may trigger multiple indicators simultaneously.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
