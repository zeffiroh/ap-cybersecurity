"""Reference solution for 1.1.c. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
import re
from typing import List

# --- indicator data -----------------------------------------------------------

_LOOKALIKE_FRAGMENTS = [
    "paypa1", "pay-pal", "paypall",
    "amaz0n", "amazzon", "amazon-security",
    "g00gle", "go0gle", "googie",
    "micros0ft", "microsooft", "micosoft",
    "app1e", "appie", "app-le",
    "netfl1x", "netf1ix",
    "secure-login", "account-secure", "account-update", "login-secure",
    "verify-account", "update-billing",
]

_MONEY_PHRASES = [
    "wire transfer", "wire $", "send money", "transfer funds", "pay now",
    "gift card", "buy gift cards", "purchase gift cards", "send gift card",
    "urgent payment", "immediate payment", "send funds", "money transfer",
]

_CRED_PHRASES = [
    "verify your account", "confirm your password", "enter your password",
    "reset your password", "update your payment", "enter your credit card",
    "provide your ssn", "confirm your identity", "verify your identity",
    "enter your login", "sign in to verify", "log in to verify",
    "confirm your email", "verify your email", "account verification required",
]

_BRANDS = [
    "paypal", "amazon", "google", "microsoft", "apple", "netflix",
    "facebook", "instagram", "twitter", "linkedin", "irs",
    "social security", "bank of america", "wells fargo", "chase", "citibank",
]

_SHORTENER_HOSTS = [
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd",
    "buff.ly", "short.io", "rb.gy", "cutt.ly", "tiny.cc",
]

_IP_URL_RE = re.compile(r"https?://\d+\.\d+\.\d+\.\d+")


# --- indicator checks ---------------------------------------------------------

def _check_lookalike(sender_low: str) -> bool:
    return any(frag in sender_low for frag in _LOOKALIKE_FRAGMENTS)


def _check_urgent_money(text_low: str) -> bool:
    return any(phrase in text_low for phrase in _MONEY_PHRASES)


def _check_credential(text_low: str) -> bool:
    return any(phrase in text_low for phrase in _CRED_PHRASES)


def _check_mismatched_sender(sender_low: str, text_low: str) -> bool:
    brands_in_text = [b for b in _BRANDS if b in text_low]
    if not brands_in_text:
        return False
    # sender must contain at least one of those brand names
    return not any(b in sender_low for b in brands_in_text)


def _check_shortened_link(link_low: str) -> bool:
    if not link_low:
        return False
    if any(host in link_low for host in _SHORTENER_HOSTS):
        return True
    if _IP_URL_RE.search(link_low):
        return True
    return False


# --- public entry point -------------------------------------------------------

def solve(message: dict) -> List[str]:
    """Return sorted, de-duplicated phishing indicator labels for `message`.

    Args:
        message: dict with keys channel, sender, text, link (all strings).
    Returns:
        Sorted list of triggered indicator label strings (may be empty).
    """
    sender_low = (message.get("sender") or "").lower()
    text_low = (message.get("text") or "").lower()
    link_low = (message.get("link") or "").lower()

    found = set()
    if _check_lookalike(sender_low):
        found.add("lookalike-domain")
    if _check_urgent_money(text_low):
        found.add("urgent-money-request")
    if _check_credential(text_low):
        found.add("credential-request")
    if _check_mismatched_sender(sender_low, text_low):
        found.add("mismatched-sender")
    if _check_shortened_link(link_low):
        found.add("shortened-link")
    return sorted(found)
