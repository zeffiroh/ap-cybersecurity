# Interface, 1.1.c-phishing-indicator-extractor (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or
composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(message: dict) -> list[str]
```

## Input (`message`)
A dict with the following keys (all strings):
- `"channel"`, one of `"email"`, `"sms"`, `"dm"` (social-media direct message)
- `"sender"`, the sender address, phone number, or handle (may be empty string)
- `"text"`, the message body text (may be empty string)
- `"link"`, a URL or empty string (the primary link extracted from the message)

All keys are always present. Values are strings; none are None.

## Output (`result`)
A **sorted, de-duplicated** `list[str]` drawn from the indicator set below.
Empty list if no indicator fires.

## Indicator rules (applied in order; case-insensitive where stated)

### `"lookalike-domain"`
Fires when the sender field contains a domain (anything after `@` for email, or a
hostname-like string for other channels) where a character has been substituted with a
visually similar ASCII character or a digit, compared against a reference brand list.
Concretely: the sender (lowercased) matches the pattern `.*@?<mangled>.*` where `<mangled>`
is any of the following strings (applied via substring match on the lowercased sender):

```
paypa1, paypa1.com, pay-pal, paypall,
amaz0n, amazzon, amazon-security,
g00gle, go0gle, googIe,
micros0ft, microsooft, micosoft,
app1e, appIe, app-le,
netfl1x, netf1ix,
secure-login, account-secure, account-update, login-secure,
verify-account, update-billing
```

### `"urgent-money-request"`
Fires when the text field (lowercased) contains any of:
```
wire transfer, wire $, send money, transfer funds, pay now,
gift card, buy gift cards, purchase gift cards, send gift card,
urgent payment, immediate payment, send funds, money transfer
```

### `"credential-request"`
Fires when the text field (lowercased) contains any of:
```
verify your account, confirm your password, enter your password,
reset your password, update your payment, enter your credit card,
provide your ssn, confirm your identity, verify your identity,
enter your login, sign in to verify, log in to verify,
confirm your email, verify your email, account verification required
```

### `"mismatched-sender"`
Fires when BOTH of the following are true:
1. The text field (lowercased) contains a brand name from the reference list:
   `paypal, amazon, google, microsoft, apple, netflix, facebook, instagram, twitter,
   linkedin, irs, social security, bank of america, wells fargo, chase, citibank`
2. The sender (lowercased) does NOT contain the corresponding keyword from that same list.
   (i.e. the text claims to be from brand X but the sender address/handle does not include
   any substring that matches any name in the brand list that the text contains)
   More precisely: extract all brand names mentioned in the text; the sender must contain
   at least one of those brand names; if it contains none, fire this indicator.

### `"shortened-link"`
Fires when the link field is non-empty and the link (lowercased) contains any of the
following known shortener hostnames, OR matches the pattern of a bare IP address URL:
```
bit.ly, tinyurl.com, t.co, goo.gl, ow.ly, is.gd, buff.ly,
short.io, rb.gy, cutt.ly, tiny.cc
```
Also fires if the link matches the pattern `https?://\d+\.\d+\.\d+\.\d+` (bare IP address).

## Guarantees / rules
- Pure function, deterministic, no I/O, no network. Standard library only.
- Matching is case-insensitive (use `.lower()` on all inputs before matching).
- Output always sorted ascending (alphabetical) and de-duplicated.
- Keys `channel`, `sender`, `text`, `link` are always present; values are strings.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
