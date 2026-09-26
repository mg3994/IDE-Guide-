import json
import pytest
from pathlib import Path
from scripts.ide_guide_agent_skill import (
    get_or_create_ide_info,
    generate_amp_blog_post,
    generate_google_flow_spec,
    REQUIRED_DISCLAIMER
)
from scripts.amp_validator import validate_amp_html

def test_get_or_create_ide_info_existing():
    info = get_or_create_ide_info("Cursor AI")
    assert "Cursor" in info["name"]
    assert "pros" in info
    assert len(info["pros"]) > 0

def test_get_or_create_ide_info_dynamic():
    info = get_or_create_ide_info("Custom New IDE")
    assert info["name"] == "Custom New Ide"
    assert len(info["pros"]) > 0

def test_generate_amp_blog_post():
    info = get_or_create_ide_info("VS Code")
    html = generate_amp_blog_post(info)
    assert "<amp-img" in html
    assert REQUIRED_DISCLAIMER in html
    is_valid, errors = validate_amp_html(html)
    assert is_valid is True, f"Errors: {errors}"

def test_generate_google_flow_spec():
    info = get_or_create_ide_info("Zed")
    spec = generate_google_flow_spec(info)
    assert spec["target_ide"] == "Zed Editor"
    assert len(spec["scenes"]) >= 3
    assert "visual_prompt" in spec["scenes"][0]
    assert "voiceover_script" in spec["scenes"][0]
    assert REQUIRED_DISCLAIMER in spec["description"]
