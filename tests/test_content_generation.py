"""Tests for daily content generation and history tracking."""

import os
import json
import tempfile
import pytest
from scripts.generate_daily_content import (
    select_daily_ides,
    load_history,
    save_history,
    generate_amp_blog_post,
    generate_flow_video_spec,
    run_daily_generation,
    DISCLAIMER_TEXT,
)
from data.ide_database import IDE_CATALOG


def test_ide_catalog_integrity():
    assert len(IDE_CATALOG) >= 10
    for name, data in IDE_CATALOG.items():
        assert "name" in data
        assert "tagline" in data
        assert "pricing_model" in data
        assert "pricing_details" in data
        assert len(data["pros"]) >= 2
        assert len(data["cons"]) >= 2
        assert "best_for" in data
        assert "visual_theme" in data
        assert "flow_broll_prompt" in data


def test_history_rotation():
    with tempfile.TemporaryDirectory() as tmpdir:
        hist_file = os.path.join(tmpdir, "test_history.json")

        # First run: select 3 IDEs
        batch1 = select_daily_ides(count=3, history_path=hist_file)
        assert len(batch1) == 3

        history1 = load_history(hist_file)
        assert len(history1) == 3
        assert set(batch1) == set(history1)

        # Second run: next 3 IDEs should be disjoint from first run
        batch2 = select_daily_ides(count=3, history_path=hist_file)
        assert len(batch2) == 3
        assert len(set(batch1).intersection(set(batch2))) == 0

        history2 = load_history(hist_file)
        assert len(history2) == 6


def test_generate_amp_blog_post_structure():
    data = IDE_CATALOG["Cursor"]
    html = generate_amp_blog_post(data)

    assert "<article class=\"ide-guide-post\"" in html
    assert "Cursor" in html
    assert "The Good" in html
    assert "The Bad" in html
    assert "Pricing Model" in html
    assert DISCLAIMER_TEXT in html
    assert "https://www.cursor.com" in html


def test_generate_flow_video_spec_format():
    data = IDE_CATALOG["Zed"]

    # Test full 16:9 spec
    spec_16_9 = generate_flow_video_spec(data, is_short=False)
    assert spec_16_9["aspect_ratio"] == "16:9 (1920x1080)"
    assert spec_16_9["channel"] == "@IDEguide"
    assert len(spec_16_9["google_flow_prompts"]["scenes"]) == 4
    assert spec_16_9["independent_disclaimer"] == DISCLAIMER_TEXT
    assert "master_aesthetic_prompt" in spec_16_9["google_flow_prompts"]

    # Test shorts 9:16 spec
    spec_shorts = generate_flow_video_spec(data, is_short=True)
    assert spec_shorts["aspect_ratio"] == "9:16 (1080x1920)"
    assert "Shorts" in spec_shorts["format"]


def test_run_daily_generation_output():
    with tempfile.TemporaryDirectory() as tmpdir:
        results = run_daily_generation(output_base_dir=tmpdir, target_date="2026-11-01")
        assert len(results["selected_ides"]) == 3
        assert len(results["generated_files"]) == 9  # 3 posts + 3 16:9 + 3 shorts

        for filepath in results["generated_files"]:
            assert os.path.exists(filepath)
            assert os.path.getsize(filepath) > 0
