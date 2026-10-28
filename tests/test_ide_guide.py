import os
import json
import pytest
import shutil
from pathlib import Path

from scripts.amp_validator import validate_amp_html
from scripts.generate_daily_content import generate_daily_content, REQUIRED_DISCLAIMER
from scripts.ide_guide_agent_skill import generate_agentic_content, infer_ide_details

def test_amp_validator_valid():
    valid_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>Test Page</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/test.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{animation:none}}</style>
  <style amp-custom>body {{ color: red; }}</style>
</head>
<body>
  <p>Test content</p>
  <p>{REQUIRED_DISCLAIMER}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(valid_html)
    assert is_valid is True
    assert len(errors) == 0

def test_amp_validator_invalid():
    invalid_html = "<html><body><img src='test.jpg' style='color:red;'>No disclaimer</body></html>"
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert len(errors) > 0

def test_daily_content_generation(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    generated = generate_daily_content("2026-04-01")
    assert len(generated) == 6  # 3 blog posts + 3 video specs

    # Check that output files exist
    for filepath in generated:
        assert os.path.exists(filepath)

    # Validate blog post
    html_files = [f for f in generated if f.endswith(".html")]
    assert len(html_files) == 3
    for hf in html_files:
        with open(hf, "r", encoding="utf-8") as f:
            content = f.read()
        is_valid, errors = validate_amp_html(content)
        assert is_valid is True, f"Errors in {hf}: {errors}"

def test_agentic_cli_skill(tmp_path):
    output_dir = tmp_path / "agentic_test"
    blog, video = generate_agentic_content("https://github.com/zed-industries/zed", str(output_dir))
    assert os.path.exists(blog)
    assert os.path.exists(video)

    with open(blog, "r", encoding="utf-8") as f:
        html_content = f.read()
    is_valid, errors = validate_amp_html(html_content)
    assert is_valid is True, f"AMP Errors: {errors}"

    with open(video, "r", encoding="utf-8") as f:
        video_data = json.load(f)
    assert video_data["ide_name"] == "Zed"
    assert len(video_data["google_flow_prompts"]) == 4
    assert REQUIRED_DISCLAIMER in video_data["disclaimer"]
