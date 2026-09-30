import os
import pytest
from scripts.amp_validator import validate_amp_html, REQUIRED_DISCLAIMER

def test_valid_amp_html():
    valid_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>Test Post</title>
</head>
<body>
  <amp-img src="test.jpg" width="800" height="400" layout="responsive" alt="Test"></amp-img>
  <p>{REQUIRED_DISCLAIMER}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(valid_html)
    assert is_valid is True
    assert len(errors) == 0

def test_invalid_img_tag():
    invalid_html = f"""<html>
<body>
  <img src="test.jpg" alt="test">
  <p>{REQUIRED_DISCLAIMER}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any(" forbidden <img> tag" in err for err in errors)

def test_missing_disclaimer():
    invalid_html = """<!doctype html>
<html ⚡ lang="en">
<body>
  <amp-img src="test.jpg" width="800" height="400" layout="responsive" alt="Test"></amp-img>
</body>
</html>"""
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("Missing required exact non-sponsorship disclaimer" in err for err in errors)
