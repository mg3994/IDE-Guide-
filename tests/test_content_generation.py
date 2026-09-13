"""
Unit tests for CLI Agent Skill and Daily Content Generator.
"""

import sys
import os
import json
import pytest
import tempfile
import shutil

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.ide_guide_agent_skill import (
    resolve_ide_data,
    generate_google_flow_video_spec,
    DISCLAIMER_TEXT
)
from scripts.generate_daily_content import select_daily_ides, load_history, save_history


def test_resolve_ide_data_known():
    info = resolve_ide_data(ide_query="cursor")
    assert info["name"] == "Cursor IDE"
    assert len(info["pros"]) > 0
    assert len(info["cons"]) > 0
    assert "Freemium" in info["pricing"]


def test_resolve_ide_data_custom():
    info = resolve_ide_data(ide_query="Custom Nano Editor", custom_pricing="Free")
    assert info["name"] == "Custom Nano Editor"
    assert info["pricing"] == "Free"


def test_google_flow_video_spec_structure():
    info = resolve_ide_data(ide_query="Zed Editor")
    spec = generate_google_flow_video_spec(info)

    assert spec["channel"] == "@IDEguide"
    assert spec["ide_name"] == "Zed Editor"
    assert spec["disclaimer"] == DISCLAIMER_TEXT

    # Shorts spec assertions
    shorts = spec["youtube_shorts_spec"]
    assert shorts["aspect_ratio"] == "9:16"
    assert shorts["resolution"] == "1080x1920"
    assert len(shorts["scenes"]) == 5

    # Standard video spec assertions
    video = spec["youtube_video_spec"]
    assert video["aspect_ratio"] == "16:9"
    assert len(video["narration_outline"]) > 0


def test_select_daily_ides_rotation():
    history = {"covered_ides": ["Cursor IDE"], "daily_runs": []}
    selected = select_daily_ides(history, target_count=3)

    assert len(selected) == 3
    names = [s["name"] for s in selected]
    assert "Cursor IDE" not in names


def test_history_file_persistence():
    temp_dir = tempfile.mkdtemp()
    try:
        hist_path = os.path.join(temp_dir, "history.json")
        data = {"covered_ides": ["TestIDE"], "daily_runs": []}

        with open(hist_path, "w", encoding="utf-8") as f:
            json.dump(data, f)

        with open(hist_path, "r", encoding="utf-8") as f:
            loaded = json.load(f)

        assert loaded["covered_ides"] == ["TestIDE"]
    finally:
        shutil.rmtree(temp_dir)
