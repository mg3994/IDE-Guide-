import pytest
from scripts.amp_validator import validate_amp_html, REQUIRED_DISCLAIMER


def test_valid_amp_html():
    valid_html = f"""<!DOCTYPE html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-custom>p {{ color: #333; }}</style>
  <style amp-boilerplate>body {{ opacity: 1; }}</style>
</head>
<body>
  <h1>Valid Test</h1>
  <amp-img src="https://example.com/test.jpg" width="600" height="400" layout="responsive" alt="Test image"></amp-img>
  <p>{REQUIRED_DISCLAIMER}</p>
</body>
</html>"""
    result = validate_amp_html(valid_html)
    assert result["valid"] is True
    assert len(result["errors"]) == 0


def test_missing_disclaimer_fails():
    invalid_html = """<!DOCTYPE html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-custom>p { color: #333; }</style>
</head>
<body>
  <p>No disclaimer here</p>
</body>
</html>"""
    result = validate_amp_html(invalid_html)
    assert result["valid"] is False
    assert any("disclaimer missing" in err.lower() for err in result["errors"])


def test_standard_img_tag_fails():
    invalid_html = f"""<!DOCTYPE html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-custom>p {{ color: #333; }}</style>
</head>
<body>
  <img src="https://example.com/test.jpg" alt="forbidden">
  <p>{REQUIRED_DISCLAIMER}</p>
</body>
</html>"""
    result = validate_amp_html(invalid_html)
    assert result["valid"] is False
    assert any("standard <img> tag is forbidden" in err.lower() for err in result["errors"])


def test_inline_style_fails():
    invalid_html = f"""<!DOCTYPE html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-custom>p {{ color: #333; }}</style>
</head>
<body>
  <p style="color: red;">Inline style</p>
  <p>{REQUIRED_DISCLAIMER}</p>
</body>
</html>"""
    result = validate_amp_html(invalid_html)
    assert result["valid"] is False
    assert any("inline style attribute found" in err.lower() for err in result["errors"])
