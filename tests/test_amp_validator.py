import pytest
from scripts.amp_validator import validate_amp_html, REQUIRED_DISCLAIMER

def test_valid_amp_html():
    valid_html = f"""
    <style amp-custom>
      .post {{ color: #000; }}
    </style>
    <div class="post">
      <h1>VS Code Review</h1>
      <amp-img src="https://example.com/img.jpg" width="800" height="450" layout="responsive" alt="VS Code"></amp-img>
      <p>{REQUIRED_DISCLAIMER}</p>
    </div>
    """
    is_valid, errors = validate_amp_html(valid_html)
    assert is_valid is True
    assert len(errors) == 0

def test_invalid_img_tag():
    invalid_html = f"""
    <div class="post">
      <img src="https://example.com/img.jpg" alt="Invalid">
      <p>{REQUIRED_DISCLAIMER}</p>
    </div>
    """
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("img" in err.lower() for err in errors)

def test_missing_disclaimer():
    invalid_html = """
    <div class="post">
      <amp-img src="https://example.com/img.jpg" width="800" height="450" layout="responsive" alt="VS Code"></amp-img>
      <p>Missing disclaimer</p>
    </div>
    """
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("disclaimer" in err.lower() for err in errors)
