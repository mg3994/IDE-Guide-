import os
import json
import pytest
from scripts.amp_validator import validate_amp_html, validate_file, DISCLAIMER_TEXT
from scripts.ide_guide_agent_skill import (
    generate_amp_blog_post,
    generate_google_flow_video_spec,
    run_agent_skill,
    DEFAULT_IDE_KNOWLEDGE
)
from scripts.generate_daily_content import (
    generate_daily_content_package,
    load_history,
    save_history,
    select_daily_ides
)


def test_amp_validator_valid():
    sample_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1">
  <link rel="canonical" href="https://ideguide.blogspot.com/sample.html">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{animation:none}}</style>
  <style amp-custom>body{{color:red;}}</style>
</head>
<body>
  <h1>Test</h1>
  <p>{DISCLAIMER_TEXT}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(sample_html)
    assert is_valid is True
    assert len(errors) == 0


def test_amp_validator_invalid_img():
    invalid_html = f"""<!doctype html>
<html amp lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1">
  <link rel="canonical" href="https://ideguide.blogspot.com/sample.html">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-boilerplate>body{{animation:none}}</style>
  <style amp-custom>body{{color:red;}}</style>
</head>
<body>
  <img src="test.jpg">
  <p>{DISCLAIMER_TEXT}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("Forbidden <img> tag" in err for err in errors)


def test_generate_amp_blog_post():
    ide_info = DEFAULT_IDE_KNOWLEDGE["VS Code"]
    html_output = generate_amp_blog_post("VS Code", ide_info)
    is_valid, errors = validate_amp_html(html_output)
    assert is_valid is True, f"Errors: {errors}"
    assert "VS Code" in html_output
    assert DISCLAIMER_TEXT in html_output


def test_generate_google_flow_video_spec():
    ide_info = DEFAULT_IDE_KNOWLEDGE["Cursor"]
    spec = generate_google_flow_video_spec("Cursor", ide_info)
    assert spec["ide_name"] == "Cursor"
    assert len(spec["google_flow_scenes"]) == 4
    assert DISCLAIMER_TEXT in spec["voiceover_script"]


def test_agent_skill_execution(tmp_path):
    output_dir = str(tmp_path / "custom")
    res = run_agent_skill("PyCharm", output_dir=output_dir)
    assert os.path.exists(res["blog_post"])
    assert os.path.exists(res["video_spec"])
    assert validate_file(res["blog_post"]) is True


def test_daily_content_generation(tmp_path, monkeypatch):
    test_date = "2026-10-10"
    monkeypatch.setattr("scripts.generate_daily_content.HISTORY_FILE", str(tmp_path / "history.json"))

    results = generate_daily_content_package(target_date=test_date)
    assert len(results) == 3
    for pkg in results:
        assert os.path.exists(pkg["blog_post"])
        assert os.path.exists(pkg["video_spec"])
        assert validate_file(pkg["blog_post"]) is True
