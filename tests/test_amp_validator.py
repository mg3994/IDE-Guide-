import pytest
from scripts.amp_validator import validate_amp_html, DISCLAIMER_TEXT

def test_valid_amp_html():
    valid_html = f"""
    <article>
      <h2>Test Post</h2>
      <p>Sample text</p>
      <amp-img src="https://example.com/test.jpg" width="600" height="400" layout="responsive"></amp-img>
      <p>{DISCLAIMER_TEXT}</p>
    </article>
    """
    is_valid, errors = validate_amp_html(valid_html)
    assert is_valid is True
    assert len(errors) == 0

def test_invalid_amp_img_tag():
    invalid_html = f"""
    <article>
      <h2>Test Post</h2>
      <img src="https://example.com/test.jpg" alt="test">
      <p>{DISCLAIMER_TEXT}</p>
    </article>
    """
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("Forbidden tag <img>" in e for e in errors)

def test_inline_style_attribute():
    invalid_html = f"""
    <article>
      <h2 style="color: red;">Test Post</h2>
      <p>{DISCLAIMER_TEXT}</p>
    </article>
    """
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("Inline style attributes" in e for e in errors)

def test_missing_disclaimer():
    invalid_html = """
    <article>
      <h2>Test Post</h2>
      <p>No disclaimer present here.</p>
    </article>
    """
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("Missing mandatory non-sponsorship disclaimer" in e for e in errors)
