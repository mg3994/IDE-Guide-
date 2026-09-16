import os
import json
from scripts.ide_guide_agent_skill import run_agentic_skill
from scripts.generate_daily_content import DISCLAIMER_TEXT

def test_agentic_skill_execution(tmp_path):
    out_dir = str(tmp_path / "custom_agentic_build")
    res = run_agentic_skill(
        ide_name="Zed Editor",
        category="Rust Code Editor",
        pricing="100% Free",
        developer="Zed Industries",
        output_dir=out_dir
    )

    assert os.path.exists(res["amp_path"])
    assert os.path.exists(res["json_path"])
    assert os.path.exists(res["md_path"])

    with open(res["amp_path"], "r", encoding="utf-8") as f:
        amp_content = f.read()
        assert "Zed Editor" in amp_content
        assert "<amp-img" in amp_content
        assert DISCLAIMER_TEXT in amp_content

    with open(res["json_path"], "r", encoding="utf-8") as f:
        video_json = json.load(f)
        assert video_json["ide_name"] == "Zed Editor"
        assert len(video_json["scenes"]) == 5
