"""Test suite for 1.1.c — the blackbox acceptance contract.
Imports the implementation under test via IMPL env var so the SAME tests grade:
  - solution.py   (reference, must be green)
  - starter.py    (must be red until completed)
Default target is solution.py.
"""
import importlib.util
import os
import pathlib

_HERE = pathlib.Path(__file__).parent
_TARGET = os.environ.get("IMPL", str(_HERE / "solution.py"))


def _load(path):
    spec = importlib.util.spec_from_file_location("impl", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


impl = _load(_TARGET)


# ---- visible cases -----------------------------------------------------------

def test_lookalike_domain_email():
    msg = {
        "channel": "email",
        "sender": "support@paypa1.com",
        "text": "Please log in to review your account.",
        "link": "",
    }
    result = impl.solve(msg)
    assert "lookalike-domain" in result


def test_urgent_money_request_wire():
    msg = {
        "channel": "email",
        "sender": "ceo@corp-executive.net",
        "text": "Wire $50,000 today. Do not loop in finance. Keep this confidential.",
        "link": "",
    }
    result = impl.solve(msg)
    assert result == ["urgent-money-request"]


def test_credential_request_verify():
    msg = {
        "channel": "sms",
        "sender": "ALERTS",
        "text": "Your account has been locked. Verify your account to restore access.",
        "link": "",
    }
    result = impl.solve(msg)
    assert "credential-request" in result


def test_shortened_link_bitly():
    msg = {
        "channel": "dm",
        "sender": "@helpdesk_official",
        "text": "Click here to claim your reward.",
        "link": "https://bit.ly/3xAmPle",
    }
    result = impl.solve(msg)
    assert "shortened-link" in result


def test_no_indicators_legit():
    msg = {
        "channel": "sms",
        "sender": "+1-555-0192",
        "text": "Reminder: dentist appointment at 2pm tomorrow. Reply YES to confirm.",
        "link": "",
    }
    assert impl.solve(msg) == []


def test_multiple_indicators():
    # lookalike-domain + credential-request + mismatched-sender
    msg = {
        "channel": "email",
        "sender": "security@paypa1.com",
        "text": "Verify your account to keep your PayPal access active.",
        "link": "",
    }
    result = impl.solve(msg)
    assert "lookalike-domain" in result
    assert "credential-request" in result
    # result must be sorted
    assert result == sorted(result)


# ---- hidden / edge cases -----------------------------------------------------

def test_ip_address_link():
    msg = {
        "channel": "email",
        "sender": "noreply@example.com",
        "text": "Click to verify your identity.",
        "link": "http://192.168.10.5/login",
    }
    result = impl.solve(msg)
    assert "shortened-link" in result
    assert "credential-request" in result


def test_mismatched_sender_fires():
    # Text claims to be Netflix but sender has no netflix in it
    msg = {
        "channel": "email",
        "sender": "billing@stream-updates.net",
        "text": "Your Netflix subscription has been suspended.",
        "link": "",
    }
    result = impl.solve(msg)
    assert "mismatched-sender" in result


def test_mismatched_sender_does_not_fire_when_match():
    # Sender legitimately contains the brand name
    msg = {
        "channel": "email",
        "sender": "no-reply@netflix.com",
        "text": "Your Netflix payment is due.",
        "link": "",
    }
    result = impl.solve(msg)
    assert "mismatched-sender" not in result


def test_gift_card_scam():
    msg = {
        "channel": "email",
        "sender": "boss@company.org",
        "text": "Can you buy gift cards for me? I need them urgently.",
        "link": "",
    }
    result = impl.solve(msg)
    assert "urgent-money-request" in result


def test_empty_message():
    msg = {
        "channel": "email",
        "sender": "",
        "text": "",
        "link": "",
    }
    assert impl.solve(msg) == []


def test_output_sorted_and_deduped():
    msg = {
        "channel": "sms",
        "sender": "amaz0n-security",
        "text": "Verify your Amazon account. Wire $100 to confirm.",
        "link": "https://tinyurl.com/abc123",
    }
    result = impl.solve(msg)
    # No duplicates
    assert len(result) == len(set(result))
    # Sorted ascending
    assert result == sorted(result)
    # Must include at least these
    assert "lookalike-domain" in result
    assert "urgent-money-request" in result
    assert "shortened-link" in result


def test_case_insensitive_text():
    msg = {
        "channel": "email",
        "sender": "alerts@bank.com",
        "text": "VERIFY YOUR ACCOUNT to avoid suspension.",
        "link": "",
    }
    result = impl.solve(msg)
    assert "credential-request" in result


def test_tinyurl_shortener():
    msg = {
        "channel": "dm",
        "sender": "@random_user",
        "text": "Check out this deal.",
        "link": "https://tinyurl.com/deal99",
    }
    result = impl.solve(msg)
    assert "shortened-link" in result


def test_no_false_positive_on_brand_in_sender():
    # Sender is paypal.com — mismatched-sender should NOT fire
    msg = {
        "channel": "email",
        "sender": "service@paypal.com",
        "text": "Your PayPal transaction was completed.",
        "link": "",
    }
    result = impl.solve(msg)
    assert "mismatched-sender" not in result
