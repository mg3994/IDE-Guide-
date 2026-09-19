import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from scripts.generate_daily_content import build_amp_html, CURATED_IDES, DISCLAIMER_TEXT

def test_amp_html_structure():
    sample_ide = CURATED_IDES[0]
    amp_html = build_amp_html(sample_ide)

    # AMP HTML Validation Requirements
    assert amp_html.startswith("<!doctype html>") or amp_html.startswith("<!DOCTYPE html>")
    assert '<html ⚡ lang="en">' in amp_html or '<html amp lang="en">' in amp_html
    assert '<meta charset="utf-8">' in amp_html
    assert '<script async src="https://cdn.ampproject.org/v0.js"></script>' in amp_html
    assert '<link rel="canonical"' in amp_html
    assert '<meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">' in amp_html
    assert '<style amp-boilerplate>' in amp_html
    assert '<noscript><style amp-boilerplate>' in amp_html
    assert '<style amp-custom>' in amp_html
    assert DISCLAIMER_TEXT in amp_html

def test_amp_html_contains_ide_details():
    sample_ide = CURATED_IDES[1] # Cursor
    amp_html = build_amp_html(sample_ide)

    assert sample_ide["name"] in amp_html
    assert sample_ide["category"] in amp_html
    assert sample_ide["pricing_type"] in amp_html
    assert sample_ide["best_for"] in amp_html
