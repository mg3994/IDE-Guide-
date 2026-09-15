import json
import os
import shutil
import pytest
from datetime import datetime

import ide_guide_agent_skill as skill
import generate_daily_content as daily

def test_amp_html_blog_generation():
    data = skill.IDE_DATABASE["cursor"]
    amp_html = skill.generate_amp_html_blog(data)

    # Verify AMP HTML required tags & attributes
    assert "<html ⚡" in amp_html or "<html amp" in amp_html
    assert "<style amp-boilerplate>" in amp_html
    assert "<style amp-custom>" in amp_html
    assert "https://cdn.ampproject.org/v0.js" in amp_html
    assert "Cursor IDE" in amp_html
    assert skill.DISCLAIMER_TEXT in amp_html

def test_google_flow_video_spec_generation():
    data = skill.IDE_DATABASE["zed"]
    spec = skill.generate_google_flow_video_spec(data)

    assert spec["channel"] == "@IDEguide"
    assert spec["disclaimer"] == skill.DISCLAIMER_TEXT
    assert len(spec["scenes"]) >= 4

    scene1 = spec["scenes"][0]
    assert "visual_prompt" in scene1
    assert "camera_framing_motion" in scene1
    assert "lighting_atmosphere" in scene1
    assert "text_overlay" in scene1
    assert "voiceover_script" in scene1

def test_daily_content_batch_generation(tmp_path, monkeypatch):
    test_content_dir = str(tmp_path / "content")
    monkeypatch.setattr(daily, "CONTENT_DIR", test_content_dir)
    monkeypatch.setattr(daily, "HISTORY_FILE", os.path.join(test_content_dir, "history.json"))

    date_str = "2026-09-15"
    files = daily.generate_daily_batch(date_str)

    assert len(files) == 6  # 3 AMP blog posts + 3 video specs

    blogs = [f for f in files if "blogs" in f]
    videos = [f for f in files if "videos" in f]

    assert len(blogs) == 3
    assert len(videos) == 3

    # Check history recording
    history_file = os.path.join(test_content_dir, "history.json")
    assert os.path.exists(history_file)
    with open(history_file, "r") as f:
        history = json.load(f)
    assert len(history["covered_keys"]) == 3

def test_cli_agent_skill_fallback():
    data = skill.get_ide_data("https://github.com/custom-org/hyper-editor")
    assert data["name"] == "Hyper Editor"
    assert "custom-org/hyper-editor" not in data["name"]
    assert skill.DISCLAIMER_TEXT in skill.generate_amp_html_blog(data)
