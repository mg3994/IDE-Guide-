import pytest
import os
import json
import subprocess
from scripts.amp_validator import validate_amp_html, REQUIRED_DISCLAIMER

def test_agent_skill_cli(tmp_path):
    out_dir = str(tmp_path / "custom")
    cmd = [
        "python3",
        "scripts/ide_guide_agent_skill.py",
        "--ide", "Neovim Modal Editor",
        "--pricing", "Free Open Source",
        "--output-dir", out_dir
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    res = subprocess.run(cmd, capture_output=True, text=True, env=env)
    assert res.returncode == 0, f"CLI command failed with stderr: {res.stderr}"

    blog_path = os.path.join(out_dir, "blog_post_neovim-modal-editor.html")
    spec_path = os.path.join(out_dir, "video_spec_neovim-modal-editor.json")
    script_path = os.path.join(out_dir, "video_script_neovim-modal-editor.md")

    assert os.path.exists(blog_path)
    assert os.path.exists(spec_path)
    assert os.path.exists(script_path)

    with open(blog_path, "r", encoding="utf-8") as f:
        html = f.read()
        assert REQUIRED_DISCLAIMER in html
        is_valid, errors = validate_amp_html(html)
        assert is_valid, f"Generated blog HTML failed AMP validation: {errors}"

    with open(spec_path, "r", encoding="utf-8") as f:
        spec = json.load(f)
        assert spec["ide_name"] == "Neovim Modal Editor"
        assert "shorts_spec" in spec
        assert "full_video_spec" in spec
