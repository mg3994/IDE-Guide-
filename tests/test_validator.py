import pytest
from scripts.amp_validator import validate_amp_blogger_content, REQUIRED_DISCLAIMER_PHRASE

def test_amp_validator_success_case():
    valid_html = f"""
    <div class="post">
      <h1>Test Editor Review</h1>
      <amp-img src="https://example.com/test.jpg" width="1200" height="675" layout="responsive" alt="Test image"></amp-img>
      <p>Here is an honest review of the tool.</p>
      <footer>
        {REQUIRED_DISCLAIMER_PHRASE}
      </footer>
    </div>
    """
    is_valid, errors, warnings = validate_amp_blogger_content(valid_html)
    assert is_valid is True
    assert len(errors) == 0

def test_amp_validator_forbidden_script_tag():
    invalid_html = f"""
    <div>
      <h1>Test</h1>
      <script>console.log("bad");</script>
      <p>{REQUIRED_DISCLAIMER_PHRASE}</p>
    </div>
    """
    is_valid, errors, _ = validate_amp_blogger_content(invalid_html)
    assert is_valid is False
    assert any("Forbidden tag detected: <script>" in err for err in errors)

def test_amp_validator_raw_img_forbidden():
    invalid_html = f"""
    <div>
      <h1>Test</h1>
      <img src="test.jpg" alt="test">
      <p>{REQUIRED_DISCLAIMER_PHRASE}</p>
    </div>
    """
    is_valid, errors, _ = validate_amp_blogger_content(invalid_html)
    assert is_valid is False
    assert any("Standard <img> tag is forbidden in AMP" in err for err in errors)

def test_amp_validator_missing_disclaimer():
    invalid_html = """
    <div>
      <h1>Test Editor</h1>
      <amp-img src="test.jpg" width="100" height="100" layout="responsive" alt="test"></amp-img>
      <p>Missing non-sponsorship disclosure.</p>
    </div>
    """
    is_valid, errors, _ = validate_amp_blogger_content(invalid_html)
    assert is_valid is False
    assert any("Missing required independent disclaimer" in err for err in errors)

def test_amp_validator_inline_event_handlers():
    invalid_html = f"""
    <div>
      <h1>Test</h1>
      <button onclick="alert('click')">Click me</button>
      <p>{REQUIRED_DISCLAIMER_PHRASE}</p>
    </div>
    """
    is_valid, errors, _ = validate_amp_blogger_content(invalid_html)
    assert is_valid is False
    assert any("Inline JavaScript event handler 'onclick' is forbidden" in err for err in errors)
