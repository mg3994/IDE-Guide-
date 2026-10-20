import pytest
from scripts.amp_validator import validate_amp_html, REQUIRED_DISCLAIMER

def test_valid_amp_html():
    valid_html = f"""<!doctype html>
<html amp lang="en">
<head>
  <meta charset="utf-8">
  <title>Test Post</title>
  <link rel="canonical" href="https://example.com/test.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{visibility:visible}}</style>
  <style amp-custom>body{{color:#000}}</style>
</head>
<body>
  <h1>Test Title</h1>
  <amp-img src="https://example.com/image.jpg" width="600" height="400" layout="responsive"></amp-img>
  <p>{REQUIRED_DISCLAIMER}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(valid_html)
    assert is_valid is True
    assert len(errors) == 0

def test_invalid_amp_missing_amp_attribute():
    invalid_html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Test Post</title>
  <link rel="canonical" href="https://example.com/test.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{visibility:visible}}</style>
  <style amp-custom>body{{color:#000}}</style>
</head>
<body>
  <p>{REQUIRED_DISCLAIMER}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("Missing '<html ⚡>' or '<html amp>' root tag" in err for err in errors)

def test_invalid_amp_forbidden_img_tag():
    invalid_html = f"""<!doctype html>
<html amp lang="en">
<head>
  <meta charset="utf-8">
  <title>Test Post</title>
  <link rel="canonical" href="https://example.com/test.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{visibility:visible}}</style>
  <style amp-custom>body{{color:#000}}</style>
</head>
<body>
  <img src="https://example.com/pic.png" alt="Standard Img">
  <p>{REQUIRED_DISCLAIMER}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("Found standard <img> tag" in err for err in errors)

def test_invalid_amp_missing_disclaimer():
    invalid_html = """<!doctype html>
<html amp lang="en">
<head>
  <meta charset="utf-8">
  <title>Test Post</title>
  <link rel="canonical" href="https://example.com/test.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{visibility:visible}</style>
  <style amp-custom>body{color:#000}</style>
</head>
<body>
  <p>No disclaimer here.</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("Missing required non-sponsorship disclaimer" in err for err in errors)
