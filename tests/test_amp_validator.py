"""
Unit tests for AMP validator module.
"""

import pytest
from scripts.amp_validator import validate_amp_html, REQUIRED_DISCLAIMER


def test_valid_amp_html():
    valid_html = f"""<!doctype html>
<html amp lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <title>Test Page</title>
  <link rel="canonical" href="https://example.com/test.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{visibility:visible}}</style>
</head>
<body>
  <h1>Test Title</h1>
  <p>{REQUIRED_DISCLAIMER}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(valid_html)
    assert is_valid is True
    assert len(errors) == 0


def test_invalid_amp_html_missing_disclaimer():
    invalid_html = """<!doctype html>
<html amp lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <title>Test Page</title>
  <link rel="canonical" href="https://example.com/test.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{visibility:visible}</style>
</head>
<body>
  <h1>Test Title</h1>
</body>
</html>"""
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("disclaimer" in err.lower() for err in errors)


def test_invalid_amp_html_prohibited_img_tag():
    invalid_html = f"""<!doctype html>
<html amp lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <title>Test Page</title>
  <link rel="canonical" href="https://example.com/test.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{visibility:visible}}</style>
</head>
<body>
  <img src="test.jpg" alt="test">
  <p>{REQUIRED_DISCLAIMER}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("amp-img" in err.lower() for err in errors)
