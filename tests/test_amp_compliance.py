"""
Unit tests for AMP HTML compliance of generated blog posts.
Ensures compliance with Accelerated Mobile Pages rules and mandatory disclaimers.
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.ide_guide_agent_skill import generate_amp_html, resolve_ide_data, DISCLAIMER_TEXT


def test_amp_html_structure():
    ide_data = resolve_ide_data(ide_query="Cursor IDE")
    amp_html = generate_amp_html(ide_data)

    # Check AMP doctype & html tag
    assert "<!doctype html>" in amp_html or "<!DOCTYPE html>" in amp_html
    assert '<html ⚡ lang="en">' in amp_html or '<html amp lang="en">' in amp_html

    # Check required AMP script
    assert 'src="https://cdn.ampproject.org/v0.js"' in amp_html

    # Check boilerplate styles
    assert "style amp-boilerplate" in amp_html
    assert "noscript" in amp_html

    # Check canonical link
    assert '<link rel="canonical"' in amp_html
    assert "https://ideguide.blogspot.com/" in amp_html

    # Check viewport
    assert '<meta name="viewport"' in amp_html


def test_amp_disclaimer_presence():
    ide_data = resolve_ide_data(ide_query="Zed Editor")
    amp_html = generate_amp_html(ide_data)

    assert DISCLAIMER_TEXT in amp_html
    assert "not sponsored, endorsed, or affiliated" in amp_html


def test_amp_content_sections():
    ide_data = resolve_ide_data(ide_query="Visual Studio Code")
    amp_html = generate_amp_html(ide_data)

    assert "Visual Studio Code" in amp_html
    assert "The Good (Pros & Advantages)" in amp_html
    assert "The Bad (Cons & Drawbacks)" in amp_html
    assert "Pricing:" in amp_html
    assert "Verdict & Recommendation:" in amp_html
