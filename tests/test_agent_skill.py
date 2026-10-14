import pytest
from scripts.ide_guide_agent_skill import extract_name_from_repo, get_or_create_ide_meta
from scripts.generate_daily_content import generate_amp_blog_post
from scripts.amp_validator import validate_amp_html

def test_extract_name_from_repo():
    name1 = extract_name_from_repo("https://github.com/zed-industries/zed")
    assert name1 == "Zed"

    name2 = extract_name_from_repo("https://github.com/helix-editor/helix/")
    assert name2 == "Helix"

def test_get_or_create_ide_meta():
    meta = get_or_create_ide_meta("Zed", "Free")
    assert meta["name"] == "Zed"
    assert "slug" in meta
    assert len(meta["pros"]) > 0
    assert len(meta["cons"]) > 0

    custom_meta = get_or_create_ide_meta("MyCustomEditor", "Paid $10")
    assert custom_meta["name"] == "MyCustomEditor"
    html = generate_amp_blog_post(custom_meta)
    is_valid, errors = validate_amp_html(html)
    assert is_valid is True, f"Validation errors: {errors}"
