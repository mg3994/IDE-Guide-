"""
Unit tests for AMP validator utility.
"""

import pytest
from scripts.amp_validator import validate_amp_html, MANDATORY_DISCLAIMER_PHRASE

def test_valid_amp_html():
    valid_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>Test Post</title>
</head>
<body>
  <h2>Overview</h2>
  <p>Overview content.</p>
  <h2>Pros & Cons</h2>
  <p>Pros and cons details.</p>
  <h2>Pricing Model</h2>
  <p>Free / Open source.</p>
  <h2>Verdict</h2>
  <p>Final verdict.</p>
  <p>{MANDATORY_DISCLAIMER_PHRASE}</p>
</body>
</html>"""

    is_valid, errors = validate_amp_html(valid_html)
    assert is_valid is True
    assert len(errors) == 0

def test_disallowed_img_tag():
    invalid_html = f"""<!doctype html>
<html>
<body>
  <h2>Overview</h2>
  <img src="test.jpg" alt="test">
  <h2>Pros & Cons</h2>
  <h2>Pricing Model</h2>
  <h2>Verdict</h2>
  <p>{MANDATORY_DISCLAIMER_PHRASE}</p>
</body>
</html>"""

    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("Disallowed tag found" in err for err in errors)

def test_missing_disclaimer():
    invalid_html = """<!doctype html>
<html>
<body>
  <h2>Overview</h2>
  <h2>Pros & Cons</h2>
  <h2>Pricing Model</h2>
  <h2>Verdict</h2>
</body>
</html>"""

    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("Missing or modified mandatory non-sponsorship disclaimer" in err for err in errors)
