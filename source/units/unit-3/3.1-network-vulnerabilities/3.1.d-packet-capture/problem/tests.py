"""Test suite for 3.1.d — the blackbox acceptance contract.
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


def _p(port, payload):
    return {"port": port, "payload": payload}


# ---- visible cases -------------------------------------------------------

def test_http_login_leak():
    packets = [_p(80, "POST /login HTTP/1.1\r\n\r\nuser=alice&password=Pass123!")]
    assert impl.solve(packets) == ["LEAK"]


def test_https_always_safe():
    packets = [_p(443, "password= this looks like a leak but is encrypted TLS payload")]
    assert impl.solve(packets) == ["SAFE"]


def test_telnet_password_leak():
    packets = [_p(23, "login: admin\r\nPassword: R0uterAdmin!")]
    assert impl.solve(packets) == ["LEAK"]


def test_http_no_credential_safe():
    packets = [_p(80, "GET /index.html HTTP/1.1")]
    assert impl.solve(packets) == ["SAFE"]


def test_ftp_pass_leak():
    packets = [_p(21, "USER backup\r\nPASS Backup#2024")]
    assert impl.solve(packets) == ["LEAK"]


def test_ssh_always_safe():
    packets = [_p(22, "SSH-2.0-OpenSSH_9.3 key exchange")]
    assert impl.solve(packets) == ["SAFE"]


def test_out_of_scope_port_safe():
    packets = [_p(53, "DNS query: mail.example A?")]
    assert impl.solve(packets) == ["SAFE"]


def test_empty_packets():
    assert impl.solve([]) == []


def test_mixed_batch_order_preserved():
    packets = [
        _p(80, "password=leaked1"),
        _p(443, "password=leaked2"),
        _p(21, "PASS ftpsecret"),
    ]
    assert impl.solve(packets) == ["LEAK", "SAFE", "LEAK"]


# ---- hidden / edge cases -------------------------------------------------

def test_case_sensitivity_lowercase_pass_not_matched():
    """Lowercase 'pass ' (not the exact 'PASS ' indicator) should NOT trigger a leak."""
    packets = [_p(21, "this text says pass phrase but not the exact marker")]
    assert impl.solve(packets) == ["SAFE"]


def test_https_with_literal_password_text_still_safe():
    packets = [_p(443, "Password: totally-visible-but-port-is-encrypted")]
    assert impl.solve(packets) == ["SAFE"]


def test_multiple_indicators_still_single_leak():
    packets = [_p(80, "password=abc\r\nPassword: def\r\nPASS ghi")]
    assert impl.solve(packets) == ["LEAK"]


def test_unrelated_cleartext_port_content_safe():
    packets = [_p(23, "just some banner text, no credentials here")]
    assert impl.solve(packets) == ["SAFE"]


def test_large_batch_deterministic():
    packets = []
    expected = []
    for i in range(15):
        if i % 3 == 0:
            packets.append(_p(80, f"password=leak{i}"))
            expected.append("LEAK")
        elif i % 3 == 1:
            packets.append(_p(443, f"password=leak{i}"))
            expected.append("SAFE")
        else:
            packets.append(_p(9999, f"password=leak{i}"))
            expected.append("SAFE")
    assert impl.solve(packets) == expected
