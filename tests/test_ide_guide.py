import os
import json
import pytest
from scripts.amp_validator import validate_amp_html, REQUIRED_DISCLAIMER
from scripts.generate_daily_content import run_daily_generation, IDE_DATABASE, generate_amp_blog_post, generate_google_flow_video_spec
from scripts.ide_guide_agent_skill import analyze_custom_ide, generate_custom_package


def test_amp_validator_valid():
    html = f"""<!doctype html>
<html ⚡ lang="en">
<head><meta charset="utf-8"></head>
<body>
  <amp-img src="test.jpg" width="600" height="400" layout="responsive" alt="test"></amp-img>
  <p>{REQUIRED_DISCLAIMER}</p>
</body>
</html>"""
    is_valid, errors = validate_amp_html(html)
    assert is_valid is True
    assert len(errors) == 0


def test_amp_validator_invalid_img():
    html = f"""<div><img src="test.jpg"><p>{REQUIRED_DISCLAIMER}</p></div>"""
    is_valid, errors = validate_amp_html(html)
    assert is_valid is False
    assert any("Forbidden standard tag" in e for e in errors)


def test_amp_validator_missing_disclaimer():
    html = """<!doctype html><html ⚡ lang="en"><body><p>Hello world</p></body></html>"""
    is_valid, errors = validate_amp_html(html)
    assert is_valid is False
    assert any("disclaimer missing" in e for e in errors)


def test_generate_daily_content(tmp_path):
    generated = run_daily_generation(base_dir=str(tmp_path))
    assert len(generated) == 6  # 3 blog posts + 3 video specs

    history_file = tmp_path / "content" / "history.json"
    assert history_file.exists()

    with open(history_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data["covered"]) == 3
    assert len(data["history"]) == 1


def test_agent_skill_custom_repo(tmp_path):
    out_dir = str(tmp_path / "skill_out")
    generate_custom_package("https://github.com/emacs-mirror/emacs", output_dir=out_dir, pricing="Free / Open Source")

    expected_blog = os.path.join(out_dir, "amp_blog_emacs.html")
    expected_spec = os.path.join(out_dir, "google_flow_spec_emacs.md")

    assert os.path.exists(expected_blog)
    assert os.path.exists(expected_spec)

    with open(expected_blog, "r", encoding="utf-8") as f:
        content = f.read()
    is_valid, errors = validate_amp_html(content)
    assert is_valid is True
