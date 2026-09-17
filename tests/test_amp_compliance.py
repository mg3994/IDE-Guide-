import os
import sys
import re
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from generate_daily_content import generate_amp_blog_html, CURATED_IDE_DATABASE, MANDATORY_DISCLAIMER

def test_amp_html_structure():
    sample_ide = CURATED_IDE_DATABASE[0]
    html = generate_amp_blog_html(sample_ide, "2026-03-30")

    # 1. Doctype
    assert re.search(r'<!doctype html>', html, re.IGNORECASE)

    # 2. <html ⚡> or <html amp>
    assert re.search(r'<html\s+(⚡|amp)[\s>]', html, re.IGNORECASE)

    # 3. AMP runtime script v0.js
    assert 'https://cdn.ampproject.org/v0.js' in html

    # 4. Canonical tag
    assert '<link rel="canonical"' in html

    # 5. Viewport meta
    assert 'name="viewport"' in html

    # 6. AMP boilerplate
    assert 'style amp-boilerplate' in html

    # 7. Custom style tag
    assert '<style amp-custom>' in html

    # 8. Schema.org JSON-LD structured data
    assert 'application/ld+json' in html
    assert '"@type": "BlogPosting"' in html

    # 9. Non-sponsorship disclaimer
    assert MANDATORY_DISCLAIMER in html
