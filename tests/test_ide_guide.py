import pytest
import json
import shutil
from pathlib import Path

from scripts.amp_validator import validate_amp_html, MANDATORY_DISCLAIMER
from scripts.ide_guide_agent_skill import (
    get_ide_info,
    generate_amp_blog_post,
    generate_google_flow_video_spec,
)
from scripts.generate_daily_content import (
    load_history,
    save_history,
    select_daily_ides,
    run_daily_generation,
)


def test_mandatory_disclaimer_constant():
    assert "not sponsored, endorsed, or affiliated" in MANDATORY_DISCLAIMER
    assert "IDE Guide is an independent technical publication." in MANDATORY_DISCLAIMER


def test_amp_validator_valid_html():
    valid_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-custom>
    body {{ font-family: sans-serif; }}
  </style>
</head>
<body>
  <p>{MANDATORY_DISCLAIMER}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(valid_html)
    assert is_valid is True
    assert len(errors) == 0


def test_amp_validator_detects_errors():
    # Missing html tag, missing charset, missing runtime script, includes forbidden <img>, missing disclaimer
    invalid_html = """<html>
<head></head>
<body>
  <img src="test.jpg" alt="test">
  <div style="color: red;">Inline style</div>
</body>
</html>"""
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("Missing <html ⚡>" in e for e in errors)
    assert any("Missing <meta charset=" in e for e in errors)
    assert any("Missing AMP runtime script" in e for e in errors)
    assert any("Forbidden standard <img>" in e for e in errors)
    assert any("Forbidden inline style" in e for e in errors)
    assert any("non-sponsorship disclaimer" in e for e in errors)


def test_agent_skill_generation(tmp_path):
    info = get_ide_info(ide_name="Visual Studio Code", price="Free")
    assert info["name"] == "Visual Studio Code"
    assert info["price_tier"] == "Free"

    blog_html = generate_amp_blog_post(info)
    is_valid, errors = validate_amp_html(blog_html)
    assert is_valid is True, f"Generated blog post failed AMP validation: {errors}"
    assert MANDATORY_DISCLAIMER in blog_html

    video_spec = generate_google_flow_video_spec(info)
    assert video_spec["ide_name"] == "Visual Studio Code"
    assert "long_form_video" in video_spec
    assert "shorts_video" in video_spec
    assert video_spec["long_form_video"]["non_sponsorship_disclaimer"] == MANDATORY_DISCLAIMER
    assert video_spec["shorts_video"]["non_sponsorship_disclaimer"] == MANDATORY_DISCLAIMER


def test_repo_url_parsing():
    info = get_ide_info(repo_url="https://github.com/zed-industries/zed")
    assert info["name"] == "Zed"
    assert info["developer"] == "Zed Industries"


def test_daily_content_generation_flow(monkeypatch, tmp_path):
    history_path = tmp_path / "history.json"
    monkeypatch.setattr("scripts.generate_daily_content.HISTORY_FILE", history_path)

    # Initial run
    history = load_history()
    assert history["covered_ides"] == []

    selected = select_daily_ides(count=3)
    assert len(selected) == 3

    run_daily_generation()

    assert history_path.exists()
    updated_history = load_history()
    assert len(updated_history["covered_ides"]) == 3
    assert len(updated_history["daily_runs"]) == 1
