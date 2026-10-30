import html
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


def test_plain_comment_renders():
    out = impl.render_comment("jordan", "Nice, clear write-up")
    assert "jordan" in out
    assert "Nice, clear write-up" in out


def test_structural_tags_present():
    out = impl.render_comment("jordan", "hello")
    assert '<div class="c">' in out
    assert "<b>" in out and "</b>" in out and "</div>" in out


def test_script_payload_encoded():
    out = impl.render_comment("jordan", "<script>steal()</script>")
    assert "<script>" not in out
    assert "&lt;script&gt;" in out


def test_img_onerror_payload_encoded():
    out = impl.render_comment("jordan", '<img src=x onerror=steal()>')
    assert "<img" not in out
    assert "&lt;img" in out


def test_malicious_username_encoded():
    out = impl.render_comment("<script>evil()</script>", "hi")
    assert "<script>" not in out
    assert "&lt;script&gt;" in out


def test_quotes_and_ampersand_encoded():
    out = impl.render_comment("jordan", 'a "b" \'c\' & d')
    assert "&quot;" in out
    assert "&#x27;" in out
    assert "&amp;" in out


def test_user_value_encoded_exactly():
    payload = '"><svg/onload=steal()>&\''
    out = impl.render_comment("jordan", payload)
    assert html.escape(payload, quote=True) in out
    assert payload not in out


def test_ampersand_not_double_or_raw():
    out = impl.render_comment("a&b", "c")
    assert "&amp;" in out
