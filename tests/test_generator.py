import os
import json
import pytest
import datetime
from scripts.generate_daily_content import (
    generate_daily_package,
    generate_google_flow_video_spec,
    IDE_DATABASE,
    DISCLAIMER_TEXT,
    load_history,
    save_history
)
from scripts.ide_guide_agent_skill import run_agentic_skill


def test_ide_database_validity():
    assert len(IDE_DATABASE) >= 10
    for ide in IDE_DATABASE:
        assert "id" in ide
        assert "name" in ide
        assert "pros" in ide and len(ide["pros"]) >= 2
        assert "cons" in ide and len(ide["cons"]) >= 1
        assert "pricing" in ide


def test_generate_daily_package(tmp_path, monkeypatch):
    test_date = "2026-10-15"
    history_file = tmp_path / "history.json"

    # Patch history file location in content directory
    monkeypatch.chdir(tmp_path)

    created_files = generate_daily_package(target_date=test_date)

    # Must generate 3 AMP blog posts + 3 Flow JSON specs + 3 Flow Markdown specs = 9 files total
    assert len(created_files) == 9
    assert os.path.exists(tmp_path / "content" / test_date)

    # Check that 3 unique AMP files exist
    amp_files = [f for f in created_files if f.endswith("_blog_post.html")]
    assert len(amp_files) == 3

    # Check history saved
    history = load_history(str(tmp_path / "content" / "history.json"))
    assert len(history["covered_ides"]) == 3


def test_google_flow_video_spec_completeness():
    test_ide = IDE_DATABASE[0]
    date_str = "2026-10-15"
    spec = generate_google_flow_video_spec(test_ide, date_str, index=1)

    assert spec["metadata"]["ide_name"] == test_ide["name"]
    assert spec["metadata"]["disclaimer"] == DISCLAIMER_TEXT
    assert "google_flow_prompt_config" in spec
    assert "youtube_shorts_spec_60s" in spec
    assert len(spec["youtube_shorts_spec_60s"]["scenes"]) == 4

    for scene in spec["youtube_shorts_spec_60s"]["scenes"]:
        assert "google_flow_video_prompt" in scene
        assert "voiceover_script" in scene
        assert len(scene["google_flow_video_prompt"]) > 10


def test_agentic_skill_cli(tmp_path):
    output_dir = str(tmp_path / "skill_output")
    res = run_agentic_skill(ide_name="Zed Editor", output_dir=output_dir, validate=True)

    assert res["ide_name"] == "Zed Editor"
    assert res["validation_passed"] is True
    assert len(res["generated_files"]) == 3
