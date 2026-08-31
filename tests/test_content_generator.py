import pytest
import os
import json
import shutil
from scripts.generate_daily_content import run_daily_generation, DISCLAIMER_TEXT

def test_run_daily_generation(tmp_path):
    out_root = str(tmp_path / "content")
    date_str = "2026-09-01"

    generated_dirs = run_daily_generation(output_root=out_root, target_date=date_str)
    assert len(generated_dirs) == 3

    for item_dir in generated_dirs:
        assert os.path.exists(item_dir)
        amp_file = os.path.join(item_dir, "blog_post_amp.html")
        spec_file = os.path.join(item_dir, "google_flow_video_spec.json")

        assert os.path.isfile(amp_file)
        assert os.path.isfile(spec_file)

        with open(spec_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert data["disclaimer"] == DISCLAIMER_TEXT
            assert "scenes" in data
            assert len(data["scenes"]) == 5
