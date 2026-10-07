import os
import json
import pytest
from argparse import Namespace
from scripts.ide_guide_agent_skill import run_agent_skill, build_custom_ide_data
from scripts.amp_validator import validate_amp_html, DISCLAIMER_TEXT

def test_build_custom_ide_data():
    ide_data = build_custom_ide_data(
        name="Fleet Test",
        category="Modern IDE",
        pricing="Freemium",
        repo_url="https://github.com/test/fleet",
    )
    assert ide_data["name"] == "Fleet Test"
    assert ide_data["category"] == "Modern IDE"
    assert ide_data["pricing"] == "Freemium"
    assert ide_data["repo_url"] == "https://github.com/test/fleet"

def test_run_agent_skill(tmp_path):
    output_dir = str(tmp_path / "skill_output")
    args = Namespace(
        ide_name="Custom Nova",
        category="Lightweight Editor",
        pricing="Paid",
        repo_url="https://github.com/test/nova",
        pros="Ultra fast,Sleek UI",
        cons="Mac only",
        target_audience="macOS developers",
        killer_features="Native macOS theme,Fast search",
        output_dir=output_dir,
    )

    run_agent_skill(args)

    blog_file = os.path.join(output_dir, "blogpost_custom_nova.html")
    spec_file = os.path.join(output_dir, "video_flow_spec_custom_nova.json")

    assert os.path.exists(blog_file)
    assert os.path.exists(spec_file)

    with open(blog_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    is_valid, errors = validate_amp_html(html_content)
    assert is_valid is True, f"AMP Validation failed: {errors}"
    assert "Custom Nova" in html_content
    assert DISCLAIMER_TEXT in html_content

    with open(spec_file, "r", encoding="utf-8") as f:
        spec_data = json.load(f)

    assert spec_data["disclaimer"] == DISCLAIMER_TEXT
    assert spec_data["repo_url"] == "https://github.com/test/nova"
