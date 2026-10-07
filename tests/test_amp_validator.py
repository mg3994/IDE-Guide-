import pytest
from scripts.amp_validator import validate_amp_html, DISCLAIMER_TEXT

def test_valid_amp_html():
    valid_html = f"""<!doctype html>
<html amp lang="en">
<head>
  <meta charset="utf-8">
  <title>Test Page</title>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{visibility:visible}}</style>
  <style amp-custom>p {{ color: red; }}</style>
</head>
<body>
  <p>{DISCLAIMER_TEXT}</p>
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
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{visibility:visible}}</style>
  <style amp-custom>p { color: red; }</style>
</head>
<body>
  <p>Some post without disclaimer</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("disclaimer" in err.lower() for err in errors)

def test_invalid_amp_html_disallowed_tag():
    invalid_html = f"""<!doctype html>
<html amp lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{visibility:visible}}</style>
  <style amp-custom>p {{ color: red; }}</style>
</head>
<body>
  <img src="test.jpg" alt="test">
  <p>{DISCLAIMER_TEXT}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("disallowed" in err.lower() for err in errors)
