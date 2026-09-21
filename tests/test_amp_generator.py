"""Tests for AMP HTML Generator module."""

from scripts.lib.amp_generator import generate_amp_html, DISCLAIMER_TEXT


def test_generate_amp_html_contains_required_amp_tags():
    sample_ide = {
        "name": "Cursor",
        "tagline": "AI Code Editor",
        "description": "An AI-first code editor",
        "pricing_type": "Freemium",
        "pricing_details": "Free tier with $20/mo pro plan",
        "features": ["AI Completion", "Multi-file edit"],
        "pros": ["Fast", "Smart"],
        "cons": ["Requires internet"],
        "best_for": "AI enthusiast developers"
    }
    html = generate_amp_html(sample_ide)

    # AMP HTML mandatory elements check
    assert "<html ⚡ lang=\"en\">" in html or "<html amp lang=\"en\">" in html
    assert "https://cdn.ampproject.org/v0.js" in html
    assert "<style amp-boilerplate>" in html
    assert "<style amp-custom>" in html
    assert "Cursor" in html
    assert DISCLAIMER_TEXT in html


def test_generate_amp_html_handles_missing_fields_gracefully():
    html = generate_amp_html({})
    assert "Unknown IDE" in html
    assert DISCLAIMER_TEXT in html
