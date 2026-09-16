import os
import json
import pytest
from scripts.generate_daily_content import (
    run_daily_generation,
    DEFAULT_IDE_CATALOG,
    DISCLAIMER_TEXT,
    BLOGGER_URL,
    YOUTUBE_URL
)

def test_catalog_structure():
    assert len(DEFAULT_IDE_CATALOG) >= 5
    for item in DEFAULT_IDE_CATALOG:
        assert "name" in item
        assert "slug" in item
        assert "category" in item
        assert "pricing" in item
        assert "summary" in item
        assert isinstance(item["pros"], list)
        assert len(item["pros"]) > 0
        assert isinstance(item["cons"], list)
        assert len(item["cons"]) > 0

def test_daily_generation_output(tmp_path):
    target_date = "2026-09-18"
    results = run_daily_generation(target_date)
    assert len(results) == 3

    daily_dir = os.path.join("content", target_date)
    assert os.path.exists(daily_dir)

    for res in results:
        assert os.path.exists(res["amp_post"])
        assert os.path.exists(res["video_spec_json"])
        assert os.path.exists(res["video_spec_md"])

        # Check JSON video spec
        with open(res["video_spec_json"], "r", encoding="utf-8") as f:
            v_data = json.load(f)
            assert "title" in v_data
            assert "scenes" in v_data
            assert len(v_data["scenes"]) == 5
            assert v_data["disclaimer"] == DISCLAIMER_TEXT
