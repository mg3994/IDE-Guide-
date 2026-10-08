import pytest
from scripts.amp_validator import validate_amp_html, MANDATORY_DISCLAIMER


def test_valid_amp_html():
    valid_html = f"""
    <article>
        <h1>VS Code Review</h1>
        <amp-img src="https://example.com/editor.png" width="800" height="450" layout="responsive" alt="Editor"></amp-img>
        <p>Key features and pros.</p>
        <p>{MANDATORY_DISCLAIMER}</p>
    </article>
    """
    is_valid, errors = validate_amp_html(valid_html)
    assert is_valid is True
    assert len(errors) == 0


def test_missing_disclaimer():
    invalid_html = """
    <article>
        <h1>VS Code Review</h1>
        <amp-img src="https://example.com/editor.png" width="800" height="450" layout="responsive" alt="Editor"></amp-img>
    </article>
    """
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("Missing or modified mandatory non-sponsorship disclaimer" in err for err in errors)


def test_forbidden_img_tag():
    invalid_html = f"""
    <article>
        <h1>VS Code Review</h1>
        <img src="https://example.com/editor.png" alt="Editor">
        <p>{MANDATORY_DISCLAIMER}</p>
    </article>
    """
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("Forbidden <img> tag found" in err for err in errors)


def test_forbidden_inline_style():
    invalid_html = f"""
    <article>
        <h1 style="color: red;">VS Code Review</h1>
        <p>{MANDATORY_DISCLAIMER}</p>
    </article>
    """
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("Forbidden inline style attribute found" in err for err in errors)


def test_amp_img_missing_dimensions():
    invalid_html = f"""
    <article>
        <h1>VS Code Review</h1>
        <amp-img src="https://example.com/editor.png" alt="Editor"></amp-img>
        <p>{MANDATORY_DISCLAIMER}</p>
    </article>
    """
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("missing required 'width' attribute" in err for err in errors)
    assert any("missing required 'height' attribute" in err for err in errors)
