import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import pytest
from scripts.ide_guide_agent_skill import run_agent_skill, find_or_build_ide_info
from scripts.generate_daily_content import DISCLAIMER_TEXT

def test_run_agent_skill_by_ide_name(tmp_path):
    out_dir = str(tmp_path / "custom_cursor")
    result = run_agent_skill(ide_name="Cursor", out_dir=out_dir, record_history=False)

    assert result["status"] == "success"
    assert result["ide_name"] == "Cursor AI Code Editor"
    assert os.path.exists(result["files"]["amp_html"])
    assert os.path.exists(result["files"]["flow_spec_json"])
    assert os.path.exists(result["files"]["flow_spec_md"])

    with open(result["files"]["amp_html"], "r", encoding="utf-8") as f:
        amp_content = f.read()
        assert "<html ⚡ lang=\"en\">" in amp_content
        assert DISCLAIMER_TEXT in amp_content

def test_run_agent_skill_by_github_url(tmp_path):
    out_dir = str(tmp_path / "custom_zed")
    result = run_agent_skill(url="https://github.com/zed-industries/zed", out_dir=out_dir, record_history=False)

    assert result["status"] == "success"
    assert "Zed" in result["ide_name"]
    assert os.path.exists(result["files"]["amp_html"])
    assert os.path.exists(result["files"]["flow_spec_json"])

    with open(result["files"]["flow_spec_json"], "r", encoding="utf-8") as f:
        spec = json.load(f)
        assert spec["disclaimer"] == DISCLAIMER_TEXT
        assert spec["youtube_channel"] == "@IDEguide"
        assert spec["blogger_url"] == "https://ideguide.blogspot.com/"
