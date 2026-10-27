"""Reference solution for 1.1.b. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
import re
from typing import List
from urllib.parse import urlparse

# --- constants from interface.md ---

LOOKALIKE_DOMAINS = {
    "paypa1.com", "arnazon.com", "dropbx.com", "g00gle.com", "faceb00k.com",
    "rn1crosoft.com", "rnicrosott.com", "rnicrosoft.com", "linkedln.com",
    "app1e.com", "twiitter.com", "lnstagram.com",
}

DANGEROUS_EXTENSIONS = {
    ".exe", ".scr", ".bat", ".cmd", ".ps1", ".vbs", ".vbe", ".js", ".jse",
    ".wsf", ".wsh", ".jar", ".pif", ".com", ".hta", ".msi", ".dll", ".cpl", ".reg",
}

TRUSTED_DOMAINS = {
    "paypal.com", "amazon.com", "dropbox.com", "google.com", "facebook.com",
    "microsoft.com", "linkedin.com", "apple.com", "twitter.com", "instagram.com",
    "bankofamerica.com", "chase.com", "wellsfargo.com", "company.example",
    "shop.example", "meridian-corp.example",
}

TRUSTED_BRANDS = [
    "paypal", "amazon", "dropbox", "google", "facebook", "microsoft", "linkedin",
    "apple", "twitter", "instagram", "bankofamerica", "chase", "wellsfargo",
]

_IP_RE = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?$')


def _registrable_domain(hostname: str) -> str:
    """Return last two labels of a hostname, lowercased (e.g. 'evil.net' from 'foo.evil.net')."""
    parts = hostname.lower().split(".")
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return hostname.lower()


def _final_extension(s: str) -> str:
    """Return the final dot-extension of a string (path segment or filename), lowercased."""
    # take the last path segment
    segment = s.rstrip("/").split("/")[-1].split("?")[0].split("#")[0]
    dot_idx = segment.rfind(".")
    if dot_idx == -1:
        return ""
    return segment[dot_idx:].lower()


def solve(url_or_filename: str) -> List[str]:
    """Return sorted, de-duplicated malicious indicators present in url_or_filename."""
    s = url_or_filename or ""
    found = set()
    is_url = s.lower().startswith("http://") or s.lower().startswith("https://")

    if is_url:
        parsed = urlparse(s)
        hostname = parsed.hostname or ""
        reg_domain = _registrable_domain(hostname)

        # ip-url
        if _IP_RE.match(parsed.netloc.lower()):
            found.add("ip-url")

        # lookalike-domain
        if reg_domain in LOOKALIKE_DOMAINS:
            found.add("lookalike-domain")

        # mismatched-link: not a trusted domain, but URL contains a trusted brand keyword
        if reg_domain not in TRUSTED_DOMAINS:
            url_lower = s.lower()
            # check keyword presence outside the registrable domain portion
            # strip reg_domain from the string and check remaining
            url_without_reg = url_lower.replace(reg_domain, "", 1)
            for brand in TRUSTED_BRANDS:
                if brand in url_without_reg:
                    found.add("mismatched-link")
                    break

        # dangerous-extension (from URL path)
        ext = _final_extension(parsed.path)
        if ext in DANGEROUS_EXTENSIONS:
            found.add("dangerous-extension")
    else:
        # bare filename — only dangerous-extension applies
        ext = _final_extension(s)
        if ext in DANGEROUS_EXTENSIONS:
            found.add("dangerous-extension")

    return sorted(found)
