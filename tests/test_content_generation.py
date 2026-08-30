import os
import json
import pytest
import subprocess
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from generate_daily_content import (
    generate_amp_html,
    generate_google_flow_spec,
    DISCLAIMER,
    FALLBACK_IDE_CATALOG,
    load_history,
    save_history,
    select_daily_ides
)
import ide_guide_agent_skill


def test_disclaimer_content():
    expected_disclaimer = (
        "Disclaimer: IDE Guide is an independent technical publication. "
        "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer mentioned above. "
        "All reviews and assessments are based strictly on objective developer evaluation."
    )
    assert DISCLAIMER == expected_disclaimer


def test_generate_amp_html_compliance():
    sample_ide = FALLBACK_IDE_CATALOG[0]
    amp_html = generate_amp_html(sample_ide)

    # AMP validation checks
    assert "<html ⚡ lang=\"en\">" in amp_html
    assert "<style amp-boilerplate>" in amp_html
    assert "<style amp-custom>" in amp_html
    assert "https://cdn.ampproject.org/v0.js" in amp_html
    assert DISCLAIMER in amp_html
    assert sample_ide["name"] in amp_html
    assert sample_ide["pricing"] in amp_html


def test_generate_google_flow_spec():
    sample_ide = FALLBACK_IDE_CATALOG[0]
    spec = generate_google_flow_spec(sample_ide)

    assert spec["channel"] == "@IDEguide"
    assert spec["url"] == "https://www.youtube.com/@IDEguide"
    assert spec["disclaimer"] == DISCLAIMER
    assert "youtube_shorts" in spec["video_formats"]
    assert "youtube_horizontal_video" in spec["video_formats"]
    assert spec["video_formats"]["youtube_shorts"]["aspect_ratio"] == "9:16"
    assert spec["video_formats"]["youtube_horizontal_video"]["aspect_ratio"] == "16:9"

    # Check scene structures
    scenes = spec["video_formats"]["youtube_shorts"]["scenes"]
    assert len(scenes) >= 4
    for scene in scenes:
        assert "visual_prompt" in scene
        assert "voiceover" in scene
        assert "text_overlay" in scene


def test_history_tracking(tmp_path):
    history_file = tmp_path / "test_history.json"
    initial_data = {"covered_slugs": ["vscode"], "history": [{"date": "2026-08-01", "slug": "vscode", "ide_name": "VS Code"}]}

    save_history(initial_data, str(history_file))
    loaded = load_history(str(history_file))

    assert loaded["covered_slugs"] == ["vscode"]

    # Select daily IDEs with history
    selected = select_daily_ides(count=3, history_file=str(history_file))
    assert len(selected) == 3
    for ide in selected:
        assert ide["slug"] != "vscode"


def test_agentic_cli_skill(tmp_path):
    out_dir = tmp_path / "skill_output"
    cmd = [
        sys.executable,
        "scripts/ide_guide_agent_skill.py",
        "--name",
        "Zed Editor",
        "--output-dir",
        str(out_dir)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert "AMP HTML Blog Post created at" in res.stdout

    # Check created files
    blog_file = out_dir / "zed_review_amp.html"
    flow_file = out_dir / "zed_google_flow_spec.json"

    assert blog_file.exists()
    assert flow_file.exists()

    amp_content = blog_file.read_text(encoding="utf-8")
    assert "<html ⚡ lang=\"en\">" in amp_content
    assert DISCLAIMER in amp_content
