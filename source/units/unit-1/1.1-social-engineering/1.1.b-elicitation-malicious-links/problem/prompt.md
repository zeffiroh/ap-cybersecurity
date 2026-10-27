# Coding problem, 1.1.b: Malicious link and file indicator detector

**Skill:** Analyze Risk · **Maps to:** 1.1.A, 1.1.C · **Language:** Python 3 (pytest)

## Problem
Build the analyzer a phishing-awareness tool would use to flag suspicious URLs and filenames.
Given a single string that is either a URL or a filename, return which malicious indicators
it exhibits.

Four indicator categories are defined:

- `"lookalike-domain"`, the URL hostname resembles a known brand but is not the real domain
  (typosquatting rules defined in `interface.md`)
- `"ip-url"`, the URL uses a raw IPv4 address as its host instead of a domain name
- `"dangerous-extension"`, the filename (or URL path) ends in an executable or script extension
- `"mismatched-link"`, the URL contains a brand keyword in a path or subdomain while the
  actual registrable domain belongs to a different host (defined precisely in `interface.md`)

## Function contract
Implement `solve(url_or_filename: str) -> list[str]` in `starter.py`
(see `interface.md` / `blackbox.yaml`).

Return the detected indicator labels as a **sorted, de-duplicated** list.

## Input
A single string, either a URL (starting with `http://` or `https://`) or a bare filename.

## Output
A sorted list of zero or more indicator labels drawn from
`{"dangerous-extension", "ip-url", "lookalike-domain", "mismatched-link"}`.

## Examples
```
"http://paypa1.com/verify"                  -> ["lookalike-domain"]
"http://192.168.4.99/reset"                 -> ["ip-url"]
"invoice.pdf.exe"                           -> ["dangerous-extension"]
"http://bankofamerica.com.secure-login.xyz" -> ["lookalike-domain", "mismatched-link"]
"http://shop.example/track/44821"           -> []
"http://dropbx.com/s/Q3.scr"               -> ["dangerous-extension", "lookalike-domain"]
```

## Constraints
- Deterministic, offline, standard library only.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
