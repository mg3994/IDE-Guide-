import pytest
from scripts.amp_validator import validate_amp_html, MANDATORY_DISCLAIMER


def test_valid_amp_html():
    valid_html = f"""
    <div>
        <h1>Test Post</h1>
        <amp-img src="https://example.com/img.jpg" width="800" height="450" layout="responsive" alt="Test"></amp-img>
        <p>{MANDATORY_DISCLAIMER}</p>
    </div>
    """
    is_valid, errors = validate_amp_html(valid_html)
    assert is_valid is True
    assert len(errors) == 0


def test_invalid_standard_img_tag():
    invalid_html = f"""
    <div>
        <img src="https://example.com/img.jpg" alt="Test" />
        <p>{MANDATORY_DISCLAIMER}</p>
    </div>
    """
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("Forbidden standard <img>" in e for e in errors)


def test_missing_amp_img_attributes():
    invalid_html = f"""
    <div>
        <amp-img src="https://example.com/img.jpg"></amp-img>
        <p>{MANDATORY_DISCLAIMER}</p>
    </div>
    """
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("missing 'width'" in e for e in errors)
    assert any("missing 'height'" in e for e in errors)
    assert any("missing 'layout'" in e for e in errors)


def test_missing_disclaimer():
    invalid_html = """
    <div>
        <h1>Test Post</h1>
        <amp-img src="https://example.com/img.jpg" width="800" height="450" layout="responsive" alt="Test"></amp-img>
    </div>
    """
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("Mandatory non-sponsorship disclaimer is missing" in e for e in errors)
