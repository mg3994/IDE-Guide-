"""
Unit tests for IDE Guide AMP HTML compliance and Google Flow Video Spec generation.
"""

import os
import json
import pytest
from scripts.ide_guide_agent_skill import (
    generate_amp_html,
    generate_google_flow_spec,
    get_ide_data,
    run_agent_skill,
    DISCLAIMER_TEXT
)
from scripts.generate_daily_content import select_daily_ides, load_history, save_history


def test_amp_html_compliance():
    ide_info = get_ide_data("Cursor")
    amp_html = generate_amp_html(ide_info)

    # AMP standard checks
    assert "<html ⚡" in amp_html or "<html amp" in amp_html
    assert 'src="https://cdn.ampproject.org/v0.js"' in amp_html
    assert "<style amp-boilerplate>" in amp_html
    assert "<style amp-custom>" in amp_html
    assert 'canonical' in amp_html
    assert DISCLAIMER_TEXT in amp_html
    assert "Cursor" in amp_html


def test_google_flow_spec_structure():
    ide_info = get_ide_data("Zed")
    spec = generate_google_flow_spec(ide_info)

    assert spec["channel"] == "@IDEguide"
    assert spec["youtube_url"] == "https://www.youtube.com/@IDEguide"
    assert DISCLAIMER_TEXT in spec["disclaimer"]
    assert len(spec["scenes"]) >= 3

    for scene in spec["scenes"]:
        assert "google_flow_prompt" in scene
        assert "camera_angle_and_framing" in scene
        assert "lighting_and_atmosphere" in scene
        assert "narration_voiceover" in scene
        assert "on_screen_text_overlays" in scene


def test_agent_skill_execution(tmp_path):
    output_dir = os.path.join(tmp_path, "test_output")
    result = run_agent_skill(ide_name="Neovim", price_model="Free", output_dir=output_dir)

    assert os.path.exists(os.path.join(output_dir, "blog_post.amp.html"))
    assert os.path.exists(os.path.join(output_dir, "video_spec.json"))
    assert os.path.exists(os.path.join(output_dir, "video_script.md"))

    with open(os.path.join(output_dir, "video_spec.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
        assert "Neovim" in data["title"]


def test_daily_selection_no_duplicates(tmp_path):
    history_path = tmp_path / "history.json"
    history_data = {"covered_ides": ["cursor", "zed"], "last_updated": None}

    # Temporarily monkeypatch history path if needed or test select_daily_ides logic
    selected = select_daily_ides(3)
    assert len(selected) == 3
    names = [s["name"].lower() for s in selected]
    assert len(set(names)) == 3
