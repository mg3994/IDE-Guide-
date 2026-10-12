import os
import json
import pytest

from scripts.amp_validator import validate_amp_html, MANDATORY_DISCLAIMER
from scripts.ide_guide_agent_skill import generate_amp_blog_post, generate_google_flow_spec
from scripts.generate_daily_content import generate_daily, load_history

def test_amp_validator_valid():
    valid_html = f"""<div><h1>Test Post</h1><style amp-custom>p {{ color: red; }}</style><p>{MANDATORY_DISCLAIMER}</p></div>"""
    is_valid, errors = validate_amp_html(valid_html)
    assert is_valid
    assert len(errors) == 0

def test_amp_validator_missing_disclaimer():
    invalid_html = "<div><h1>Test Post</h1><style amp-custom>p { color: red; }</style></div>"
    is_valid, errors = validate_amp_html(invalid_html)
    assert not is_valid
    assert any("mandatory non-sponsorship disclaimer" in err for err in errors)

def test_amp_validator_forbidden_tags():
    invalid_html = f"""<div><img src="test.jpg" /><p>{MANDATORY_DISCLAIMER}</p></div>"""
    is_valid, errors = validate_amp_html(invalid_html)
    assert not is_valid
    assert any("Forbidden tag" in err for err in errors)

def test_cli_skill_blog_generation():
    blog_html = generate_amp_blog_post("Cursor")
    assert "Cursor AI Code Editor" in blog_html
    assert "The Good" in blog_html
    assert "The Bad" in blog_html
    assert "Pricing" in blog_html
    assert MANDATORY_DISCLAIMER in blog_html

    is_valid, errors = validate_amp_html(blog_html)
    assert is_valid, f"Generated blog HTML failed AMP validation: {errors}"

def test_cli_skill_video_generation():
    video_spec = generate_google_flow_spec("Zed")
    assert video_spec["ide_name"] == "Zed Editor"
    assert "google_flow_prompts" in video_spec
    assert len(video_spec["google_flow_prompts"]) == 5
    assert video_spec["disclaimer"] == MANDATORY_DISCLAIMER

def test_daily_content_generation(tmp_path):
    test_date = "2026-08-27"
    generated_files = generate_daily(test_date)
    assert len(generated_files) == 6

    # 3 blog posts and 3 video specs
    blogs = [f for f in generated_files if "blog_" in f]
    videos = [f for f in generated_files if "video_" in f]
    assert len(blogs) == 3
    assert len(videos) == 3

    # Check contents
    for b in blogs:
        with open(b, "r", encoding="utf-8") as f:
            content = f.read()
            is_valid, errors = validate_amp_html(content)
            assert is_valid, f"Blog file {b} failed AMP validation: {errors}"

    for v in videos:
        with open(v, "r", encoding="utf-8") as f:
            spec = json.load(f)
            assert "google_flow_prompts" in spec
            assert spec["disclaimer"] == MANDATORY_DISCLAIMER

    # Check history update
    history = load_history("content/history.json")
    assert len(history) >= 3
