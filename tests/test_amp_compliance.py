import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from generate_daily_content import DISCLAIMER, generate_amp_html_post, CURATED_IDES

def test_amp_boilerplate_and_doctype():
    ide = CURATED_IDES[0]
    html = generate_amp_html_post(ide, "2026-09-08")

    assert "<!doctype html>" in html.lower() or "<!doctype html>" in html
    assert '<html ⚡ lang="en">' in html
    assert 'amp-boilerplate' in html
    assert 'https://cdn.ampproject.org/v0.js' in html

def test_amp_custom_css_restrictions():
    ide = CURATED_IDES[0]
    html = generate_amp_html_post(ide, "2026-09-08")

    assert "<style amp-custom>" in html
    assert "!important" not in html

def test_amp_disclaimer_presence():
    ide = CURATED_IDES[0]
    html = generate_amp_html_post(ide, "2026-09-08")

    assert DISCLAIMER in html
