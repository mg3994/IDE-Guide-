import os
import json
import pytest
from scripts.amp_validator import validate_amp_html, REQUIRED_DISCLAIMER
from scripts.generate_daily_content import run_daily_content_generation, generate_amp_blog_html, IDE_DATABASE
from scripts.ide_guide_agent_skill import generate_custom_ide_content


def test_amp_validator_valid():
    sample_ide = IDE_DATABASE["VS Code"]
    valid_html = generate_amp_blog_html(sample_ide, "https://ideguide.blogspot.com/2026/10/vs-code.html")
    is_valid, errs = validate_amp_html(valid_html)
    assert is_valid is True
    assert len(errs) == 0


def test_amp_validator_invalid_missing_disclaimer():
    sample_ide = IDE_DATABASE["VS Code"]
    valid_html = generate_amp_blog_html(sample_ide, "https://ideguide.blogspot.com/2026/10/vs-code.html")
    invalid_html = valid_html.replace(REQUIRED_DISCLAIMER, "")
    is_valid, errs = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("non-sponsorship disclaimer" in err for err in errs)


def test_amp_validator_prohibits_plain_img():
    sample_ide = IDE_DATABASE["VS Code"]
    valid_html = generate_amp_blog_html(sample_ide, "https://ideguide.blogspot.com/2026/10/vs-code.html")
    invalid_html = valid_html + '<img src="test.jpg" alt="test">'
    is_valid, errs = validate_amp_html(invalid_html)
    assert is_valid is False
    assert any("Prohibited <img> tag" in err for err in errs)


def test_daily_content_generation(tmp_path):
    generated_files = run_daily_content_generation("2026-10-25")
    assert len(generated_files) == 6  # 3 blog posts + 3 video specs

    for fpath in generated_files:
        assert os.path.exists(fpath)
        if fpath.endswith(".html"):
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            is_valid, errs = validate_amp_html(content)
            assert is_valid is True, f"AMP errors in {fpath}: {errs}"
        elif fpath.endswith(".json"):
            with open(fpath, "r", encoding="utf-8") as f:
                spec = json.load(f)
            assert "scenes" in spec
            assert len(spec["scenes"]) == 5
            assert REQUIRED_DISCLAIMER in spec["disclaimer"]


def test_agentic_cli_skill(tmp_path):
    out_dir = str(tmp_path / "custom")
    result = generate_custom_ide_content("Sublime Text", out_dir)
    assert result["amp_valid"] is True
    assert os.path.exists(result["html_file"])
    assert os.path.exists(result["video_spec_file"])

    with open(result["html_file"], "r", encoding="utf-8") as f:
        html = f.read()
    assert "Sublime Text" in html
    assert REQUIRED_DISCLAIMER in html
