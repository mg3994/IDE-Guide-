import os
import shutil
import tempfile
import pytest
from scripts.amp_validator import validate_amp_html, MANDATORY_DISCLAIMER
from scripts.generate_daily_content import (
    IDE_DATABASE, generate_amp_blog_post, generate_google_flow_spec,
    run_daily_generation, load_history, save_history
)
from scripts.ide_guide_agent_skill import generate_custom_ide_content

def test_amp_validator_valid():
    sample_amp = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{}}</style>
  <noscript><style amp-boilerplate>body{{}}</style></noscript>
</head>
<body>
  <p>{MANDATORY_DISCLAIMER}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(sample_amp)
    assert is_valid is True
    assert len(errors) == 0

def test_amp_validator_invalid_missing_disclaimer():
    sample_amp = """<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{}</style>
  <noscript><style amp-boilerplate>body{}</style></noscript>
</head>
<body>
  <p>Some random post without disclaimer</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(sample_amp)
    assert is_valid is False
    assert any("disclaimer" in err.lower() for err in errors)

def test_generate_daily_content_creates_files(monkeypatch):
    temp_dir = tempfile.mkdtemp()
    try:
        history_file = os.path.join(temp_dir, "history.json")
        monkeypatch.setattr("scripts.generate_daily_content.HISTORY_FILE", history_file)

        test_date = "2099-01-01"
        run_daily_generation(date_str=test_date)

        target_dir = os.path.join("content", test_date)
        assert os.path.exists(target_dir)

        files = os.listdir(target_dir)
        html_files = [f for f in files if f.endswith(".html")]
        md_files = [f for f in files if f.endswith(".md")]

        assert len(html_files) == 3
        assert len(md_files) == 3

        # Verify AMP validity and disclaimer in generated files
        for html_file in html_files:
            filepath = os.path.join(target_dir, html_file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            is_valid, errors = validate_amp_html(content)
            assert is_valid, f"AMP validation failed for {html_file}: {errors}"
            assert MANDATORY_DISCLAIMER in content

        # Clean up test output directory
        shutil.rmtree(target_dir)

    finally:
        shutil.rmtree(temp_dir)

def test_agent_skill_custom_ide():
    temp_dir = tempfile.mkdtemp()
    try:
        blog_path, video_path = generate_custom_ide_content(
            ide_name="Lapce",
            output_dir=temp_dir,
            category="Code Editor",
            pricing="Free & Open Source",
            pricing_category="Free",
            pros="Lightning fast Rust editor; Native UI",
            cons="Early development state",
            best_for="Rust developers and lightweight editor fans",
            site_url="https://lapce.dev"
        )

        assert os.path.exists(blog_path)
        assert os.path.exists(video_path)

        with open(blog_path, "r", encoding="utf-8") as f:
            blog_html = f.read()

        is_valid, errors = validate_amp_html(blog_html)
        assert is_valid
        assert "Lapce" in blog_html
        assert MANDATORY_DISCLAIMER in blog_html

        with open(video_path, "r", encoding="utf-8") as f:
            video_spec = f.read()

        assert "Google Flow Video Generation Spec: Lapce" in video_spec
        assert MANDATORY_DISCLAIMER in video_spec

    finally:
        shutil.rmtree(temp_dir)
