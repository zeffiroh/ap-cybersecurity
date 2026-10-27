"""Test suite for 5.4.d — the blackbox acceptance contract.
Imports the implementation under test via IMPL env var so the SAME tests grade:
  - solution.py   (reference, must be green)
  - starter.py    (must be red until completed)
Default target is solution.py.

Fixtures below are a small, hand-verified certificate chain: a root CA (self-signed), an
intermediate CA it signs, and a leaf certificate the intermediate signs. Signatures were computed
independently of any implementation using the exact rolling-hash + textbook-RSA scheme specified
in prompt.md / interface.md, so this file works as an oracle even against a from-scratch student
implementation.
"""
import copy
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

_MODULUS = (2 ** 61) - 1


def _oracle_digest(cert: dict) -> int:
    """Independent reference digest, computed the same way tests build fixtures below."""
    e, n = cert["public_key"]
    canonical = f'{cert["subject"]}|{cert["issuer"]}|{e}:{n}|{cert["not_before"]}|{cert["not_after"]}'
    h = 0
    for ch in canonical:
        h = (h * 131 + ord(ch)) % _MODULUS
    return h


# ---- fixture chain: root -> intermediate -> leaf, all hand-verified ------
ROOT_E, ROOT_N, ROOT_D = 17, 2773, 157
INT_E, INT_N, INT_D = 17, 2537, 1433
LEAF_E, LEAF_N = 17, 2501

ROOT_CERT = {
    "subject": "Meridian Root CA",
    "issuer": "Meridian Root CA",
    "public_key": [ROOT_E, ROOT_N],
    "not_before": 1000,
    "not_after": 9000,
    "revoked": False,
    "signature": 1287,  # sign(digest(ROOT_CERT), ROOT_D, ROOT_N)
}

INTERMEDIATE_CERT = {
    "subject": "Meridian Intermediate CA",
    "issuer": "Meridian Root CA",
    "public_key": [INT_E, INT_N],
    "not_before": 1000,
    "not_after": 9000,
    "revoked": False,
    "signature": 884,  # sign(digest(INTERMEDIATE_CERT), ROOT_D, ROOT_N)
}

LEAF_CERT = {
    "subject": "www.meridianbank.example",
    "issuer": "Meridian Intermediate CA",
    "public_key": [LEAF_E, LEAF_N],
    "not_before": 1000,
    "not_after": 9000,
    "revoked": False,
    "signature": 1271,  # sign(digest(LEAF_CERT), INT_D, INT_N)
}

TRUSTED_ROOTS = {"Meridian Root CA": [ROOT_E, ROOT_N]}


def _chain():
    return [copy.deepcopy(LEAF_CERT), copy.deepcopy(INTERMEDIATE_CERT), copy.deepcopy(ROOT_CERT)]


# ---- visible cases -------------------------------------------------------
def test_valid_chain_is_trusted():
    result = impl.validate_chain(_chain(), TRUSTED_ROOTS, current_time=5000)
    assert result == {"valid": True, "reason": "valid"}


def test_digest_matches_oracle():
    assert impl.compute_digest(LEAF_CERT) == _oracle_digest(LEAF_CERT)
    assert impl.compute_digest(INTERMEDIATE_CERT) == _oracle_digest(INTERMEDIATE_CERT)
    assert impl.compute_digest(ROOT_CERT) == _oracle_digest(ROOT_CERT)


def test_rsa_sign_and_verify_round_trip():
    digest = _oracle_digest(LEAF_CERT)
    sig = impl.rsa_sign(digest, INT_D, INT_N)
    assert sig == LEAF_CERT["signature"]
    assert impl.rsa_verify(digest, sig, INT_E, INT_N) is True


def test_expired_leaf_is_rejected():
    chain = _chain()
    result = impl.validate_chain(chain, TRUSTED_ROOTS, current_time=9500)
    assert result == {"valid": False, "reason": "expired"}


def test_revoked_intermediate_is_rejected():
    chain = _chain()
    chain[1]["revoked"] = True
    result = impl.validate_chain(chain, TRUSTED_ROOTS, current_time=5000)
    assert result == {"valid": False, "reason": "revoked"}


def test_solve_validate_op():
    result = impl.solve({
        "op": "validate",
        "chain": _chain(),
        "trusted_roots": TRUSTED_ROOTS,
        "current_time": 5000,
    })
    assert result == {"valid": True, "reason": "valid"}


# ---- hidden / edge cases -------------------------------------------------
def test_broken_issuer_subject_link_is_rejected():
    chain = _chain()
    chain[0]["issuer"] = "Some Other CA"  # leaf no longer names the intermediate as its issuer
    result = impl.validate_chain(chain, TRUSTED_ROOTS, current_time=5000)
    assert result == {"valid": False, "reason": "broken_chain"}


def test_untrusted_self_signed_root_is_rejected():
    chain = _chain()
    result = impl.validate_chain(chain, trusted_roots={}, current_time=5000)
    assert result == {"valid": False, "reason": "untrusted_root"}


def test_root_with_mismatched_trusted_key_is_rejected():
    chain = _chain()
    tampered_roots = {"Meridian Root CA": [ROOT_E, ROOT_N + 2]}  # wrong key on file
    result = impl.validate_chain(chain, tampered_roots, current_time=5000)
    assert result == {"valid": False, "reason": "untrusted_root"}


def test_tampered_leaf_signature_is_rejected():
    chain = _chain()
    chain[0]["signature"] = chain[0]["signature"] + 1  # one-off tamper, still same fields
    result = impl.validate_chain(chain, TRUSTED_ROOTS, current_time=5000)
    assert result == {"valid": False, "reason": "bad_signature"}


def test_tampered_leaf_subject_is_rejected_as_bad_signature():
    chain = _chain()
    chain[0]["subject"] = "www.evil.example"  # identity swapped after signing
    result = impl.validate_chain(chain, TRUSTED_ROOTS, current_time=5000)
    assert result == {"valid": False, "reason": "bad_signature"}


def test_expired_check_takes_priority_over_broken_chain():
    chain = _chain()
    chain[0]["not_after"] = 2000  # leaf expired
    chain[0]["issuer"] = "Nonexistent CA"  # ALSO broken chain -- expiry must win (checked first)
    result = impl.validate_chain(chain, TRUSTED_ROOTS, current_time=5000)
    assert result == {"valid": False, "reason": "expired"}


def test_solve_digest_op():
    result = impl.solve({"op": "digest", "cert": LEAF_CERT})
    assert result == {"digest": _oracle_digest(LEAF_CERT)}


def test_current_time_at_exact_boundaries_is_valid():
    chain = _chain()
    result_start = impl.validate_chain(chain, TRUSTED_ROOTS, current_time=1000)
    result_end = impl.validate_chain(chain, TRUSTED_ROOTS, current_time=9000)
    assert result_start == {"valid": True, "reason": "valid"}
    assert result_end == {"valid": True, "reason": "valid"}
