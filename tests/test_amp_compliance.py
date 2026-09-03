import pytest
import re
from scripts.ide_guide_agent_skill import DISCLAIMER_TEXT, get_ide_info, generate_amp_html


def test_amp_html_structure():
    info = get_ide_info(ide_name="Cursor")
    html = generate_amp_html(info)

    # 1. Doctype
    assert re.search(r"<!doctype html>", html, re.IGNORECASE)

    # 2. AMP HTML tag
    assert "<html ⚡" in html or "<html amp" in html

    # 3. Required AMP JS Library
    assert 'src="https://cdn.ampproject.org/v0.js"' in html

    # 4. Canonical link
    assert '<link rel="canonical"' in html

    # 5. AMP Boilerplate
    assert "<style amp-boilerplate>" in html

    # 6. Inline Custom CSS
    assert "<style amp-custom>" in html

    # 7. Pricing, Pros, Cons, Verdict sections
    assert "Pricing Structure:" in html
    assert "Key Strengths" in html
    assert "Limitations" in html
    assert "Recommendation" in html

    # 8. Mandatory Non-Sponsorship Disclaimer
    assert DISCLAIMER_TEXT in html
