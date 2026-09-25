import pytest
from scripts.generate_daily_content import generate_amp_blog_post, IDE_DATABASE, DISCLAIMER_TEXT
from scripts.ide_guide_agent_skill import validate_amp_html


def test_amp_html_formatting():
    test_ide = IDE_DATABASE[0]
    date_str = "2026-10-15"
    html = generate_amp_blog_post(test_ide, date_str, index=1)

    # 1. AMP Boileplate and JS runtime imports
    assert '<script async src="https://cdn.ampproject.org/v0.js"></script>' in html
    assert '<style amp-boilerplate>' in html
    assert '<style amp-custom>' in html
    assert '<html ⚡ lang="en">' in html

    # 2. Strict amp-img enforcement
    assert '<amp-img ' in html
    assert '<img ' not in html

    # 3. Required Blogger and YouTube channel links
    assert 'https://ideguide.blogspot.com/' in html
    assert 'https://www.youtube.com/@IDEguide' in html

    # 4. Mandatory non-sponsorship disclaimer
    assert DISCLAIMER_TEXT in html

    # 5. Full validation check
    assert validate_amp_html(html) is True


def test_amp_disclaimer_presence_in_all_ides():
    date_str = "2026-10-15"
    for ide in IDE_DATABASE:
        html = generate_amp_blog_post(ide, date_str, index=1)
        assert DISCLAIMER_TEXT in html
        assert ide["name"] in html
        assert ide["pricing"] in html
