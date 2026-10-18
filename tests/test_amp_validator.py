import pytest
from scripts.amp_validator import AmpValidator, REQUIRED_DISCLAIMER

def test_valid_amp_html():
    valid_html = f"""<!doctype html>
<html amp lang="en">
<head>
  <meta charset="utf-8">
  <title>Test Page</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/test.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both}}</style>
</head>
<body>
  <h1>Test Header</h1>
  <amp-img src="https://example.com/image.jpg" width="800" height="450" layout="responsive" alt="Test"></amp-img>
  <p>{REQUIRED_DISCLAIMER}</p>
</body>
</html>"""

    validator = AmpValidator(valid_html)
    is_valid, errors, warnings = validator.validate()
    assert is_valid is True
    assert len(errors) == 0

def test_invalid_amp_html_missing_amp_attribute():
    invalid_html = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <link rel="canonical" href="https://ideguide.blogspot.com/test.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{animation:none}</style>
</head>
<body>
  <p>Test</p>
</body>
</html>"""

    validator = AmpValidator(invalid_html)
    is_valid, errors, _ = validator.validate()
    assert is_valid is False
    assert any("Missing <html ⚡> or <html amp>" in e for e in errors)

def test_forbidden_img_tag_fails_validation():
    invalid_html = f"""<!doctype html>
<html amp lang="en">
<head>
  <meta charset="utf-8">
  <link rel="canonical" href="https://ideguide.blogspot.com/test.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{animation:none}}</style>
</head>
<body>
  <img src="test.jpg" alt="Forbidden img">
  <p>{REQUIRED_DISCLAIMER}</p>
</body>
</html>"""

    validator = AmpValidator(invalid_html)
    is_valid, errors, _ = validator.validate()
    assert is_valid is False
    assert any("Forbidden <img> tags found" in e for e in errors)
