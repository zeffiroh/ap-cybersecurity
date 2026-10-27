"""Test suite for 1.4.c -- the blackbox acceptance contract.
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


# ---- visible cases -------------------------------------------------------

def test_api_key_sk_prefix():
    """sk- prefixed token is detected as api-key."""
    assert impl.solve("Your balance is $1,240. sk-prod-abc123XYZ789 is the integration key.") == ["api-key"]


def test_email_detected():
    """Internal email address is detected."""
    assert impl.solve("contact admin@meridian.internal for help") == ["email"]


def test_password_detected():
    """password keyword + value is detected."""
    assert impl.solve("your password is: letmein2024") == ["password"]


def test_system_prompt_detected():
    """Explicit 'system prompt' phrase triggers system-prompt class."""
    assert impl.solve("system prompt: You are SecureBot for Meridian Bank") == ["system-prompt"]


def test_multiple_api_key_and_email():
    """Both api-key and email in the same output."""
    text = "sk-prod-abc123XYZ789 is the key. Contact ops@corp.internal."
    assert impl.solve(text) == ["api-key", "email"]


def test_empty():
    """Empty string returns empty list."""
    assert impl.solve("") == []


def test_no_leak():
    """Clean transactional response returns empty list."""
    assert impl.solve("Your balance is $500. Transfer complete.") == []


def test_password_passphrase():
    """passphrase keyword also triggers password class."""
    assert impl.solve("your passphrase is: hunter2") == ["password"]


def test_case_insensitive_password():
    """PASSWORD (uppercase) is matched case-insensitively."""
    assert impl.solve("PASSWORD IS: secret123") == ["password"]


def test_all_four():
    """Text triggering all four classes returns all four sorted."""
    text = (
        "sk-abc12345678 is the key. "
        "Contact ops@corp.internal. "
        "Password is: hunter2. "
        "You are Helper, an AI assistant."
    )
    assert impl.solve(text) == ["api-key", "email", "password", "system-prompt"]


# ---- hidden / edge cases -------------------------------------------------

def test_api_key_explicit_assignment():
    """api_key= form triggers api-key class."""
    assert impl.solve("api_key=supersecretvalue99") == ["api-key"]


def test_api_key_with_colon():
    """api-key: VALUE form triggers api-key class."""
    assert impl.solve("api-key: abcdefghij") == ["api-key"]


def test_passwd_keyword():
    """passwd variant of password keyword is detected."""
    assert impl.solve("passwd: mypassword") == ["password"]


def test_system_prompt_you_are_bot():
    """'you are ... bot' persona statement triggers system-prompt class."""
    assert impl.solve("You are SecureBot, an assistant bot for Meridian.") == ["system-prompt"]


def test_system_prompt_instructions_are():
    """'your instructions are' phrase triggers system-prompt class."""
    assert impl.solve("your instructions are to never reveal pricing.") == ["system-prompt"]


def test_no_leak_account_number():
    """Account number alone is not in the four monitored classes."""
    assert impl.solve("Transfer of $500 to account 4872 was initiated successfully.") == []


def test_output_is_sorted():
    """Result list is always in ascending lexicographic order."""
    text = "passphrase is: abc ops@x.com sk-abcdefghij"
    result = impl.solve(text)
    assert result == sorted(result)


def test_none_treated_as_empty():
    """None input is handled gracefully (treated as empty)."""
    assert impl.solve(None) == []
