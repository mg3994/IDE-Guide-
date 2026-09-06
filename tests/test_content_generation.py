import os
import json
import shutil
import pytest
from datetime import datetime, timezone
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from generate_daily_content import (
    generate_amp_html_post,
    generate_google_flow_video_spec,
    select_ides_for_today,
    load_history,
    save_history,
    NON_SPONSORSHIP_DISCLAIMER,
    CURATED_IDES
)
from ide_guide_agent_skill import run_agentic_skill


def test_disclaimer_constant():
    assert "not sponsored, endorsed, or affiliated" in NON_SPONSORSHIP_DISCLAIMER
    assert "IDE Guide is an independent technical publication" in NON_SPONSORSHIP_DISCLAIMER


def test_generate_amp_html_post():
    sample_ide = CURATED_IDES[0]
    amp_html = generate_amp_html_post(sample_ide)

    # AMP HTML validations
    assert "<html ⚡ lang=\"en\">" in amp_html or "<html amp lang=\"en\">" in amp_html
    assert "https://cdn.ampproject.org/v0.js" in amp_html
    assert "style amp-boilerplate" in amp_html
    assert NON_SPONSORSHIP_DISCLAIMER in amp_html
    assert sample_ide["name"] in amp_html
    assert sample_ide["pricing"] in amp_html
    assert "https://ideguide.blogspot.com/" in amp_html


def test_generate_google_flow_video_spec():
    sample_ide = CURATED_IDES[1]
    video_spec = generate_google_flow_video_spec(sample_ide)

    assert video_spec["channel"] == "@IDEguide"
    assert video_spec["website"] == "https://ideguide.blogspot.com/"
    assert video_spec["disclaimer"] == NON_SPONSORSHIP_DISCLAIMER
    assert video_spec["ide_name"] == sample_ide["name"]

    # Check scene prompts
    scenes = video_spec["google_flow_prompts"]
    assert len(scenes) >= 3
    for scene in scenes:
        assert "visual_prompt" in scene
        assert "framing" in scene
        assert "lighting" in scene
        assert "camera_motion" in scene
        assert "narration" in scene


def test_history_tracking(tmp_path):
    hist_file = os.path.join(tmp_path, "history.json")

    initial_history = load_history(hist_file)
    assert initial_history == {"covered_ides": [], "daily_logs": []}

    initial_history["covered_ides"].append("visual studio code")
    save_history(initial_history, hist_file)

    loaded = load_history(hist_file)
    assert "visual studio code" in loaded["covered_ides"]


def test_select_ides_for_today():
    history = {"covered_ides": ["visual studio code", "neovim"]}
    selected = select_ides_for_today(history, count=3)

    assert len(selected) == 3
    for item in selected:
        assert item["name"].lower() not in history["covered_ides"]


def test_agentic_cli_skill(tmp_path):
    output_dir = str(tmp_path / "agent_out")
    result = run_agentic_skill(
        ide_name="Test custom IDE",
        pricing="Free",
        category="Test Category",
        output_dir=output_dir
    )

    assert result["status"] == "success"
    assert result["disclaimer_included"] is True
    assert os.path.exists(result["blog_post_path"])
    assert os.path.exists(result["video_spec_path"])

    with open(result["blog_post_path"], "r", encoding="utf-8") as f:
        html = f.read()
        assert "<html ⚡ lang=\"en\">" in html
        assert NON_SPONSORSHIP_DISCLAIMER in html

    with open(result["video_spec_path"], "r", encoding="utf-8") as f:
        spec = json.load(f)
        assert spec["disclaimer"] == NON_SPONSORSHIP_DISCLAIMER
