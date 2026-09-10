import json
import os
import sys
import subprocess
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from ide_guide_agent_skill import fetch_github_repo_info

def test_fetch_github_repo_info_fallback():
    info = fetch_github_repo_info("https://github.com/zed-industries/zed")
    assert info["name"] is not None
    assert "url" in info
    assert "pros" in info
    assert "cons" in info

def test_cli_skill_execution(tmp_path):
    output_dir = tmp_path / "test_skills"
    cmd = [
        sys.executable,
        "scripts/ide_guide_agent_skill.py",
        "--ide", "Helix Editor",
        "--output-dir", str(output_dir)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0

    blog_file = output_dir / "helix_editor_blog_post.amp.html"
    spec_file = output_dir / "helix_editor_google_flow_spec.json"

    assert blog_file.exists()
    assert spec_file.exists()

    with open(blog_file, "r", encoding="utf-8") as f:
        content = f.read()
        assert "<style amp-custom>" in content
        assert "Disclaimer: IDE Guide is an independent technical publication." in content
