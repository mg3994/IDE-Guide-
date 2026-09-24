import json
import os
import pytest

from scripts.amp_validator import validate_amp_html, DISCLAIMER_TEXT
from scripts.ide_guide_agent_skill import get_ide_data, generate_amp_blog, generate_video_spec
from scripts.generate_daily_content import generate_daily_batch, load_history

def test_amp_validator_valid_html():
    valid_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>Test Title</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/test">
  <style amp-boilerplate>body{{animation:none}}</style>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-custom>body {{ color: red; }}</style>
</head>
<body>
  <p>{DISCLAIMER_TEXT}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(valid_html)
    assert is_valid is True, f"Expected valid HTML but got errors: {errors}"
    assert len(errors) == 0

def test_amp_validator_detects_forbidden_img_and_missing_disclaimer():
    invalid_html = """<!doctype html>
<html>
<head><title>Bad Page</title></head>
<body>
  <img src="test.jpg" alt="test">
</body>
</html>"""
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("Forbidden tag <img" in e for e in errors)
    assert any("Missing mandatory non-sponsorship disclaimer" in e for e in errors)

def test_agent_skill_generator():
    ide_data = get_ide_data("cursor")
    assert ide_data["name"] == "Cursor IDE"
    assert "Freemium" in ide_data["pricing_type"]

    amp_html = generate_amp_blog(ide_data)
    is_valid, errors = validate_amp_html(amp_html)
    assert is_valid is True, f"Generated AMP HTML is invalid: {errors}"

    video_spec = generate_video_spec(ide_data)
    assert "youtube_channel" in video_spec
    assert len(video_spec["full_video_scenes"]) == 4
    assert DISCLAIMER_TEXT in video_spec["disclaimer"]

    # Verify Google Flow prompt in scene 1
    scene_1_prompt = video_spec["full_video_scenes"][0]["google_flow_prompt"]
    assert "Cursor IDE" in scene_1_prompt
    assert "Cinematic" in scene_1_prompt or "close-up" in scene_1_prompt

def test_daily_batch_generator(tmp_path, monkeypatch):
    test_date = "2026-04-01"
    monkeypatch.setattr("scripts.generate_daily_content.HISTORY_FILE", str(tmp_path / "history.json"))

    date_dir = generate_daily_batch(test_date)
    assert os.path.exists(date_dir)

    files = os.listdir(date_dir)
    amp_files = [f for f in files if f.endswith(".html")]
    spec_files = [f for f in files if f.endswith(".json")]

    assert len(amp_files) == 3, f"Expected 3 AMP blog files, found {len(amp_files)}"
    assert len(spec_files) == 3, f"Expected 3 video spec files, found {len(spec_files)}"

    for amp_file in amp_files:
        filepath = os.path.join(date_dir, amp_file)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        is_valid, errors = validate_amp_html(content)
        assert is_valid is True, f"Daily generated file {amp_file} failed AMP validation: {errors}"
