"""Test suite for 5.3.b — the blackbox acceptance contract.
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


# ---- wrap_key / unwrap_key -----------------------------------------------
def test_wrap_key_basic_xor():
    dek = b"\x01\x02\x03\x04"
    kek = b"\xff\x00"
    assert impl.wrap_key(dek, kek) == bytes([0x01 ^ 0xFF, 0x02 ^ 0x00, 0x03 ^ 0xFF, 0x04 ^ 0x00])


def test_wrap_unwrap_round_trip():
    dek = b"top-secret-dek-1234"
    kek = b"kekmaterial"
    wrapped = impl.wrap_key(dek, kek)
    assert wrapped != dek
    assert impl.unwrap_key(wrapped, kek) == dek


def test_wrap_key_empty_dek():
    assert impl.wrap_key(b"", b"anykek") == b""


def test_wrap_key_kek_shorter_than_dek_repeats():
    dek = b"\x00\x00\x00\x00"
    kek = b"\x01\x02"
    assert impl.wrap_key(dek, kek) == b"\x01\x02\x01\x02"


# ---- looks_like_csprng -----------------------------------------------------
def test_repeated_byte_is_weak():
    assert impl.looks_like_csprng(bytes([5] * 16)) is False


def test_arithmetic_sequence_is_weak():
    assert impl.looks_like_csprng(bytes(range(16))) is False


def test_short_repeating_pattern_is_weak():
    assert impl.looks_like_csprng(b"abab" * 4) is False


def test_too_short_is_weak():
    assert impl.looks_like_csprng(b"\x01\x02\x03") is False


def test_plausible_csprng_output_is_strong():
    assert impl.looks_like_csprng(b"\x4e\x91\x0a\xd3\x77\xbb\x02\xf8") is True


def test_another_plausible_csprng_output():
    assert impl.looks_like_csprng(bytes([0x9F, 0x02, 0x77, 0xC1, 0x3A, 0x5E, 0x00, 0xE4, 0x6B])) is True


# ---- detect_ecb_leakage -----------------------------------------------------
def test_duplicate_blocks_flagged():
    blocks = [b"AAAAAAAA", b"BBBBBBBB", b"AAAAAAAA"]
    assert impl.detect_ecb_leakage(blocks) is True


def test_all_distinct_blocks_not_flagged():
    blocks = [b"AAAAAAAA", b"BBBBBBBB", b"CCCCCCCC"]
    assert impl.detect_ecb_leakage(blocks) is False


def test_single_block_not_flagged():
    assert impl.detect_ecb_leakage([b"AAAAAAAA"]) is False


def test_empty_blocks_not_flagged():
    assert impl.detect_ecb_leakage([]) is False


def test_duplicate_at_end_of_longer_list():
    blocks = [b"11111111", b"22222222", b"33333333", b"44444444", b"22222222"]
    assert impl.detect_ecb_leakage(blocks) is True
