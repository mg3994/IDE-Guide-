import pytest
import os
import json
from scripts.generate_daily_content import (
    generate_amp_html,
    CURATED_IDE_CATALOG,
    DISCLAIMER_TEXT
)

def test_amp_html_structure():
    ide = CURATED_IDE_CATALOG[0]
    date_str = "2026-08-31"
    html = generate_amp_html(ide, date_str)

    assert "<!doctype html>" in html
    assert "<html ⚡ lang=\"en\">" in html
    assert "async src=\"https://cdn.ampproject.org/v0.js\"" in html
    assert "<style amp-boilerplate>" in html
    assert "<style amp-custom>" in html
    assert DISCLAIMER_TEXT in html
    assert ide["name"] in html
    assert "https://ideguide.blogspot.com/" in html
    assert "https://www.youtube.com/@IDEguide" in html

def test_amp_html_pros_cons():
    ide = CURATED_IDE_CATALOG[1]
    html = generate_amp_html(ide, "2026-08-31")

    for pro in ide["pros"]:
        assert pro in html
    for con in ide["cons"]:
        assert con in html
