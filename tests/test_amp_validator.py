import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from ide_guide_agent_skill import validate_amp_html, DISCLAIMER_TEXT


def test_validate_amp_html_valid():
    valid_amp = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{visibility:visible}}</style>
  <style amp-custom>body {{ color: red; }}</style>
</head>
<body>
  <amp-img src="hero.jpg" width="600" height="400" layout="responsive"></amp-img>
  <p>{DISCLAIMER_TEXT}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(valid_amp)
    assert is_valid is True
    assert len(errors) == 0


def test_validate_amp_html_missing_amp_attribute():
    invalid_amp = f"""<!doctype html>
<html>
<head>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{visibility:visible}}</style>
  <style amp-custom>body {{ color: red; }}</style>
</head>
<body>
  <amp-img src="hero.jpg" width="600" height="400" layout="responsive"></amp-img>
  <p>{DISCLAIMER_TEXT}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(invalid_amp)
    assert is_valid is False
    assert any("Missing <html ⚡>" in err for err in errors)


def test_validate_amp_html_disallowed_img_tag():
    invalid_amp = f"""<!doctype html>
<html amp lang="en">
<head>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{visibility:visible}}</style>
  <style amp-custom>body {{ color: red; }}</style>
</head>
<body>
  <img src="standard.jpg" alt="standard image">
  <amp-img src="hero.jpg" width="600" height="400" layout="responsive"></amp-img>
  <p>{DISCLAIMER_TEXT}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(invalid_amp)
    assert is_valid is False
    assert any("standard <img> tag" in err for err in errors)


def test_validate_amp_html_missing_disclaimer():
    invalid_amp = """<!doctype html>
<html ⚡ lang="en">
<head>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{visibility:visible}}</style>
  <style amp-custom>body {{ color: red; }}</style>
</head>
<body>
  <amp-img src="hero.jpg" width="600" height="400" layout="responsive"></amp-img>
</body>
</html>"""
    is_valid, errors = validate_amp_html(invalid_amp)
    assert is_valid is False
    assert any("mandatory non-sponsorship disclaimer" in err for err in errors)
