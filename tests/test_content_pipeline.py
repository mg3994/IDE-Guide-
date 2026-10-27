"""
Unit tests for IDE Guide AMP Validator, Daily Generator, and Agentic Skill Tool.
"""

import os
import json
import pytest
import yaml
from scripts.amp_validator import validate_amp_html, REQUIRED_DISCLAIMER
from scripts.generate_daily_content import (
    generate_daily_package,
    select_daily_ides,
    IDE_CATALOG,
    HISTORY_FILE
)

def test_amp_validator_valid_post():
    valid_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <title>Test Editor Review</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/test.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{animation:none}}</style>
  <style amp-custom>body {{ color: #111; }}</style>
</head>
<body>
  <h1>Test Editor</h1>
  <amp-img src="https://example.com/img.jpg" width="800" height="400" layout="responsive" alt="test"></amp-img>
  <div class="disclaimer">{REQUIRED_DISCLAIMER}</div>
</body>
</html>"""
    valid, errors = validate_amp_html(valid_html)
    assert valid is True
    assert len(errors) == 0

def test_amp_validator_invalid_img_tag():
    invalid_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <title>Test Editor Review</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/test.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{animation:none}}</style>
  <style amp-custom>body {{ color: #111; }}</style>
</head>
<body>
  <h1>Test Editor</h1>
  <img src="https://example.com/img.jpg" alt="forbidden">
  <div class="disclaimer">{REQUIRED_DISCLAIMER}</div>
</body>
</html>"""
    valid, errors = validate_amp_html(invalid_html)
    assert valid is False
    assert any("Forbidden <img> tag found" in err for err in errors)

def test_amp_validator_missing_disclaimer():
    invalid_html = """<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <title>Test Editor Review</title>
  <link rel="canonical" href="https://ideguide.blogspot.com/test.html">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{animation:none}}</style>
  <style amp-custom>body {{ color: #111; }}</style>
</head>
<body>
  <h1>Test Editor</h1>
</body>
</html>"""
    valid, errors = validate_amp_html(invalid_html)
    assert valid is False
    assert any("Missing or incorrect non-sponsorship disclaimer" in err for err in errors)

def test_daily_package_generation(tmp_path, monkeypatch):
    # Setup temporary directory for content generation
    monkeypatch.chdir(tmp_path)

    generated_files = generate_daily_package("2026-10-27")
    assert len(generated_files) == 6  # 3 blog posts + 3 video specs

    amp_posts = [f for f in generated_files if f.endswith(".html")]
    video_specs = [f for f in generated_files if f.endswith(".yaml")]

    assert len(amp_posts) == 3
    assert len(video_specs) == 3

    # Validate each generated AMP post
    for post in amp_posts:
        with open(post, "r", encoding="utf-8") as f:
            content = f.read()
        valid, errors = validate_amp_html(content)
        assert valid is True, f"Errors in {post}: {errors}"

    # Validate each video spec YAML
    for spec_file in video_specs:
        with open(spec_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        assert "meta" in data
        assert "google_flow_prompts" in data
        assert "script" in data
        assert REQUIRED_DISCLAIMER in data["script"]["disclaimer"]

def test_history_rotation(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    selected_day1 = select_daily_ides(3)
    assert len(selected_day1) == 3

    selected_day2 = select_daily_ides(3)
    assert len(selected_day2) == 3

    slugs_day1 = {ide["slug"] for ide in selected_day1}
    slugs_day2 = {ide["slug"] for ide in selected_day2}

    # Day 1 and Day 2 should cover distinct IDEs
    assert len(slugs_day1.intersection(slugs_day2)) == 0
