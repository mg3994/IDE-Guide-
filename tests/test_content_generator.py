import json
import os
import shutil
import tempfile
import pytest

from scripts.generate_daily_content import generate_daily_batch, load_database
from scripts.amp_validator import validate_amp_html, MANDATORY_DISCLAIMER_SNIPPET


@pytest.fixture
def temp_environment():
    tmp_dir = tempfile.mkdtemp()
    db_file = os.path.join(tmp_dir, "ide_database.json")
    history_file = os.path.join(tmp_dir, "history.json")
    content_dir = os.path.join(tmp_dir, "content")

    shutil.copy("data/ide_database.json", db_file)

    yield {
        "db_file": db_file,
        "history_file": history_file,
        "content_dir": content_dir
    }

    shutil.rmtree(tmp_dir)


def test_generate_daily_batch_produces_three_packages(temp_environment):
    env = temp_environment
    res = generate_daily_batch(
        date_str="2025-05-01",
        db_path=env["db_file"],
        history_path=env["history_file"],
        content_dir=env["content_dir"]
    )

    assert res["date"] == "2025-05-01"
    packages = res["packages"]
    # User requirement: exactly three videos a day and three blog posts everyday
    assert len(packages) == 3

    for pkg in packages:
        # Check files exist
        assert os.path.exists(pkg["blog_path"])
        assert os.path.exists(pkg["video_path"])
        assert os.path.exists(pkg["script_path"])

        # Check blog content is AMP valid
        with open(pkg["blog_path"], "r", encoding="utf-8") as f:
            blog_html = f.read()
        is_valid, errors = validate_amp_html(blog_html, require_disclaimer=True)
        assert is_valid is True, f"Errors for {pkg['ide_name']}: {errors}"

        # Verify Google Flow spec structure
        with open(pkg["video_path"], "r", encoding="utf-8") as f:
            flow_data = json.load(f)

        assert "scenes" in flow_data
        assert len(flow_data["scenes"]) >= 5
        assert "mandatory_disclaimer" in flow_data
        assert MANDATORY_DISCLAIMER_SNIPPET in flow_data["mandatory_disclaimer"]
        assert "pacing_notes" in flow_data
        assert "pricing_tier" in flow_data

        # Verify scene prompt details
        for scene in flow_data["scenes"]:
            assert "google_flow_prompt" in scene
            assert "voiceover_script" in scene
            assert len(scene["google_flow_prompt"]) > 20
