import json
import os
import shutil
import tempfile
import pytest
from scripts.amp_validator import validate_amp_html, DISCLAIMER_TEXT
from scripts.generate_daily_content import (
    select_daily_ides,
    generate_amp_blog_post,
    generate_google_flow_video_spec,
    run_daily_generation,
    IDE_DATABASE
)
from scripts.ide_guide_agent_skill import generate_custom_package, build_custom_ide_data


def test_disclaimer_constant():
    assert "not sponsored" in DISCLAIMER_TEXT
    assert "IDE Guide" in DISCLAIMER_TEXT


def test_ide_database_validity():
    assert len(IDE_DATABASE) >= 10
    for ide in IDE_DATABASE:
        assert "id" in ide
        assert "name" in ide
        assert "pricing" in ide
        assert len(ide["pros"]) > 0
        assert len(ide["cons"]) > 0
        assert "target_audience" in ide


def test_amp_blog_post_generation_and_validation():
    ide = IDE_DATABASE[0]
    date_str = "2026-10-01"
    amp_html = generate_amp_blog_post(ide, date_str)

    # Check AMP HTML content
    assert "<html amp" in amp_html or "<html ⚡" in amp_html
    assert ide["name"] in amp_html
    assert DISCLAIMER_TEXT in amp_html
    assert "https://cdn.ampproject.org/v0.js" in amp_html

    # Validate using amp_validator
    is_valid, errors = validate_amp_html(amp_html)
    assert is_valid, f"AMP Validation errors: {errors}"


def test_google_flow_video_spec_generation():
    ide = IDE_DATABASE[0]
    date_str = "2026-10-01"
    spec = generate_google_flow_video_spec(ide, date_str)

    assert spec["metadata"]["channel"] == "@IDEguide"
    assert spec["metadata"]["target_ide"] == ide["name"]
    assert "google_flow_prompts" in spec
    assert len(spec["shots"]) >= 5
    assert spec["disclaimer"] == DISCLAIMER_TEXT


def test_daily_generation_workflow():
    temp_dir = tempfile.mkdtemp()
    try:
        history_file = os.path.join(temp_dir, "history.json")
        ides_day1 = select_daily_ides(3, history_path=history_file)
        assert len(ides_day1) == 3

        ides_day2 = select_daily_ides(3, history_path=history_file)
        assert len(ides_day2) == 3

        # Ensure day 1 and day 2 didn't pick the same IDEs
        day1_ids = [i["id"] for i in ides_day1]
        day2_ids = [i["id"] for i in ides_day2]
        assert set(day1_ids).isdisjoint(set(day2_ids))
    finally:
        shutil.rmtree(temp_dir)


def test_agentic_skill_custom_generation():
    temp_dir = tempfile.mkdtemp()
    try:
        generate_custom_package("Custom IDE", "https://github.com/custom/ide", output_dir=temp_dir)
        files = os.listdir(temp_dir)
        assert any(f.startswith("post_") and f.endswith(".html") for f in files)
        assert any(f.startswith("video_spec_") and f.endswith(".json") for f in files)
        assert any(f.startswith("video_spec_") and f.endswith(".md") for f in files)

        # Verify content of generated AMP post
        post_file = [f for f in files if f.endswith(".html")][0]
        with open(os.path.join(temp_dir, post_file), "r", encoding="utf-8") as f:
            content = f.read()

        is_valid, errors = validate_amp_html(content)
        assert is_valid, f"Custom package AMP validation errors: {errors}"
        assert DISCLAIMER_TEXT in content
    finally:
        shutil.rmtree(temp_dir)
