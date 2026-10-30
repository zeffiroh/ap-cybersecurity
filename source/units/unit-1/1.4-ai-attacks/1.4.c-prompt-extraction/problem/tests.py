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


def test_api_key_sk_prefix():
    assert impl.solve("Your balance is $1,240. sk-prod-abc123XYZ789 is the integration key.") == ["api-key"]


def test_email_detected():
    assert impl.solve("contact admin@meridian.internal for help") == ["email"]


def test_password_detected():
    assert impl.solve("your password is: letmein2024") == ["password"]


def test_system_prompt_detected():
    assert impl.solve("system prompt: You are SecureBot for Meridian Bank") == ["system-prompt"]


def test_multiple_api_key_and_email():
    text = "sk-prod-abc123XYZ789 is the key. Contact ops@corp.internal."
    assert impl.solve(text) == ["api-key", "email"]


def test_empty():
    assert impl.solve("") == []


def test_no_leak():
    assert impl.solve("Your balance is $500. Transfer complete.") == []


def test_password_passphrase():
    assert impl.solve("your passphrase is: hunter2") == ["password"]


def test_case_insensitive_password():
    assert impl.solve("PASSWORD IS: secret123") == ["password"]


def test_all_four():
    text = (
        "sk-abc12345678 is the key. "
        "Contact ops@corp.internal. "
        "Password is: hunter2. "
        "You are Helper, an AI assistant."
    )
    assert impl.solve(text) == ["api-key", "email", "password", "system-prompt"]


def test_api_key_explicit_assignment():
    assert impl.solve("api_key=supersecretvalue99") == ["api-key"]


def test_api_key_with_colon():
    assert impl.solve("api-key: abcdefghij") == ["api-key"]


def test_passwd_keyword():
    assert impl.solve("passwd: mypassword") == ["password"]


def test_system_prompt_you_are_bot():
    assert impl.solve("You are SecureBot, an assistant bot for Meridian.") == ["system-prompt"]


def test_system_prompt_instructions_are():
    assert impl.solve("your instructions are to never reveal pricing.") == ["system-prompt"]


def test_no_leak_account_number():
    assert impl.solve("Transfer of $500 to account 4872 was initiated successfully.") == []


def test_output_is_sorted():
    text = "passphrase is: abc ops@x.com sk-abcdefghij"
    result = impl.solve(text)
    assert result == sorted(result)


def test_none_treated_as_empty():
    assert impl.solve(None) == []
