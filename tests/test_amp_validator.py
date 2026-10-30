"""Tests for AMP validator utility."""

import pytest
from scripts.amp_validator import validate_amp_blogger_content, MANDATORY_DISCLAIMER_KEYWORD


def test_valid_amp_content():
    content = f"""
    <article class="post">
        <h2>Zed Editor Review</h2>
        <p>A fast editor written in Rust.</p>
        <amp-img src="https://example.com/zed.webp" width="1280" height="720" layout="responsive" alt="Zed UI"></amp-img>
        <p>{MANDATORY_DISCLAIMER_KEYWORD} This content is not sponsored.</p>
    </article>
    """
    is_valid, errors = validate_amp_blogger_content(content)
    assert is_valid is True
    assert len(errors) == 0


def test_reject_img_tag():
    content = f"""
    <article>
        <h2>Test</h2>
        <img src="https://example.com/bad.png" alt="bad image">
        <p>{MANDATORY_DISCLAIMER_KEYWORD}</p>
    </article>
    """
    is_valid, errors = validate_amp_blogger_content(content)
    assert is_valid is False
    assert any("Forbidden tag detected: <img>" in e for e in errors)


def test_reject_script_tag():
    content = f"""
    <article>
        <h2>Test</h2>
        <script>alert(1);</script>
        <p>{MANDATORY_DISCLAIMER_KEYWORD}</p>
    </article>
    """
    is_valid, errors = validate_amp_blogger_content(content)
    assert is_valid is False
    assert any("Forbidden tag detected: <script>" in e for e in errors)


def test_reject_inline_event_handlers():
    content = f"""
    <article>
        <button onclick="doSomething()">Click</button>
        <p>{MANDATORY_DISCLAIMER_KEYWORD}</p>
    </article>
    """
    is_valid, errors = validate_amp_blogger_content(content)
    assert is_valid is False
    assert any("Forbidden inline event handler" in e for e in errors)


def test_missing_disclaimer():
    content = """
    <article>
        <h2>Missing Disclaimer</h2>
        <p>Review content without disclaimer.</p>
    </article>
    """
    is_valid, errors = validate_amp_blogger_content(content)
    assert is_valid is False
    assert any("Missing mandatory non-sponsorship disclaimer" in e for e in errors)


def test_amp_img_missing_dimensions():
    content = f"""
    <article>
        <amp-img src="test.png" layout="responsive"></amp-img>
        <p>{MANDATORY_DISCLAIMER_KEYWORD}</p>
    </article>
    """
    is_valid, errors = validate_amp_blogger_content(content)
    assert is_valid is False
    assert any("missing explicit width or height" in e for e in errors)
