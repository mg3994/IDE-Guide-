"""
Unit tests for IDE Guide generation tools, AMP HTML validator, history tracking, and agentic CLI skills.
"""

import json
import os
import shutil
import tempfile
import pytest

from scripts.amp_validator import validate_amp_html, NON_SPONSORSHIP_DISCLAIMER
from scripts.ide_guide_agent_skill import (
    get_ide_info,
    generate_amp_blog_post,
    generate_google_flow_spec
)
from scripts.generate_daily_content import (
    generate_daily_package,
    select_daily_ides,
    load_history,
    save_history,
    HISTORY_FILE
)


def test_amp_validator_valid():
    sample_amp = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>Test Page</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/test">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both}}</style>
  <style amp-custom>body {{ color: #333; }}</style>
</head>
<body>
  <h1>Test Title</h1>
  <p>{NON_SPONSORSHIP_DISCLAIMER}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(sample_amp)
    assert is_valid, f"Expected valid AMP, got errors: {errors}"


def test_amp_validator_detects_img_tag():
    invalid_amp = f"""<!doctype html>
<html amp lang="en">
<head>
  <meta charset="utf-8">
  <title>Test Page</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/test">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both}}</style>
</head>
<body>
  <img src="test.jpg" alt="test">
  <p>{NON_SPONSORSHIP_DISCLAIMER}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(invalid_amp)
    assert not is_valid
    assert any("Standard <img> tag found" in err for err in errors)


def test_amp_validator_detects_missing_disclaimer():
    no_disclaimer_amp = """<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <title>Test Page</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/test">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both}}</style>
</head>
<body>
  <h1>No Disclaimer</h1>
</body>
</html>"""
    is_valid, errors = validate_amp_html(no_disclaimer_amp)
    assert not is_valid
    assert any("Missing required non-sponsorship disclaimer" in err for err in errors)


def test_ide_info_retrieval():
    vscode_info = get_ide_info("VS Code")
    assert vscode_info["developer"] == "Microsoft"
    assert "Free" in vscode_info["pricing"]

    custom_url_info = get_ide_info("https://github.com/my-org/my-custom-editor")
    assert custom_url_info["full_name"] == "My Custom Editor"


def test_agentic_skill_generation():
    ide_info = get_ide_info("Cursor")
    amp_html = generate_amp_blog_post(ide_info)
    is_valid, errors = validate_amp_html(amp_html)
    assert is_valid, f"Generated blog post failed AMP validation: {errors}"
    assert "Anysphere" in amp_html
    assert NON_SPONSORSHIP_DISCLAIMER in amp_html

    flow_spec = generate_google_flow_spec(ide_info)
    assert flow_spec["channel"] == "@IDEguide"
    assert "youtube_shorts" in flow_spec["formats"]
    assert "youtube_longform" in flow_spec["formats"]
    assert len(flow_spec["formats"]["youtube_shorts"]["scenes"]) == 4


def test_daily_content_generation(tmp_path, monkeypatch):
    test_history_path = str(tmp_path / "history.json")
    monkeypatch.setattr("scripts.generate_daily_content.HISTORY_FILE", test_history_path)

    # First run
    package_dir = generate_daily_package("2026-01-01")
    assert os.path.exists(package_dir)
    manifest_path = os.path.join(package_dir, "manifest.json")
    assert os.path.exists(manifest_path)

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    assert len(manifest["items"]) == 3
    for item in manifest["items"]:
        assert item["amp_valid"] is True
        assert os.path.exists(item["blog_file"])
        assert os.path.exists(item["video_spec_file"])

    # Verify history tracking
    with open(test_history_path, 'r', encoding='utf-8') as f:
        history_data = json.load(f)
    assert len(history_data["covered_ides"]) == 3
