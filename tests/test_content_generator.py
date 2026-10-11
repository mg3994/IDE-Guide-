"""
Unit tests for IDE Guide Content Generator, AMP Validator, and Agentic CLI Skill.
"""

import json
import os
import shutil
import tempfile
import pytest

from scripts.amp_validator import validate_amp_html, DISCLAIMER_TEXT
from scripts.generate_daily_content import select_daily_ides, generate_amp_blog_post, generate_google_flow_video_spec, IDE_CATALOG
from scripts.ide_guide_agent_skill import parse_repo_or_name, generate_custom_content


def test_amp_validator_valid():
    sample_amp_html = f"""
    <h2>VS Code Review</h2>
    <p>Sample text for testing.</p>
    <amp-img width="800" height="450" layout="responsive" src="https://example.com/img.png" alt="Preview"></amp-img>
    <p>{DISCLAIMER_TEXT}</p>
    """
    is_valid, errors = validate_amp_html(sample_amp_html)
    assert is_valid is True
    assert len(errors) == 0


def test_amp_validator_prohibited_tags():
    invalid_html = f"""
    <h2>VS Code Review</h2>
    <img src="https://example.com/img.png" />
    <script>alert('bad');</script>
    <div style="color: red;">Inline style</div>
    <p>{DISCLAIMER_TEXT}</p>
    """
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("<img>" in err for err in errors)
    assert any("script" in err.lower() for err in errors)
    assert any("style" in err.lower() for err in errors)


def test_daily_content_generation_and_history():
    temp_dir = tempfile.mkdtemp()
    try:
        history_path = os.path.join(temp_dir, "history.json")

        # First round: 3 IDEs
        ides_round1 = select_daily_ides(count=3, history_file=history_path)
        assert len(ides_round1) == 3
        round1_ids = [ide["id"] for ide in ides_round1]

        # Verify history file created
        assert os.path.exists(history_path)
        with open(history_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert data["covered_ide_ids"] == round1_ids

        # Second round: Next 3 IDEs (no overlap)
        ides_round2 = select_daily_ides(count=3, history_file=history_path)
        assert len(ides_round2) == 3
        round2_ids = [ide["id"] for ide in ides_round2]

        # Ensure no overlap between round 1 and round 2
        assert len(set(round1_ids).intersection(set(round2_ids))) == 0

    finally:
        shutil.rmtree(temp_dir)


def test_disclaimer_presence_in_generated_outputs():
    sample_ide = IDE_CATALOG[0]

    blog_html = generate_amp_blog_post(sample_ide)
    assert DISCLAIMER_TEXT in blog_html

    video_spec = generate_google_flow_video_spec(sample_ide)
    assert DISCLAIMER_TEXT in video_spec


def test_agentic_cli_skill():
    temp_dir = tempfile.mkdtemp()
    try:
        # Test custom repo name
        generate_custom_content("zed-industries/zed", temp_dir)
        blog_file = os.path.join(temp_dir, "blog_post_zed.html")
        spec_file = os.path.join(temp_dir, "video_spec_zed.md")

        assert os.path.exists(blog_file)
        assert os.path.exists(spec_file)

        with open(blog_file, 'r', encoding='utf-8') as f:
            blog_content = f.read()
            assert DISCLAIMER_TEXT in blog_content
            is_valid, errors = validate_amp_html(blog_content)
            assert is_valid is True, f"AMP validation failed: {errors}"

        with open(spec_file, 'r', encoding='utf-8') as f:
            spec_content = f.read()
            assert DISCLAIMER_TEXT in spec_content

    finally:
        shutil.rmtree(temp_dir)
