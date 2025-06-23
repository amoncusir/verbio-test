import pytest
import base64

from src.module.detector.presentation.http.utils import generate_token, decode_token


def test_generate_and_decode_token_with_strings_and_ints():
    original_values = ("user123", 456, "admin", 0)
    token = generate_token(*original_values)
    decoded = decode_token(token)
    assert decoded == original_values


def test_generate_and_decode_token_with_none_values():
    original_values = ("foo", None, 123, None, "bar")
    token = generate_token(*original_values)
    decoded = decode_token(token)
    assert decoded == original_values


def test_generate_token_encoding_format():
    # Token should be valid base64
    token = generate_token("hello", 42)
    try:
        base64.urlsafe_b64decode(token.encode("utf-8"))
    except Exception:
        pytest.fail("Token is not valid base64")


def test_empty_token_encoding():
    token = generate_token()
    decoded = decode_token(token)
    assert decoded == ()


def test_generate_and_decode_token_only_ints():
    original_values = (1, 2, 3, 9999)
    token = generate_token(*original_values)
    decoded = decode_token(token)
    assert decoded == original_values


def test_generate_and_decode_token_only_strings():
    original_values = ("a", "b", "c", "z")
    token = generate_token(*original_values)
    decoded = decode_token(token)
    assert decoded == original_values


def test_roundtrip_preserves_order_and_type():
    values = ("abc", 123, None, "xyz", 0, None, 7)
    assert decode_token(generate_token(*values)) == values
