import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from ide_guide_agent_skill import (
    get_ide_info,
    generate_amp_blog_post,
    generate_google_flow_video_spec,
    validate_amp_html,
    DISCLAIMER_TEXT,
)


def test_get_ide_info_known():
    info = get_ide_info("Cursor")
    assert "Cursor" in info["name"]
    assert "Anysphere" in info["developer"]
    assert len(info["pros"]) > 0
    assert len(info["cons"]) > 0


def test_get_ide_info_repo_url():
    info = get_ide_info("https://github.com/zed-industries/zed")
    assert "Zed" in info["name"]


def test_generate_amp_blog_post():
    info = get_ide_info("Neovim")
    html = generate_amp_blog_post(info)
    assert "<html ⚡" in html
    assert "<amp-img" in html
    assert DISCLAIMER_TEXT in html

    is_valid, errors = validate_amp_html(html)
    assert is_valid is True, f"AMP errors: {errors}"


def test_generate_google_flow_video_spec():
    info = get_ide_info("Visual Studio Code")
    spec = generate_google_flow_video_spec(info)
    assert spec["duration_seconds"] == 60
    assert len(spec["scenes"]) == 5
    assert DISCLAIMER_TEXT in spec["disclaimer"]
    for scene in spec["scenes"]:
        assert "narration_script" in scene
        assert "visual_prompt" in scene
        assert "camera_motion" in scene
        assert "overlay_text" in scene
