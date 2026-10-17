import pytest
from scripts.amp_validator import validate_amp_html, DISCLAIMER_TEXT

def test_valid_amp_html():
    valid_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{visibility:visible}}</style>
  <style amp-custom>body {{ color: red; }}</style>
</head>
<body>
  <p>Hello world</p>
  <p>{DISCLAIMER_TEXT}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(valid_html)
    assert is_valid is True
    assert len(errors) == 0

def test_missing_amp_attribute():
    invalid_html = f"""<!doctype html>
<html>
<head>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{visibility:visible}}</style>
  <style amp-custom>body {{ color: red; }}</style>
</head>
<body><p>{DISCLAIMER_TEXT}</p></body>
</html>"""
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("Missing `<html ⚡>` or `<html amp>`" in err for err in errors)

def test_disallowed_img_tag():
    invalid_html = f"""<!doctype html>
<html amp lang="en">
<head>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{visibility:visible}}</style>
  <style amp-custom>body {{ color: red; }}</style>
</head>
<body>
  <img src="test.jpg" alt="test">
  <p>{DISCLAIMER_TEXT}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("Disallowed <img> tag found" in err for err in errors)

def test_missing_disclaimer():
    invalid_html = """<!doctype html>
<html ⚡ lang="en">
<head>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{visibility:visible}}</style>
  <style amp-custom>body {{ color: red; }}</style>
</head>
<body><p>No disclaimer here</p></body>
</html>"""
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("Missing mandatory non-sponsorship disclaimer" in err for err in errors)
