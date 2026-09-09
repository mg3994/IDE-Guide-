import pytest
from src.ide_guide.catalog import DEFAULT_IDE_CATALOG
from src.ide_guide.amp_generator import generate_amp_blog_post, DISCLAIMER_TEXT

def test_amp_generator_output():
    sample_ide = DEFAULT_IDE_CATALOG[0]
    html = generate_amp_blog_post(sample_ide)

    # Check AMP HTML compliance tags
    assert "<!DOCTYPE html>" in html
    assert "<html ⚡ lang=\"en\">" in html or "<html amp lang=\"en\">" in html
    assert 'src="https://cdn.ampproject.org/v0.js"' in html
    assert "<style amp-boilerplate>" in html
    assert "<style amp-custom>" in html
    assert "<amp-img" in html

    # Check content sections
    assert sample_ide["name"] in html
    assert "Overview" in html
    assert "Key Capabilities & Features" in html
    assert "The Good (Pros)" in html
    assert "The Bad (Cons)" in html
    assert "IDE Guide Rating & Verdict" in html

    # Check exact disclaimer text
    assert DISCLAIMER_TEXT in html
