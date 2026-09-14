import os
import sys
import json
import tempfile
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

from generate_daily_content import (
    generate_amp_html,
    generate_google_flow_spec,
    run_daily_generation,
    load_history,
    save_history,
    DISCLAIMER_TEXT,
    CURATED_IDE_DATABASE
)
from ide_guide_agent_skill import build_custom_ide_data

def test_amp_html_compliance():
    sample_ide = CURATED_IDE_DATABASE[0]
    amp_html = generate_amp_html(sample_ide, "2026-09-14", post_index=1)

    assert "<!doctype html>" in amp_html
    assert "<html ⚡ lang=\"en\">" in amp_html
    assert "https://cdn.ampproject.org/v0.js" in amp_html
    assert "style amp-boilerplate" in amp_html
    assert "style amp-custom" in amp_html
    assert sample_ide["name"] in amp_html
    assert sample_ide["pricing"] in amp_html
    assert DISCLAIMER_TEXT in amp_html

def test_google_flow_spec_structure():
    sample_ide = CURATED_IDE_DATABASE[1]
    flow_json, flow_md = generate_google_flow_spec(sample_ide, "2026-09-14", video_index=1)

    assert flow_json["channel"] == "@IDEguide"
    assert flow_json["ide_name"] == sample_ide["name"]
    assert len(flow_json["scenes"]) == 5
    assert flow_json["disclaimer"] == DISCLAIMER_TEXT

    assert "Google Flow Video Specification" in flow_md
    assert "16:9" in flow_md and "9:16" in flow_md
    assert sample_ide["name"] in flow_md
    assert DISCLAIMER_TEXT in flow_md

def test_run_daily_generation():
    with tempfile.TemporaryDirectory() as tmpdir:
        history_path = os.path.join(tmpdir, "history.json")
        summary = run_daily_generation("2026-09-14", output_base_dir=tmpdir, history_file=history_path)

        assert len(summary) == 3

        # Verify files created
        day_dir = os.path.join(tmpdir, "2026-09-14")
        files = os.listdir(day_dir)

        amp_files = [f for f in files if f.endswith("_amp.html")]
        json_files = [f for f in files if f.endswith("_flow.json")]
        md_files = [f for f in files if f.endswith("_flow.md")]

        assert len(amp_files) == 3
        assert len(json_files) == 3
        assert len(md_files) == 3

        # Verify history updated
        history = load_history(history_path)
        assert len(history["covered_ides"]) == 3

def test_agent_skill_builder():
    custom_data = build_custom_ide_data("Sublime Text", tagline="Fast text editor", pricing="Paid")
    assert custom_data["name"] == "Sublime Text"
    assert custom_data["tagline"] == "Fast text editor"
    assert custom_data["pricing"] == "Paid"
    assert len(custom_data["good_points"]) > 0
    assert len(custom_data["bad_points"]) > 0
