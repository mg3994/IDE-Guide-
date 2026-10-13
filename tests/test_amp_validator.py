import pytest
import os
from scripts.amp_validator import validate_amp_html, REQUIRED_DISCLAIMER

def test_amp_validator_valid_html():
    valid_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>Test Page</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/p/test.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{animation:none}}</style>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-custom>body {{ color: red; }}</style>
</head>
<body>
  <p>{REQUIRED_DISCLAIMER}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(valid_html)
    assert is_valid, f"Expected valid AMP HTML but got errors: {errors}"
    assert len(errors) == 0

def test_amp_validator_invalid_html():
    invalid_html = """<html>
<head><title>No AMP</title></head>
<body><img src="test.jpg"><iframe src="test"></iframe></body>
</html>"""
    is_valid, errors = validate_amp_html(invalid_html)
    assert not is_valid
    assert len(errors) > 0
    assert any("doctype" in err.lower() for err in errors)
    assert any("disclaimer" in err.lower() for err in errors)
    assert any("img" in err.lower() for err in errors)
