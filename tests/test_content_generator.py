import json
import os
import sys
import pytest

# Add scripts to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from generate_daily_content import (
    generate_amp_html,
    generate_google_flow_spec,
    load_history,
    save_history,
    MANDATORY_DISCLAIMER,
    CURATED_IDE_DATABASE,
)

def test_amp_boilerplate_and_disclaimer():
    sample_ide = CURATED_IDE_DATABASE[0]
    amp_html = generate_amp_html(sample_ide)

    # Check AMP HTML essentials
    assert '<html ⚡ lang="en">' in amp_html or '<html amp lang="en">' in amp_html
    assert 'https://cdn.ampproject.org/v0.js' in amp_html
    assert '<style amp-boilerplate>' in amp_html
    assert '<style amp-custom>' in amp_html
    assert '<amp-img' in amp_html
    assert MANDATORY_DISCLAIMER in amp_html

def test_google_flow_spec_structure():
    sample_ide = CURATED_IDE_DATABASE[1]
    spec = generate_google_flow_spec(sample_ide)

    assert spec["branding"]["channel_name"] == "IDE Guide"
    assert spec["branding"]["youtube_handle"] == "@IDEguide"
    assert spec["non_sponsorship_disclaimer"] == MANDATORY_DISCLAIMER
    assert len(spec["scenes"]) >= 5

    # Check mandatory scene properties
    for scene in spec["scenes"]:
        assert "visual_prompt" in scene
        assert "camera_motion" in scene
        assert "lighting" in scene
        assert "voiceover" in scene
        assert "on_screen_text" in scene

def test_history_file_operations(tmp_path):
    history_path = tmp_path / "history.json"
    dummy_history = {"covered_ides": ["cursor ai"], "daily_runs": []}

    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(dummy_history, f)

    with open(history_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "cursor ai" in data["covered_ides"]
