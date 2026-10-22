import json
from pathlib import Path
import pytest
from scripts.generate_daily_content import generate_daily_content, IDE_POOL
from scripts.amp_validator import validate_file, REQUIRED_DISCLAIMER


def test_generate_daily_content(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    test_date = "2026-05-01"
    dirs = generate_daily_content(today_str=test_date)

    assert len(dirs) == 3
    for d in dirs:
        p = Path(d)
        assert p.exists()
        amp_file = p / "blog_post.amp.html"
        json_file = p / "video_flow_spec.json"
        md_file = p / "video_flow_spec.md"

        assert amp_file.exists()
        assert json_file.exists()
        assert md_file.exists()

        # Validate AMP
        val_res = validate_file(str(amp_file))
        assert val_res["valid"] is True, f"AMP validation failed for {amp_file}: {val_res['errors']}"

        # Check disclaimer in json and md
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert data["disclaimer"] == REQUIRED_DISCLAIMER

        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
            assert REQUIRED_DISCLAIMER in content

    # Check history.json
    history_file = Path("content/history.json")
    assert history_file.exists()
    with open(history_file, "r", encoding="utf-8") as f:
        hist_data = json.load(f)
        assert len(hist_data["covered_ids"]) == 3
        assert len(hist_data["history_log"]) == 1
        assert hist_data["history_log"][0]["date"] == test_date
