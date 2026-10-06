import os
import json
import tempfile
import pytest
from scripts.amp_validator import validate_amp_html, DISCLAIMER_TEXT
from scripts.generate_daily_content import generate_daily_content_packages, generate_amp_blog_html, IDE_DATABASE
from scripts.ide_guide_agent_skill import infer_tool_data_from_name_or_repo, generate_custom_amp_blog, generate_custom_google_flow_spec

def test_amp_validator_valid():
    sample_tool = IDE_DATABASE[0]
    html = generate_amp_blog_html(sample_tool, "https://ideguide.blogspot.com/2026/10/vscode.html")
    is_valid, errors = validate_amp_html(html)
    assert is_valid is True
    assert len(errors) == 0

def test_amp_validator_invalid_missing_boilerplate():
    html = "<html><head><meta charset='utf-8'></head><body>" + DISCLAIMER_TEXT + "</body></html>"
    is_valid, errors = validate_amp_html(html)
    assert is_valid is False
    assert any("amp-boilerplate" in err for err in errors)

def test_amp_validator_invalid_forbidden_img_tag():
    sample_tool = IDE_DATABASE[0]
    html = generate_amp_blog_html(sample_tool, "https://ideguide.blogspot.com/2026/10/vscode.html")
    html_with_img = html.replace("</body>", "<img src='test.jpg'></body>")
    is_valid, errors = validate_amp_html(html_with_img)
    assert is_valid is False
    assert any("Forbidden <img>" in err for err in errors)

def test_generate_daily_content_packages():
    with tempfile.TemporaryDirectory() as tmp_dir:
        history_path = os.path.join(tmp_dir, "history.json")
        output_dir = os.path.join(tmp_dir, "content")

        files = generate_daily_content_packages(
            date_str="2026-10-06",
            output_base_dir=output_dir,
            history_file=history_path
        )

        assert len(files) == 6  # 3 blog posts + 3 flow video specs

        # Check history updated
        with open(history_path, "r", encoding="utf-8") as f:
            history = json.load(f)
        assert len(history["covered_tools"]) == 3

        # Verify disclaimer in every generated file
        for filepath in files:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            assert DISCLAIMER_TEXT in content

def test_agent_skill_infer_and_generate():
    tool_data = infer_tool_data_from_name_or_repo(ide_name="Zed")
    assert tool_data["name"] == "Zed"

    repo_data = infer_tool_data_from_name_or_repo(repo_url="https://github.com/neovim/neovim")
    assert repo_data["name"] == "Neovim"

    blog_html = generate_custom_amp_blog(repo_data, "https://ideguide.blogspot.com/custom/neovim.html")
    is_valid, errors = validate_amp_html(blog_html)
    assert is_valid is True

    flow_spec = generate_custom_google_flow_spec(repo_data)
    assert flow_spec["tool_name"] == "Neovim"
    assert flow_spec["non_sponsorship_disclaimer"] == DISCLAIMER_TEXT
