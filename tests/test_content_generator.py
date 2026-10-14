import pytest
import json
from scripts.generate_daily_content import generate_amp_blog_post, generate_video_spec, generate_video_spec_markdown, IDE_POOL, REQUIRED_DISCLAIMER
from scripts.amp_validator import validate_amp_html

def test_ide_pool_structure():
    assert len(IDE_POOL) >= 5
    for ide in IDE_POOL:
        assert "name" in ide
        assert "slug" in ide
        assert "pricing" in ide
        assert "pros" in ide and len(ide["pros"]) > 0
        assert "cons" in ide and len(ide["cons"]) > 0
        assert "best_for" in ide

def test_generate_amp_blog_post():
    sample_ide = IDE_POOL[0]
    html = generate_amp_blog_post(sample_ide)
    is_valid, errors = validate_amp_html(html)
    assert is_valid is True, f"Errors: {errors}"
    assert sample_ide["name"] in html
    assert REQUIRED_DISCLAIMER in html

def test_generate_video_spec():
    sample_ide = IDE_POOL[0]
    spec = generate_video_spec(sample_ide)
    assert spec["channel"] == "@IDEguide"
    assert len(spec["prompts"]) == 5
    assert spec["disclaimer"] == REQUIRED_DISCLAIMER

    spec_md = generate_video_spec_markdown(spec)
    assert sample_ide["name"] in spec_md
    assert REQUIRED_DISCLAIMER in spec_md
