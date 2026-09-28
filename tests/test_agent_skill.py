import pytest
from scripts.ide_guide_agent_skill import (
    get_ide_info,
    generate_amp_blog_post,
    generate_google_flow_video_spec,
    MANDATORY_DISCLAIMER
)
from scripts.amp_validator import validate_amp_html


def test_get_ide_info_known():
    info = get_ide_info("cursor")
    assert info["name"] == "Cursor"
    assert info["is_paid"] is True
    assert len(info["pros"]) > 0
    assert len(info["cons"]) > 0


def test_get_ide_info_unknown():
    info = get_ide_info("MyCustomIDE")
    assert info["name"] == "Mycustomide" or info["name"] == "MyCustomIDE"
    assert "MyCustomIDE" in info["description"] or "Mycustomide" in info["description"]


def test_generate_amp_blog_post():
    info = get_ide_info("zed")
    blog_html = generate_amp_blog_post(info)
    assert "<amp-img" in blog_html
    assert MANDATORY_DISCLAIMER in blog_html

    is_valid, errors = validate_amp_html(blog_html)
    assert is_valid is True, f"AMP Validation errors: {errors}"


def test_generate_google_flow_video_spec():
    info = get_ide_info("neovim")
    spec = generate_google_flow_video_spec(info)
    assert spec["channel"] == "@IDEguide"
    assert spec["ide_name"] == "Neovim"
    assert "google_flow_prompts" in spec
    assert len(spec["google_flow_prompts"]["landscape_16_9"]) == 4
    assert len(spec["google_flow_prompts"]["vertical_shorts_9_16"]) == 3
    assert spec["disclaimer"] == MANDATORY_DISCLAIMER
