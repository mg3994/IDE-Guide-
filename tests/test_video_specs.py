import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from scripts.generate_daily_content import build_google_flow_spec, build_google_flow_markdown, CURATED_IDES, DISCLAIMER_TEXT

def test_google_flow_spec_fields():
    sample_ide = CURATED_IDES[0] # VS Code
    spec = build_google_flow_spec(sample_ide)

    assert spec["youtube_channel"] == "@IDEguide"
    assert spec["blogger_url"] == "https://ideguide.blogspot.com/"
    assert "YouTube Short" in spec["target_format"]
    assert len(spec["scenes"]) >= 5
    assert spec["disclaimer"] == DISCLAIMER_TEXT

    for scene in spec["scenes"]:
        assert "scene_number" in scene
        assert "timestamp" in scene
        assert "camera_framing" in scene
        assert "lighting" in scene
        assert "visual_prompt" in scene
        assert "narration" in scene

def test_google_flow_markdown_formatting():
    sample_ide = CURATED_IDES[0]
    spec = build_google_flow_spec(sample_ide)
    md = build_google_flow_markdown(spec)

    assert f"# Google Flow Video Spec: {sample_ide['name']}" in md
    assert "@IDEguide" in md
    assert DISCLAIMER_TEXT in md
    assert "### Scene 1" in md
