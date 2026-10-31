import pytest
from scripts.amp_validator import validate_amp_html, MANDATORY_DISCLAIMER_SNIPPET


def test_valid_amp_html():
    valid_snippet = f"""<style amp-custom>
  .test {{ color: red; }}
</style>
<div class="test">
  <h2>Valid AMP Post</h2>
  <p>{MANDATORY_DISCLAIMER_SNIPPET}</p>
</div>"""
    is_valid, errors = validate_amp_html(valid_snippet, require_disclaimer=True)
    assert is_valid is True
    assert len(errors) == 0


def test_disallowed_script_tag():
    bad_snippet = f"""<div class="test">
  <script src="https://evil.com/tracker.js"></script>
  <p>{MANDATORY_DISCLAIMER_SNIPPET}</p>
</div>"""
    is_valid, errors = validate_amp_html(bad_snippet, require_disclaimer=True)
    assert is_valid is False
    assert any("Disallowed tag detected" in err for err in errors)


def test_disallowed_inline_style():
    bad_snippet = f"""<div class="test" style="color: blue;">
  <p>{MANDATORY_DISCLAIMER_SNIPPET}</p>
</div>"""
    is_valid, errors = validate_amp_html(bad_snippet, require_disclaimer=True)
    assert is_valid is False
    assert any("Disallowed inline attribute found" in err for err in errors)


def test_missing_disclaimer():
    snippet = """<div class="test">
  <h2>Post Without Disclaimer</h2>
  <p>Some review content.</p>
</div>"""
    is_valid, errors = validate_amp_html(snippet, require_disclaimer=True)
    assert is_valid is False
    assert any("Mandatory non-sponsorship disclaimer is missing" in err for err in errors)


def test_amp_img_validation():
    img_valid = f"""<div>
  <amp-img src="test.jpg" width="600" height="400" layout="responsive" alt="Editor Screenshot"></amp-img>
  <p>{MANDATORY_DISCLAIMER_SNIPPET}</p>
</div>"""
    is_valid, errors = validate_amp_html(img_valid, require_disclaimer=True)
    assert is_valid is True

    img_invalid = f"""<div>
  <amp-img src="test.jpg" layout="responsive"></amp-img>
  <p>{MANDATORY_DISCLAIMER_SNIPPET}</p>
</div>"""
    is_valid, errors = validate_amp_html(img_invalid, require_disclaimer=True)
    assert is_valid is False
    assert any("missing required width/height" in err for err in errors)
