import os
import json
import pytest
from scripts.amp_validator import validate_amp_content
from scripts.generate_daily_content import (
    generate_daily_content_package,
    generate_amp_blog_post,
    generate_google_flow_video_spec,
    load_history,
    DISCLAIMER_TEXT,
    IDE_DATABASE
)
from scripts.ide_guide_agent_skill import generate_skill_content, parse_repo_url

def test_disclaimer_text_presence():
    assert "IDE Guide is an independent technical publication" in DISCLAIMER_TEXT
    assert "not sponsored" in DISCLAIMER_TEXT

def test_amp_validator_valid():
    sample_amp = f"""
    <div>
        <h2>Test IDE Review</h2>
        <amp-img src="https://example.com/test.png" width="800" height="450" layout="responsive" alt="Test"></amp-img>
        <p>{DISCLAIMER_TEXT}</p>
    </div>
    """
    is_valid, errors = validate_amp_content(sample_amp)
    assert is_valid is True
    assert len(errors) == 0

def test_amp_validator_invalid_img():
    sample_invalid = f"""
    <div>
        <img src="https://example.com/test.png" alt="Test">
        <p>{DISCLAIMER_TEXT}</p>
    </div>
    """
    is_valid, errors = validate_amp_content(sample_invalid)
    assert is_valid is False
    assert any("Forbidden <img> tag" in err for err in errors)

def test_amp_validator_missing_disclaimer():
    sample_invalid = """
    <div>
        <amp-img src="https://example.com/test.png" width="800" height="450" layout="responsive" alt="Test"></amp-img>
    </div>
    """
    is_valid, errors = validate_amp_content(sample_invalid)
    assert is_valid is False
    assert any("Mandatory non-sponsorship disclaimer missing" in err for err in errors)

def test_daily_content_generation(tmp_path, monkeypatch):
    test_date = "2026-08-27"
    # Run content generation
    files = generate_daily_content_package(test_date)
    assert len(files) == 6

    # Verify 3 blog posts and 3 video specs
    amp_files = [f for f in files if f.endswith(".amp.html")]
    json_files = [f for f in files if f.endswith(".json")]
    assert len(amp_files) == 3
    assert len(json_files) == 3

    for blog in amp_files:
        with open(blog, "r", encoding="utf-8") as f:
            content = f.read()
        is_valid, errors = validate_amp_content(content)
        assert is_valid is True, f"AMP validation errors in {blog}: {errors}"

    for video in json_files:
        with open(video, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["channel"] == "@IDEguide"
        assert DISCLAIMER_TEXT in data["disclaimer"]
        assert "prompts_google_flow" in data

def test_agent_skill():
    repo_info = parse_repo_url("https://github.com/helix-editor/helix")
    assert repo_info["name"] == "Helix"
    assert repo_info["slug"] == "helix"

    blog_path, video_path = generate_skill_content(repo_info, output_dir="content/test_agent")
    assert os.path.exists(blog_path)
    assert os.path.exists(video_path)

    with open(blog_path, "r", encoding="utf-8") as f:
        content = f.read()
    is_valid, _ = validate_amp_content(content)
    assert is_valid is True
