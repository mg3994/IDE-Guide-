import os
import glob
from scripts.generate_daily_content import (
    generate_amp_html_post,
    DEFAULT_IDE_CATALOG,
    DISCLAIMER_TEXT,
    BLOGGER_URL,
    YOUTUBE_URL
)

def test_amp_html_rules():
    sample_ide = DEFAULT_IDE_CATALOG[0]
    amp_html = generate_amp_html_post(sample_ide, post_num=1)

    # AMP validation checks
    assert "<html ⚡ lang=\"en\">" in amp_html or "<html amp lang=\"en\">" in amp_html
    assert "https://cdn.ampproject.org/v0.js" in amp_html
    assert "style amp-boilerplate" in amp_html
    assert "style amp-custom" in amp_html
    assert "<amp-img" in amp_html
    assert "layout=\"responsive\"" in amp_html
    assert DISCLAIMER_TEXT in amp_html
    assert BLOGGER_URL in amp_html
    assert YOUTUBE_URL in amp_html

def test_amp_html_no_forbidden_tags():
    sample_ide = DEFAULT_IDE_CATALOG[1]
    amp_html = generate_amp_html_post(sample_ide, post_num=2)

    # Standard <img> tag should not be used in AMP HTML, must be <amp-img>
    assert "<img " not in amp_html
    # External custom CSS link tags are restricted in AMP
    assert "<link rel=\"stylesheet\"" not in amp_html
