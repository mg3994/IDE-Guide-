import os
import sys
import json
import tempfile
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from generate_daily_content import (
    run_daily_generation,
    load_history,
    save_history,
    select_daily_ides,
    generate_amp_blog_html,
    generate_google_flow_video_spec,
    MANDATORY_DISCLAIMER,
    CURATED_IDE_DATABASE
)

def test_curated_ide_database_structure():
    assert len(CURATED_IDE_DATABASE) >= 5
    for ide in CURATED_IDE_DATABASE:
        assert "name" in ide
        assert "slug" in ide
        assert "category" in ide
        assert "description" in ide
        assert "pros" in ide
        assert "cons" in ide
        assert "pricing" in ide
        assert "best_for" in ide
        assert "website" in ide

def test_daily_generation_file_creation():
    with tempfile.TemporaryDirectory() as tmpdir:
        target_date = "2026-03-30"
        run_daily_generation(target_date=target_date, output_base=tmpdir)

        date_dir = os.path.join(tmpdir, target_date)
        assert os.path.exists(date_dir)

        files = os.listdir(date_dir)
        html_files = [f for f in files if f.endswith(".html")]
        md_files = [f for f in files if f.endswith(".md")]

        assert len(html_files) == 3
        assert len(md_files) == 3

        history_path = os.path.join(tmpdir, "history.json")
        assert os.path.exists(history_path)
        history = load_history(history_path)
        assert len(history["covered_ides"]) >= 3

def test_disclaimer_presence():
    sample_ide = CURATED_IDE_DATABASE[0]
    amp_html = generate_amp_blog_html(sample_ide, "2026-03-30")
    video_spec = generate_google_flow_video_spec(sample_ide, "2026-03-30")

    assert MANDATORY_DISCLAIMER in amp_html
    assert MANDATORY_DISCLAIMER in video_spec
