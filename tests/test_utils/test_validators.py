import pytest
from app.utils import validators

# test: duplicate email registration
def test_validate_valid_email():
    assert validators.validate_email("user@example.com") is True

def test_validate_invalid_email_no_at_symbol():
    assert validators.validate_email("userexample.com") is False

def test_validate_invalid_email_no_domain():
    assert validators.validate_email("user@") is False

def test_validate_valid_url_http():
    assert validators.validate_url("http://example.com") is True

def test_validate_valid_url_https():
    assert validators.validate_url("https://example.com") is True

def test_validate_invalid_url_ftp():
    assert validators.validate_url("ftp://example.com") is False

def test_validate_invalid_url_missing_protocol():
    assert validators.validate_url("example.com") is False

def test_validate_blank_email():
    assert validators.validate_email("") is False

def test_validate_blank_url():
    assert validators.validate_url("") is False

def test_validate_url_with_path():
    assert validators.validate_url("https://example.com/path/to/resource") is True
