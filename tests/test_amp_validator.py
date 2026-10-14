import pytest
from scripts.amp_validator import validate_amp_html, REQUIRED_DISCLAIMER

def test_valid_amp_html():
    valid_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>Test Post</title>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-custom>
    body {{ background: #fff; }}
  </style>
</head>
<body>
  <h1>Test Title</h1>
  <amp-img src="test.jpg" width="600" height="400" layout="responsive"></amp-img>
  <p>{REQUIRED_DISCLAIMER}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(valid_html)
    assert is_valid is True
    assert len(errors) == 0

def test_invalid_img_tag():
    invalid_html = f"""<html><body><img src="test.jpg"><p>{REQUIRED_DISCLAIMER}</p></body></html>"""
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("<img> tag found" in e for e in errors)

def test_invalid_inline_style():
    invalid_html = f"""<html><body><div style="color:red">Test</div><p>{REQUIRED_DISCLAIMER}</p></body></html>"""
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("inline style attribute found" in e for e in errors)

def test_missing_disclaimer():
    invalid_html = "<html><body><h1>No Disclaimer Here</h1></body></html>"
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("disclaimer missing" in e for e in errors)
