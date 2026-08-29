import os
import json
import pytest
import sys
import tempfile
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts")))

from generate_daily_content import (
    generate_amp_html_blog_post,
    generate_google_flow_video_spec,
    get_target_ides,
    load_history,
    save_history,
    DISCLAIMER_TEXT,
    IDE_CATALOG
)
from ide_guide_agent_skill import build_custom_ide_data

def test_disclaimer_text_integrity():
    expected = (
        "Disclaimer: IDE Guide is an independent technical publication. "
        "This content is not sponsored, endorsed, or affiliated with any software vendor or editor developer "
        "mentioned above. All reviews and assessments are based strictly on objective developer evaluation."
    )
    assert DISCLAIMER_TEXT == expected

def test_amp_html_post_generation():
    test_ide = IDE_CATALOG[0]
    amp_html = generate_amp_html_blog_post(test_ide)

    assert "<html ⚡ lang=\"en\">" in amp_html
    assert "https://cdn.ampproject.org/v0.js" in amp_html
    assert "<style amp-boilerplate>" in amp_html
    assert "<style amp-custom>" in amp_html
    assert test_ide['name'] in amp_html
    assert test_ide['pricing_model'] in amp_html
    assert DISCLAIMER_TEXT in amp_html

def test_google_flow_video_spec_generation():
    test_ide = IDE_CATALOG[0]
    spec = generate_google_flow_video_spec(test_ide)

    assert spec["channel"] == "@IDEguide"
    assert spec["ide_name"] == test_ide["name"]
    assert len(spec["target_formats"]) == 2
    assert spec["target_formats"][0]["aspect_ratio"] == "16:9"
    assert spec["target_formats"][1]["aspect_ratio"] == "9:16"

    scenes = spec["google_flow_visual_prompts"]["scene_sequence"]
    assert len(scenes) == 6
    assert spec["disclaimer"] == DISCLAIMER_TEXT

def test_history_rotation_and_uniqueness():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_history_file = os.path.join(tmp_dir, "history.json")
        save_history({"covered_ides": [], "last_updated": ""}, tmp_history_file)

        target1 = get_target_ides(count=3, history_file=tmp_history_file)
        assert len(target1) == 3

        # Mark target1 as covered
        slugs1 = [item['slug'] for item in target1]
        save_history({"covered_ides": slugs1, "last_updated": "2026-08-29"}, tmp_history_file)

        target2 = get_target_ides(count=3, history_file=tmp_history_file)
        assert len(target2) == 3
        slugs2 = [item['slug'] for item in target2]

        # Ensure no overlap if catalog has enough items
        overlap = set(slugs1).intersection(set(slugs2))
        assert len(overlap) == 0

def test_agentic_skill_custom_builder():
    custom_ide = build_custom_ide_data("Fleet", pricing="Paid Subscription", developer="JetBrains")
    assert custom_ide["name"] == "Fleet"
    assert custom_ide["slug"] == "fleet"
    assert custom_ide["developer"] == "JetBrains"

    amp_html = generate_amp_html_blog_post(custom_ide)
    assert "Fleet" in amp_html
    assert DISCLAIMER_TEXT in amp_html

    flow_spec = generate_google_flow_video_spec(custom_ide)
    assert flow_spec["ide_name"] == "Fleet"
    assert flow_spec["disclaimer"] == DISCLAIMER_TEXT
