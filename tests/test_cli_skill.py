import pytest
import os
import json
from scripts.ide_guide_agent_skill import run_skill
from scripts.generate_daily_content import DISCLAIMER_TEXT

def test_cli_skill_by_ide_name(tmp_path):
    out_dir = str(tmp_path / "skill_vscode")
    res_dir = run_skill(ide_name="Visual Studio Code", out_dir=out_dir)

    assert res_dir == out_dir
    amp_file = os.path.join(out_dir, "blog_post_amp.html")
    spec_file = os.path.join(out_dir, "google_flow_video_spec.json")

    assert os.path.isfile(amp_file)
    assert os.path.isfile(spec_file)

    with open(spec_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["ide_name"] == "Visual Studio Code"
        assert data["disclaimer"] == DISCLAIMER_TEXT

def test_cli_skill_shorts(tmp_path):
    out_dir = str(tmp_path / "skill_shorts")
    run_skill(ide_name="Zed", out_dir=out_dir, is_short=True)

    spec_file = os.path.join(out_dir, "google_flow_video_spec.json")
    with open(spec_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data["format"] == "shorts"
        assert data["aspect_ratio"] == "9:16"
