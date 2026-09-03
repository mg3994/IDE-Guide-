import json
import os
import subprocess
import pytest
from scripts.ide_guide_agent_skill import (
    DISCLAIMER_TEXT,
    get_ide_info,
    generate_amp_html,
    generate_google_flow_spec
)


def test_get_ide_info_known():
    info = get_ide_info(ide_name="Cursor")
    assert info["name"] == "Cursor"
    assert "Claude 3.5 Sonnet" in info["description"] or len(info["pros"]) > 0
    assert "Freemium" in info["pricing"]


def test_get_ide_info_repo():
    info = get_ide_info(repo_url="https://github.com/zed-industries/zed")
    assert "Zed" in info["name"]
    assert len(info["pros"]) > 0


def test_generate_google_flow_spec():
    info = get_ide_info(ide_name="Zed")
    spec = generate_google_flow_spec(info)

    assert spec["target_platform"] == "YouTube Shorts / Longform (@IDEguide)"
    assert spec["aspect_ratio"] == "9:16"
    assert spec["ide_name"] == "Zed Editor" or "Zed" in spec["ide_name"]
    assert "visual_prompts" in spec
    assert "lighting" in spec["visual_prompts"]
    assert "narration_script" in spec
    assert len(spec["narration_script"]) >= 5
    assert spec["disclaimer"] == DISCLAIMER_TEXT


def test_cli_execution(tmp_path):
    outdir = str(tmp_path / "custom_output")
    cmd = [
        "python3",
        "scripts/ide_guide_agent_skill.py",
        "--ide", "Neovim",
        "--outdir", outdir
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0
    assert os.path.exists(outdir)

    files = os.listdir(outdir)
    assert any("blogpost" in f for f in files)
    assert any("video_spec" in f for f in files)
